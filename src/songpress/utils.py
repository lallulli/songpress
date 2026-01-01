from contextlib import contextmanager
import tempfile
import logging
import shutil


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
