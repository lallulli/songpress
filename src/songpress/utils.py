from contextlib import contextmanager
import tempfile
import logging
import shutil

import wx.stc


@contextmanager
def temp_dir(keep=False):
    """
    Context manager. Create and yield a temporary dir, and destroys it on exit
    """
    t = tempfile.mkdtemp()
    try:
        yield t
    finally:
        if keep:
            logging.info(f"Keeping temporary folder: {t}")
        else:
            shutil.rmtree(t)


@contextmanager
def undo_action(text: wx.stc.StyledTextCtrl):
    """
    Context manager. Handle an atomic undo operation on a StyledTextCtrl
    """
    text.BeginUndoAction()
    try:
        yield
    finally:
        text.EndUndoAction()
