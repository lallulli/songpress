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
import xml.etree.ElementTree as ET

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
		
	def SetItemWithExt(self, s, ext):
		if s not in self.d:
			self.d[s] = str(self.i) + ext
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
		f = open(fn, "wb")
		f.write(text)
		f.close()
	
	def TransformUrl(self, baseurl, node, attrib, load=False):
		try:
			url = node[attrib]
		except:
			return
		if url[:7].lower() == "http://":
			return
		url = urlparse.urljoin(baseurl, url)
		node[attrib] = self.repo[url]
		if load:
			self.Load(url)		
	
	def InsertIntoRepository(self, item):
		t, u = glb.Split(self.tree.GetItemText(item))
		self.repo.SetItemWithExt(u, '.htm')
		self.DoWithChildren(item, self.InsertIntoRepository)
		
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
		self.DoWithChildren(item, self.Grab)
		
	def GenerateTocItem(self, item, e):
		t, u = glb.Split(self.tree.GetItemText(item))
		li = ET.SubElement(e, 'li')
		object = ET.SubElement(li, 'object')
		object.set('type', 'text/sitemap')
		param = ET.SubElement(object, 'param')
		param.set('name', t)
		param.set('Local', self.repo[u])
		param.set('ImageNumber', '0')
		if self.tree.ItemHasChildren(item):
			ul = ET.SubElement(li, 'ul')
			self.DoWithChildren(
				item,
				lambda i: self.GenerateTocItem(i, ul)
			)

	def DoWithChildren(self, item, what):
		el, cookie = self.tree.GetFirstChild(item)
		while el.IsOk():
			pos = what(el)
			el, cookie = self.tree.GetNextChild(item, cookie)
			
	def GenerateToc(self):
		fn = os.path.join(self.dir, "toc.hhc")
		html = ET.Element('html')
		ET.SubElement(html, 'head')
		body = ET.SubElement(html, 'body')
		object = ET.SubElement(body, 'object')
		object.set('type', 'text/site properties')
		param = ET.SubElement(object, 'param')
		param.set('name', 'ExWindow Styles')
		param.set('value', '0x800225')
		param = ET.SubElement(object, 'param')
		param.set('name', 'Window Styles')
		param.set('value', '0x800225')
		ul = ET.SubElement(body, 'ul')
		self.DoWithChildren(
			self.tree.GetRootItem(),
			lambda i: self.GenerateTocItem(i, ul)
		)
		f = open(fn, "w")
		f.write('<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">\n')
		t = ET.ElementTree(html)
		t.write(f)
		f.close()
		
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
		
		# traverse tree and insert urls into repository
		self.DoWithChildren(self.tree.GetRootItem(), self.InsertIntoRepository)
		
		# traverse tree and get documents
		self.DoWithChildren(self.tree.GetRootItem(), self.Grab)
		
		self.GenerateToc()
		
		# delete temp dir
		print self.dir
		"""
		for root, dirs, files in os.walk(self.dir, topdown=False):
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))
		"""
		
	
