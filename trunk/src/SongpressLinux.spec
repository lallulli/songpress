# -*- mode: python -*-
"""
	How to compile:
	cd to the directory of this file (i.e., src)
	delete 'dist' subdir, if it exists
	python <PathToPyInstaller>\Build.py Songpress.spec
"""

import os, os.path

def include_all(path, file):
	return True
	
def exclude_nothing(path, file):
	return False	

def my_tree(path, include=include_all, exclude=exclude_nothing):
	out = []
	for dirpath, dirnames, filenames in os.walk(path):
		for n in filenames:
			if include(dirpath, n) and not exclude(dirpath, n):
				f = os.path.join(dirpath, n)
				out.append((f, f, 'DATA'))
	return out
	
def exclude_svn(path, file):
	return path.find('.svn') != -1

def include_ext(extlist):
	def include_ext_int(path, file):
		f, ext = os.path.splitext(file)
		return ext in extlist
	return include_ext_int


a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), os.path.join(HOMEPATH,'support/useUnicode.py'), 'main.py'],
             pathex=['.'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.linux2/SongpressLinux', 'songpress'),
          debug=False,
          strip=True,
          upx=True,
          console=0 )
coll = COLLECT( exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               my_tree('img', exclude=exclude_svn),
               my_tree('help', exclude=exclude_svn),
               my_tree('locale', include_ext(['.mo']), exclude_svn),
               my_tree('xrc', include_ext(['.mo', '.xrc']), exclude_svn),
               strip=True,
               upx=True,
               name=os.path.join('dist', 'songpress'),
              )
#app = BUNDLE(coll,
#             name=os.path.join('dist', 'Songpress.app'))
