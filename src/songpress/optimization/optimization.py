from datetime import timedelta
from pathlib import Path
from pprint import pprint
import asyncio
import logging

from minizinc import Instance, Model, Solver, Driver

SCALE = 10

def scale(h):
    return int(round(SCALE * h))

async def _solve_async(instance):
    async for s in instance.solutions(
        timeout=timedelta(seconds=1000),
        intermediate_solutions=True,
        processes=4,
    ):
        logging.info(f"Status: {s.status}")
        try:
            pprint(s)
        except:
            logging.info("No assigned variable")
        logging.info(str(s))


def optimize(
    metrics,
    column_height=994,
    real_title_height=67,
    block_separator_height=29,
    column_module=4,
    empty_starting_columns=2,
    min_isolated_block_height=55,
):
    """
    Optimize a set of songs

    `metrics` is list of pairs `(filename, file_heights)` where 'file_heights` is the list
    of verse and chorus block heights.

    `column_height` is the overall height of the column. It can be found by pasting a song
    with a known height h, and scaling it to full height: apply the scaling factor to h.

    `block_separator_height` is the original distance between consecutive blocks. It can be found as:
    bsh = (song_height - sum_{i \in blocks}{block_height_i}) / (n_blocks - 1)

    `real_title_height` is the height of the real title that will be used in the publication, including
    the blank space to be left BELOW the title (and not above). It can be found in this way:
    1. align the title to the top of the column
    2. scale the block with known height h so that it extends from below the title to the end of the page
    3. usable_column_height = h * scaling_factor
    4. real_title_height = column_height - usable_column_height
    """
    # solver = Solver.lookup('ortools')
    driver = Driver(Path('../minizinc/MiniZincIDE-2.8.7-bundle-linux-x86_64/bin/minizinc'))
    solver = Solver.lookup('cp-sat', driver=driver)
    model = Model('songpress/optimization/songpress.mzn')
    instance = Instance(solver, model, driver)
    previous = []
    height = []
    # Map each block to song name
    song = []

    instance["column_height"] = scale(column_height + block_separator_height)
    instance["column_module"] = column_module
    instance["empty_starting_columns"] = empty_starting_columns
    instance["min_isolated_block_height"] = scale(min_isolated_block_height)

    for filename, heights in metrics:
        for i, h in enumerate(heights):
            song.append(filename)
            h += block_separator_height
            if i == 0:
                h += real_title_height
                previous.append(0)
            else:
                previous.append(len(height))
            height.append(scale(h))

    instance["n_blocks"] = len(height)
    instance["previous"] = previous
    instance["height"] = height


    try:
        asyncio.run(_solve_async(instance))
    except Exception as e:
        logging.exception(f"Optimization Error: {e}")



