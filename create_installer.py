import pynsis
from src import Globals
import sys
import os, os.path
import subprocess

license_template = "license.txt.tpl"
license_dest = "license.txt"
python2_command = 'python'


class cd:
	"""Context manager for changing the current working directory"""
	def __init__(self, newPath):
		self.newPath = os.path.expanduser(newPath)

	def __enter__(self):
		self.savedPath = os.getcwd()
		os.chdir(self.newPath)

	def __exit__(self, etype, value, traceback):
		os.chdir(self.savedPath)


def prepare_license():
	with open(license_template) as f:
		c = f.read()
	c = c.replace('{{Year}}', Globals.glb.YEAR)
	with open(license_dest, 'w') as f:
		f.write(c)


def create_installer():
	version = Globals.glb.VERSION
	with cd('src'):
		subprocess.call('%s setup.py build' % python2_command)
	prepare_license()
	pynsis.prepare_nsis_file(version)
	pynsis.call_nsis()
	

if __name__ == '__main__':
	create_installer()
