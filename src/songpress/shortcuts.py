from pyshortcuts import make_shortcut
from pathlib import Path
import sys
import os


def get_executable_path():
    exe = Path(sys.argv[0]).resolve()
    return str(exe)


def get_current_dir():
    return os.path.dirname(os.path.abspath(__file__))


def create_shortcuts():
    icon = os.path.join(get_current_dir(), 'img/songpress.ico')
    print("Icon: ", icon)
    make_shortcut(
        get_executable_path(),
        "Songpress",
        icon=icon,
        desktop=False,
        noexe=True,
    )
