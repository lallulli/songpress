from collections import defaultdict
from datetime import timedelta
from pathlib import Path
from pprint import pprint
import asyncio
import logging
import random
import os

from minizinc import Instance, Model, Solver, Driver, Status

MIN_ISOLATED_BLOCK_HEIGHT = 65
# MIN_ISOLATED_BLOCK_HEIGHT = 55

BLOCK_SEPARATOR_HEIGHT = 21
# BLOCK_SEPARATOR_HEIGHT = 29
COLUMN_HEIGHT = 882.6
# COLUMN_HEIGHT = 1243
REAL_TITLE_HEIGHT = 47.2
# REAL_TITLE_HEIGHT = 67

COLUMNS_PER_PAGE = 2
COLUMN_MODULE = 4
EMPTY_STARTING_COLUMNS = 2

MAX_SONGS_TIMEOUT_SECONDS = 2 * 60
MIN_PAGE_TIMEOUT_SECONDS = 90
N_SONGS_BATCH = 18
SCALE = 10


def scale(h):
    return int(round(SCALE * h))


def greedy_columns(
    previous,
    height,
    column_height,
    column_module,
    empty_starting_columns,
    min_isolated_block_height,
):
    """
    Number of columns of a feasible solution, used as upper bound in the optimization model

    Songs are placed in the given order, each one in the current column if possible, otherwise
    in the next column, otherwise in the next page. Constraints are the same as in the model,
    hence all heights must be already scaled (as they are passed to the model).
    """
    songs = []
    for b, p in enumerate(previous):
        if p == 0:
            songs.append([])
        songs[-1].append(b)

    def is_page_start(c):
        """Blocks cannot be wrapped to column c (same condition as in the models)"""
        return c % column_module == (empty_starting_columns + 1) % column_module

    def place(song, col, load):
        """Place song starting from (col, load); return final (col, load), or None if not possible"""
        for i, b in enumerate(song):
            if load + height[b] <= column_height:
                load += height[b]
            elif (
                i > 0
                and height[b] <= column_height
                and not is_page_start(col + 1)
                and not (i == 1 and height[song[0]] < min_isolated_block_height)
            ):
                col += 1
                load = height[b]
            else:
                return None
        return col, load

    col, load = 1, 0
    for song in songs:
        next_page = col + 1
        while not is_page_start(next_page):
            next_page += 1
        for start in ((col, load), (col + 1, 0), (next_page, 0)):
            res = place(song, *start)
            if res is not None:
                break
        else:
            raise ValueError(f"Song with blocks {song} does not fit in a page")
        col, load = res

    print(f"Upper bound on number of columns: {col}")
    return col


class Problem:
    def __init__(
        self,
        metrics,
        column_height=COLUMN_HEIGHT,
        real_title_height=REAL_TITLE_HEIGHT,
        block_separator_height=BLOCK_SEPARATOR_HEIGHT,
        column_module=COLUMN_MODULE,
        columns_per_page=COLUMNS_PER_PAGE,
        empty_starting_columns=EMPTY_STARTING_COLUMNS,
        min_isolated_block_height=MIN_ISOLATED_BLOCK_HEIGHT,
    ):
        """
        Create optimizer object

        `metrics` is a dict `{filename: file_heights}` where 'file_heights` is the list
        of verse and chorus block heights.

        `column_height` is the overall height of the column. It can be found by pasting a song
        with a known height h:
        - apply the desired resize scale r (e.g. r = 64%) to the song
        - then, rescale the song to full height, by applying a scaling factor s
        - column_height = h * s

        `block_separator_height` is the real distance between consecutive blocks. It can be found as:
        bsh = (song_height - sum_{i in blocks}{block_height_i}) / (n_blocks - 1)

        `real_title_height` is the height of the real title that will be used in the publication, including
        the blank space to be left BELOW the title (and not above). It can be found in this way:
        1. align the title to the top of the column
        2. paste a block with known height, and apply the usual resize scale (e.g. r = 64%)
        3. scale the block with known height h so that it extends from below the title to the end of the page
        4. usable_column_height = h * scaling_factor
        5. real_title_height = column_height - usable_column_height
        """
        self.metrics = metrics
        self.column_height = column_height
        self.real_title_height = real_title_height
        self.block_separator_height = block_separator_height
        self.column_module = column_module
        self.empty_starting_columns = empty_starting_columns
        self.min_isolated_block_height = min_isolated_block_height
        self.columns_per_page = columns_per_page
        self.song_name_by_block = []
        self.song_by_block = []
        self.column_by_block = []
        self.block_height = []
        self.selected = []
        self.max_column = 0
        self.column_cap = None

    @classmethod
    def format_range(cls, first, last):
        return f"{first}" if first == last else f"{first}-{last}"

    @classmethod
    def print_solution_by_page(cls, solution):
        for d in solution:
            songs = ", ".join(
                f"{name} ({cls.format_range(first_block, last_block)})"
                for name, first_block, last_block in d['songs']
            )
            occupation = f"{d['occupation'] * 100:.1f}"
            print(f"{d['orig_column']:02d}. Page {d['page']}, Col {d['page_column']} {occupation}%: {songs}")

    def get_optimized_songs(self):
        out = []
        for song, selected in zip(self.metrics, self.selected):
            if selected:
                out.append(song)
        return out

    def get_solution_by_page(self, starting_page=1, starting_column=1):
        """
        Get structured solution

        Return list of dicts: {
            'orig_column': original (problem) column
            'page': page number (`starting_page`-based)
            'page_column': column number in page (1-based)
            'songs': list of tuples `(song_name, first_block, last_block)`
            'occupation': page occupation as %
        }
        """
        by_column = [defaultdict(int) for _ in range(self.max_column)]
        column_h = [0 for _ in range(self.max_column)]
        for b, c in enumerate(self.column_by_block):
            # print(f"Block {b}: column {c}")
            if self.selected[self.song_by_block[b] - 1]:
                by_column[c - 1][self.song_name_by_block[b]] += 1
                column_h[c - 1] += self.block_height[b] + self.block_separator_height

        page = starting_page
        column = starting_column
        n = len(by_column)
        out = []
        block_count_by_song = defaultdict(int)
        for c in range(n):
            h = column_h[c] - self.block_separator_height
            prev_songs = set(by_column[c - 1]) if c > 0 else set()
            cur = by_column[c]
            cur_songs = set(cur)
            next_songs = set(by_column[c + 1]) if c < n - 1 else set()
            first = prev_songs.intersection(cur_songs)
            last = next_songs.intersection(cur_songs)
            other = cur_songs - first.union(last)
            if len(last) > 0 and last == first:
                assert len(other) == 0
                last = set()
            seq = list(first) + list(other) + list(last)

            songs = []
            for song in seq:
                first_block = block_count_by_song[song] + 1
                if first_block == 1:
                    h += self.real_title_height

                block_count_by_song[song] += cur[song]
                last_block = block_count_by_song[song]
                songs.append((song, first_block, last_block))

            out.append({
                'orig_column': c + 1,
                'page': page,
                'page_column': column,
                'songs': songs,
                'occupation': h / self.column_height,
            })

            column += 1
            if column > self.columns_per_page:
                column = 1
                page += 1

        self.print_solution_by_page(out)
        return out

    async def _solve_async(self, instance, time_limit, processes):
        """Solve instance, printing intermediate solutions; return the best solution found, or None"""
        async for s in instance.solutions(
            timeout=time_limit,
            intermediate_solutions=True,
            processes=processes,
            free_search=True,
        ):
            logging.info(f"Status: {s.status}")
            print(s.status)
            if s.status != Status.SATISFIED:
                return
            try:
                s["column"]
            except KeyError:
                return
            self.column_by_block = s["column"]
            if self.column_cap:
                self.selected = s['selected']
                print(f"Objective: {s.objective}, blocks: {s['selected_blocks']}, songs: {s['selected_songs']}")
            else:
                self.max_column = s['max_column']
                print(f"Objective: {s.objective}, columns: {self.max_column}")

            self.get_solution_by_page()

    def optimize(
        self,
        column_cap=None,
        optimize_clean_columns=False,
        time_limit=timedelta(seconds=1000),
        processes=None
    ):
        """
        Optimize a set of songs

        If `column_cap` is not given, minimize columns, otherwise maximize songs fitting given number of columns
        """
        self.column_cap = column_cap
        if processes is None:
            processes = os.cpu_count()
        # solver = Solver.lookup('ortools')
        # driver = Driver(Path('../minizinc/MiniZincIDE-2.8.7-bundle-linux-x86_64/bin/minizinc'))
        driver = Driver(Path('C:\\Program Files\\MiniZinc\\minizinc.exe'))
        # driver = Driver(Path('../minizinc/MiniZincIDE-2.10.1-x86_64-linux-gnu/bin/minizinc'))
        solver = Solver.lookup('cp-sat', driver=driver)
        # solver = Solver.lookup('chuffed', driver=driver)
        model = Model(f'songpress/optimization/songpress_{"maxsongs" if column_cap else "minpages"}.mzn')
        instance = Instance(solver, model, driver)
        previous = []
        height = []
        # Map each song name to list of column indices
        self.song = defaultdict(list)

        column_height = scale(self.column_height + self.block_separator_height)
        min_isolated_block_height = scale(self.min_isolated_block_height)
        instance["column_height"] = column_height
        instance["column_module"] = self.column_module
        instance["empty_starting_columns"] = self.empty_starting_columns
        instance["min_isolated_block_height"] = min_isolated_block_height
        n_song = 0

        for filename, heights in self.metrics.items():
            n_song += 1
            for i, h in enumerate(heights):
                self.song_name_by_block.append(filename)
                self.song_by_block.append(n_song)
                self.block_height.append(h)
                h += self.block_separator_height
                if i == 0:
                    h += self.real_title_height
                    previous.append(0)
                else:
                    previous.append(len(height))
                height.append(scale(h))

        instance["n_blocks"] = len(height)
        instance["previous"] = previous
        instance["height"] = height
        instance["song"] = self.song_by_block
        instance["n_songs"] = n_song
        # Same (scaled) values passed to the model
        if column_cap:
            ub = column_cap
            self.max_column = ub
        else:
            self.selected = [True for _ in range(n_song)]
            ub = greedy_columns(
                previous,
                height,
                column_height,
                self.column_module,
                self.empty_starting_columns,
                min_isolated_block_height,
            )
            instance['optimize_clean_columns'] = optimize_clean_columns
            print(f"Upper bound on columns: {ub}")
        instance['ub'] = ub
        # pprint(self.song)

        try:
            s = asyncio.run(self._solve_async(instance, time_limit, processes))
        except Exception as e:
            logging.exception(f"Optimization Error: {e}")
        print(f"{len(self.song)} canzoni ottimizzate")


def previous_column_zero(column, column_module, empty_starting_columns):
    """
    Return the previous column (wrt `column`) that is `empty_starting_columns + 1` mod column_module
    """
    prev = column - 1
    diff = (prev - empty_starting_columns) % column_module
    return prev - diff


def batched_optimization(
    metrics,
    starting_page=1,
    column_height=COLUMN_HEIGHT,
    real_title_height=REAL_TITLE_HEIGHT,
    block_separator_height=BLOCK_SEPARATOR_HEIGHT,
    column_module=COLUMN_MODULE,
    columns_per_page=COLUMNS_PER_PAGE,
    empty_starting_columns=EMPTY_STARTING_COLUMNS,
    min_isolated_block_height=MIN_ISOLATED_BLOCK_HEIGHT,
    n_songs_batch=N_SONGS_BATCH,
    min_pages_timeout_seconds=MIN_PAGE_TIMEOUT_SECONDS,
    max_songs_timeout_seconds=MAX_SONGS_TIMEOUT_SECONDS,
):
    """
    Optimize a set of songs in batches.

    Iteratively alternate two steps:
    1. Randomly select `n_songs_batch` unoptimized songs
    2. Minimize pages
    3. Remove some pages (using `previous_column_zero`)
    4. Maximize songs in remaining pages
    :return:
    """
    out = []
    songs = set(metrics.keys())
    page = starting_page

    while len(songs) > 0:
        # Minimize pages
        chosen_songs = random.sample(list(songs), min(n_songs_batch, len(songs)))
        chosen_metrics = {s: metrics[s] for s in chosen_songs}

        is_last = len(songs) < n_songs_batch
        print(f"Minimizing pages, {len(songs)} songs, starting page: {page}")
        p_min = Problem(
            chosen_metrics,
            column_height,
            real_title_height,
            block_separator_height,
            column_module,
            columns_per_page,
            empty_starting_columns,
            min_isolated_block_height,
        )
        p_min.optimize(time_limit=timedelta(seconds=min_pages_timeout_seconds), optimize_clean_columns=is_last)
        column = previous_column_zero(
            p_min.max_column,
            column_module,
            empty_starting_columns,
        )

        if is_last:
            out.extend(p_min.get_solution_by_page(page))
            break

        # Maximize songs
        print(f"Maximizing songs, {len(songs)} songs, columns: {column} < {p_min.max_column}, starting page: {page}")
        p_max = Problem(
            chosen_metrics,
            column_height,
            real_title_height,
            block_separator_height,
            column_module,
            columns_per_page,
            empty_starting_columns,
            min_isolated_block_height,
        )
        p_max.optimize(column, time_limit=timedelta(seconds=max_songs_timeout_seconds))
        solution = p_max.get_solution_by_page(page)
        out.extend(solution)
        empty_starting_columns = 0
        page = solution[-1]['page'] + 1
        to_remove = p_max.get_optimized_songs()
        print(f"Discarded songs: {set(chosen_songs).difference(to_remove)}")
        songs.difference_update(to_remove)

    print("\n\nFinal Solution\n")
    Problem.print_solution_by_page(out)
    return out

