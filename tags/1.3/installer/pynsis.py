import os
import os.path
import shutil
#from optparse import OptionParser

dir = "..\\src\\dist"
source = "songpress.nsi.tpl"
dest = "songpress.nsi"

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

if __name__ == '__main__':
	inst, uninst = get_files(dir)
	r = open(source)
	c = r.read()
	r.close()
	c = c.replace('{{Installation}}', inst)
	c = c.replace('{{UnInstallation}}', uninst)
	w = open(dest, 'w')
	w.write(c)
	w.close()
