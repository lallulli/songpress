from BeautifulSoup import BeautifulSoup
import os
import os.path
import shutil
import sys
from optparse import OptionParser

class Repository(object):
	def __init__(self):
		object.__init__(self)
		self.i = 1
		self.d = {}
		
	def __getitem__(self, s):
		if s not in self.d:
			p, e = os.path.splitext(f)
			self.d[s] = str(i) + e
			i += 1
		return self.d[s]
		
def initProject():
	tpath = os.path.join(prgpath, 'template')
	if not os.path.isdir(path):
		os.mkdir(path)
	d = os.listdir(tpath)
	for f in d:
		shutil.copy(os.path.join(tpath, f), path)
		
def compileProject():
	rep = Repository()
	
	
if __name__ == '__main__':
	prgpath = os.path.abspath(os.path.dirname(sys.argv[0]))

	parser = OptionParser()
	parser.add_option("-d", "--dir", dest="dir",
										help="directory to process")
	parser.add_option("-i", "--init",
										action="store_true", dest="init", default=False,
										help="prepare directory structure")
	(options, args) = parser.parse_args()
	if options.dir == None:
		path = os.path.abspath(os.curdir)
	else:
		path = options.dir
	if options.init:
		initProject()
	else:
		compileProject()
	