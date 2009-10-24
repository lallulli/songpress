###############################################################
# Name:			 Grabber.py
# Purpose:	 Grab html files and compiles them into chm
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-08-24
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

from Globals import *
from Project import *
from BeautifulSoup import BeautifulSoup
import urllib2

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

class Grabber(object):
	def __init__(self, tree, project):
		object.__init__(self)
		self.tree = tree
		self.project = project
		
	def Grab(self, item):
		t, u = glb.Split(self.tree.GetItemText(item))
		s = urllib2.urlopen(u)
		raw = s.read()
		s.close()
		print raw
		soup = BeautifulSoup(raw)
		title = self.extractTitle(soup.html)
		content = self.extractContent(soup.html)
		print title
		
		self.GrabChildren(item)
		
	def GrabChildren(self, item):
		el, cookie = self.tree.GetFirstChild(item)
		while el.IsOk():
			pos = self.Grab(el)
			el, cookie = self.tree.GetNextChild(item, cookie)
		
	def Compile(self):
		# define extracting methods
		m = "def extractTitle(html):\n"
		for l in self.project.extractTitle.splitlines():
			m += "\t" + l + "\n"
		exec m
		self.extractTitle = extractTitle
		
		m = "def extractContent(html):\n"
		for l in self.project.extractContent.splitlines():
			m += "\t" + l + "\n"
		exec m
		self.extractContent = extractContent

		self.repo = Repository()
	
		self.GrabChildren(self.tree.GetRootItem())
	
