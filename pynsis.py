import os
import os.path
import shutil
import subprocess
#from optparse import OptionParser

dir = "src\\build\\exe.win32-3.8"
source = "installer\\songpress.nsi.tpl"
dest = "songpress.nsi"
nsis_path = r"C:\Program Files (x86)\NSIS\makensis.exe"

def get_files(dir):
	inst = ""
	funinst = ""
	duninst = ""
	n = len(dir)
	for dirpath, dirnames, filenames in os.walk(dir):
		inst += "  SetOutPath \"$INSTDIR%s\"\n" % dirpath[n:]
		duninst = ("  RMDir \"$INSTDIR%s\"\n" % dirpath[n:]) + duninst
		for f in filenames:
			inst += "  File \"%s\"\n" % os.path.join(dirpath, f)
			funinst += "  Delete \"$INSTDIR%s\%s\"\n" % (dirpath[n:], f)
	return inst, funinst + duninst


def prepare_nsis_file(version):
	inst, uninst = get_files(dir)
	r = open(source)
	c = r.read()
	r.close()
	c = c.replace('{{Installation}}', inst)
	c = c.replace('{{UnInstallation}}', uninst)
	c = c.replace('{{Version}}', version)
	
	w = open(dest, 'w')
	w.write(c)
	w.close()


def dedup_dll_ric(path, dlls):
	d = os.listdir(path)
	for n in d:
		n_path = os.path.join(path, n)
		if n in dlls:
			os.remove(n_path)
		elif os.path.isdir(n_path):
			dedup_dll_ric(n_path, dlls)


def dedup_dll():
	d = os.listdir(dir)
	dlls = set([f for f in d if f.upper().endswith('.DLL')])
	for n in d:
		n_path = os.path.join(dir, n)
		if os.path.isdir(n_path):
			dedup_dll_ric(n_path, dlls)


def call_nsis():
	subprocess.call("%s %s" % (nsis_path, dest))
	
	
if __name__ == '__main__':
	from src import Globals
	prepare_nsis_file(Globals.glb.VERSION)
	dedup_dll()
	call_nsis()

	