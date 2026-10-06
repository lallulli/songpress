"""
Provide a special "get metrics" mode that return the height of every song block of every song

This mode can be used for optimizing the layout of songs in a multipage songbook
"""

import os

from minizinc import Instance, Model, Solver
from songpress.SongFormat import SongFormat
from songpress.Renderer import Renderer
import wx


def get_song_metrics(file_or_dir_name: str, song_format: SongFormat):
    """
    Return blocks heights of a single or multiple files

    Return a list of pairs `(filename, file_heights)` where  'file_heights` is the list
    of verse and chorus block heights.

    If `file_or_dir_name` is not a chordpro file or a directory, return `None`
    """
    if os.path.isdir(file_or_dir_name):
        out = []
        for f in os.listdir(file_or_dir_name):
            res = get_song_metrics(os.path.join(file_or_dir_name, f), song_format)
            if res is not None:
                out.extend(res)
        return out

    if not file_or_dir_name.endswith('.crd'):
        return

    with open(file_or_dir_name) as f:
        text = f.read()

    r = Renderer(song_format)
    dc = wx.MemoryDC(wx.Bitmap(1, 1))
    r.Render(text, dc)
    return [(os.path.basename(file_or_dir_name), r.GetBlockHeights())]


