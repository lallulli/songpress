import os
import os.path
import shutil
from optparse import OptionParser

def createDirAndGo(path, dir):
	final = os.path.join(path, dir)
	if not os.path.isdir(final) and not os.path.isfile(final):
		os.mkdir(final)
	return final

def execute(path, xrc=False, lang=[]):
	print path
	d = os.listdir(path)
	created = []
	for f in d:
		fp = os.path.join(path, f)
		if os.path.isfile(fp):
			n, e = os.path.splitext(f)
			if xrc and e == '.xrc':
				newfp = os.path.join(path, n + '.pos')
				wx.tools.pywxrc.main(['', '-g', '-o', newfp, fp])
				fp = newfp
			if e == '.py' or (xrc and e == '.xrc'):
				pot = os.path.join(path, n + '.pot')
				s = 'xgettext -L python "%s" -o "%s"' % (fp, pot)
				print s
				os.system(s)
				if os.path.isfile(pot):
					created.append(n + ".pot")
		else:
			execute(fp, xrc, lang)
	if len(lang)>0 and len(created)>0:
		p = createDirAndGo(path, 'locale')
		for l in lang:
			pl = createDirAndGo(p, l)
			pl = createDirAndGo(pl, 'LC_MESSAGES')
			for f in created:
				n, e = os.path.splitext(f)
				fn = os.path.join(pl, n + ".po")
				fo = os.path.join(path, f)
				if os.path.isfile(fn):
					s = 'msgmerge -U "%s" "%s"' % (fn, fo)
					print s
					os.system(s)
				else:
					shutil.copy(fo, fn)

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-d", "--dir", dest="dir",
										help="directory to process")
	parser.add_option("-l", "--languages", dest="lang",
										help="comma-separated list of languages to handle (init, merge)")
	parser.add_option("-x", "--xrc",
										action="store_true", dest="xrc", default=False,
										help="process xrc files (wxWidgets required)")

	(options, args) = parser.parse_args()
	if options.xrc:
		import wx.tools.pywxrc
	if options.lang != None:
		lang = options.lang.split(',')
	else:
		lang = []
	if options.dir == None:
		path = os.path.abspath(os.curdir)
	else:
		path = options.dir
	execute(path, options.xrc, lang)
