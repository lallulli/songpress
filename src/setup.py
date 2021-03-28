# coding: utf-8

import sys
from cx_Freeze import setup, Executable
import os, os.path
import platform

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}


# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"


def _get_files(d):
	out = []
	parent, nd = os.path.split(d)
	n = len(parent)
	for dirpath, dirnames, filenames in os.walk(d):
		base = dirpath[n:]
		for f in filenames:
			out.append(os.path.join(base, f))
	return out


def get_files(dirs):
	"""
	Get list of file paths included in dirs.

	dirs is a list of paths.

	Returned paths are relative to dir's parent
	"""
	out = []
	for d in dirs:
		out.extend(_get_files(d))
	return out


include_files = [(x, x) for x in get_files(['help', 'img', 'locale', 'templates', 'xrc'])]


options = {
	'build_exe': {
		'include_files': include_files,
		'include_msvcr': True,
		'packages': ["multiprocessing", "idna.idnadata", "ssl"],
		'excludes': ["numpy", "tkinter"],
	}
}

# Workaround for cx_Freeze issue for requests
# https://github.com/anthony-tuininga/cx_Freeze/issues/437
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
if sys.platform == "win32":
	options["build_exe"]['include_files'].extend([
		os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'libcrypto-1_1.dll'),
		os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'libssl-1_1.dll'),
	])

def build(version):
	setup(
		name="Songpress",
		version=version,
		description="Songpress - Il Canzonatore",
		options=options,
		executables=[Executable(
			"main.py",
			base=base,
			target_name='Songpress' if platform.system() == 'Linux' else "Songpress.exe",
			icon='img/songpress.ico',
		)]
	)


if __name__ == '__main__':
	import Globals
	build(Globals.glb.VERSION)



