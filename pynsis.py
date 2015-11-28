import os
import os.path
import shutil
import subprocess
#from optparse import OptionParser

dir = "src\\build\\exe.win32-2.7"
source = "installer\\songpress.nsi.tpl"
dest = "songpress.nsi"
nsis_path = "C:\\Programmi\\nsis\\makensis.exe"

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


def call_nsis():
	subprocess.call("%s %s" % (nsis_path, dest))
	
	
if __name__ == '__main__':
	from src import Globals
	prepare_nsis_file(Globals.glb.VERSION)
	call_nsis()

	