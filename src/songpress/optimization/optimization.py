from datetime import timedelta
from pathlib import Path
from pprint import pprint
import asyncio
import logging

from minizinc import Instance, Model, Solver, Driver

SCALE = 10


async def _solve_async(instance):
    async for s in instance.solutions(
        timeout=timedelta(seconds=100),
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
    column_height,
    title_height,
    block_separator_height,
    metrics,
    column_module=4,
    empty_starting_columns=2,
):
    """
    Optimize a set of songs.

    `metrics` is list of pairs `(filename, file_heights)` where 'file_heights` is the list
    of verse and chorus block heights.
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

    instance["column_height"] = int(round(SCALE * (column_height + block_separator_height)))
    instance["column_module"] = column_module
    instance["empty_starting_columns"] = empty_starting_columns

    for filename, heights in metrics:
        for i, h in enumerate(heights):
            song.append(filename)
            h += block_separator_height
            if i == 0:
                h += title_height
                previous.append(0)
            else:
                previous.append(len(height))
            height.append(int(round(SCALE * h)))

    instance["n_blocks"] = len(height)
    instance["previous"] = previous
    instance["height"] = height


    try:
        asyncio.run(_solve_async(instance))
    except Exception as e:
        logging.exception(f"Optimization Error: {e}")



