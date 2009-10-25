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
import BeautifulSoup
import urllib2
import urlparse
import tempfile
import os

class Repository(object):
	def __init__(self):
		object.__init__(self)
		self.i = 1
		self.d = {}
		
	def __getitem__(self, s):
		if s not in self.d:
			p, e = os.path.splitext(s)
			self.d[s] = str(self.i) + e
			self.i += 1
		return self.d[s]

class Grabber(object):
	def __init__(self, tree, project):
		object.__init__(self)
		self.tree = tree
		self.project = project
		
	def Load(self, url, text=None):
		fn = os.path.join(self.dir, self.repo[url])
		if text is None:
			s = urllib2.urlopen(url)
			text = s.read()
			s.close()
		f = open(fn, "w")
		f.write(text)
		f.close()
		
	def TransformUrl(self, baseurl, node, attrib, load=False):
		url = node[attrib]
		if url[:7].lower() == "http://":
			return
		url = urlparse.urljoin(baseurl, url)
		node[attrib] = self.repo[url]
		if load:
			self.Load(url)		
		
	def Grab(self, item):
		t, u = glb.Split(self.tree.GetItemText(item))
		s = urllib2.urlopen(u)
		raw = s.read()
		s.close()
		soup = BeautifulSoup.BeautifulSoup(raw)
		title = self.extractTitle(soup.html)
		self.tree.SetItemText(item, glb.Join(title, u))
		content = self.extractContent(soup.html)
		if type(content) != list and type(content) != BeautifulSoup.ResultSet:
			content = [content]
		a = []
		img = []
		for el in content:
			a += el.findAll('a')
			img += el.findAll('img')
		for el in a:
			self.TransformUrl(u, el, 'href')
		for el in img:
			self.TransformUrl(u, el, 'src', True)
		c = "".join([str(x) for x in content])
		t = self.template.replace('[*Title*]', t)
		text = t.replace('[*Content*]', c)
		self.Load(u, text)
		# recurse on children
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

		# create temp dir and repository
		self.dir = tempfile.mkdtemp()
		self.repo = Repository()
		
		# load template
		f = open(self.project.template)
		self.template = f.read()
		f.close()
		
		# traverse tree and get documents
		self.GrabChildren(self.tree.GetRootItem())
		
		# delete temp dir
		print self.dir
		"""
		for root, dirs, files in os.walk(self.dir, topdown=False):
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))
		"""
		
	
