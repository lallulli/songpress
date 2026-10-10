from collections import defaultdict
from datetime import timedelta
from pathlib import Path
from pprint import pprint
import asyncio
import logging
import os

from minizinc import Instance, Model, Solver, Driver, Status

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
        return c % column_module == empty_starting_columns

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
        # column_height=994,
        column_height=1243,
        real_title_height=67,
        block_separator_height=29,
        column_module=4,
        columns_per_page=2,
        empty_starting_columns=2,
        min_isolated_block_height=55,
    ):
        self.metrics = metrics
        self.column_height = column_height
        self.real_title_height = real_title_height
        self.block_separator_height = block_separator_height
        self.column_module = column_module
        self.empty_starting_columns = empty_starting_columns
        self.min_isolated_block_height = min_isolated_block_height
        self.columns_per_page = columns_per_page
        self.song_by_column = []
        self.column_by_block = []
        self.max_column = 0

    def format_range(self, first, last):
        return f"{first}" if first == last else f"{first}-{last}"

    def print_solution_by_page(self, solution):
        for d in solution:
            songs = ", ".join(
                f"{name} ({self.format_range(first_block, last_block)})"
                for name, first_block, last_block in d['songs']
            )
            print(f"{d['orig_column']:02d}. Page {d['page']}, Col {d['page_column']}: {songs}")

    def get_solution_by_page(self, starting_page=1, starting_column=1):
        by_column = [defaultdict(int) for _ in range(self.max_column)]
        for b, c in enumerate(self.column_by_block):
            # print(f"Block {b}: column {c}")
            by_column[c - 1][self.song_by_column[b]] += 1

        page = starting_page
        column = starting_column
        n = len(by_column)
        out = []
        block_count_by_song = defaultdict(int)
        for c in range(n):
            prev_songs = set(by_column[c - 1]) if c > 0 else set()
            cur = by_column[c]
            cur_songs = set(cur)
            next_songs = set(by_column[c + 1]) if c < n - 1 else set()
            first = prev_songs.intersection(cur_songs)
            last = next_songs.intersection(cur_songs)
            other = cur_songs - first.union(last)
            seq = list(first) + list(other) + list(last)

            songs = []
            for song in seq:
                first_block = block_count_by_song[song] + 1
                block_count_by_song[song] += cur[song]
                last_block = block_count_by_song[song]
                songs.append((song, first_block, last_block))

            out.append({
                'orig_column': c + 1,
                'page': page,
                'page_column': column,
                'songs':songs,
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
            self.column_by_block = s["column"]
            self.max_column = s['max_column']
            self.get_solution_by_page()
            print(f"Objective: {s.objective}, columns: {self.max_column}")

    def optimize(self, time_limit=timedelta(seconds=1000), restarts=1, processes=None, random_seed=0):
        """
        Optimize a set of songs

        `metrics` is list of pairs `(filename, file_heights)` where 'file_heights` is the list
        of verse and chorus block heights.

        `column_height` is the overall height of the column. It can be found by pasting a song
        with a known height h, and scaling it to full height: apply the scaling factor to h.

        `block_separator_height` is the original distance between consecutive blocks. It can be found as:
        bsh = (song_height - sum_{i in blocks}{block_height_i}) / (n_blocks - 1)

        `real_title_height` is the height of the real title that will be used in the publication, including
        the blank space to be left BELOW the title (and not above). It can be found in this way:
        1. align the title to the top of the column
        2. scale the block with known height h so that it extends from below the title to the end of the page
        3. usable_column_height = h * scaling_factor
        4. real_title_height = column_height - usable_column_height

        The solver is run `restarts` times, each one with a different random seed (starting from
        `random_seed`) and with a timeout of `time_limit`; the best solution is kept. Several short runs
        often work better than a single long one, since a run can get stuck in a local optimum.

        `processes` is the number of solver threads (default: number of CPUs).
        """
        if processes is None:
            processes = os.cpu_count()
        # solver = Solver.lookup('ortools')
        driver = Driver(Path('../minizinc/MiniZincIDE-2.8.7-bundle-linux-x86_64/bin/minizinc'))
        # driver = Driver(Path('../minizinc/MiniZincIDE-2.10.1-x86_64-linux-gnu/bin/minizinc'))
        solver = Solver.lookup('cp-sat', driver=driver)
        # solver = Solver.lookup('chuffed', driver=driver)
        model = Model('songpress/optimization/songpress.mzn')
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
        song = []
        n_song = 0

        for filename, heights in self.metrics:
            n_song += 1
            for i, h in enumerate(heights):
                self.song_by_column.append(filename)
                h += self.block_separator_height
                if i == 0:
                    h += self.real_title_height
                    previous.append(0)
                else:
                    previous.append(len(height))
                height.append(scale(h))
                song.append(n_song)

        instance["n_blocks"] = len(height)
        instance["previous"] = previous
        instance["height"] = height
        instance["song"] = song
        instance["n_songs"] = n_song
        # Same (scaled) values passed to the model
        ub = greedy_columns(
            previous,
            height,
            column_height,
            self.column_module,
            self.empty_starting_columns,
            min_isolated_block_height,
        )
        print(f"Upper bound on columns: {ub}")
        instance['ub'] = ub
        # pprint(self.song)

        try:
            s = asyncio.run(self._solve_async(instance, time_limit, processes))
        except Exception as e:
            logging.exception(f"Optimization Error: {e}")
        print(f"{len(self.song)} canzoni ottimizzate")
