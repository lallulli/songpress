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
import os.path
import subprocess
import xml.etree.ElementTree as ET
import wx
import wx.lib.newevent
import threading
import traceback
from genshi.template import TemplateLoader

EventTextMessage, EVT_TEXT_MESSAGE = wx.lib.newevent.NewEvent()
EventCompleted, EVT_COMPLETED = wx.lib.newevent.NewEvent()


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
		
	def __iter__(self):
		for k in self.d:
			yield k
		
class Grabber(threading.Thread):
	def __init__(self, tree, project, owner):
		threading.Thread.__init__(self)
		self.tree = tree
		self.project = project
		self.owner = owner
		self.stop = False
		
	def Send(self, msg):
		evt = EventTextMessage(message=msg)
		wx.PostEvent(self.owner, evt)		

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
		self.Send("Grabbing %s" % (u,))
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
		text = self.tpl.generate(title=t, content=c).render('html')
		self.Load(u, text)
		# recurse on children
		self.DoWithChildren(item, self.Grab)
		
	def GenerateTocItem(self, item, e):
		t, u = glb.Split(self.tree.GetItemText(item))
		li = ET.SubElement(e, 'li')
		object = ET.SubElement(li, 'object')
		object.set('type', 'text/sitemap')
		param = ET.SubElement(object, 'param', name="Name", value=t)
		param = ET.SubElement(object, 'param', name='Local', value=self.repo[u])
		param = ET.SubElement(object, 'param', name='ImageNumber', value='0')
		if self.tree.ItemHasChildren(item):
			ul = ET.SubElement(li, 'ul')
			self.DoWithChildren(
				item,
				lambda i: self.GenerateTocItem(i, ul)
			)

	def GenerateProjectItem(self, item, f):
		t, u = glb.Split(self.tree.GetItemText(item))
		f.write(self.repo[u] + "\n")
		if self.tree.ItemHasChildren(item):
			self.DoWithChildren(
				item,
				lambda i: self.GenerateProjectItem(i, f)
			)

	def DoWithChildren(self, item, what):
		el, cookie = self.tree.GetFirstChild(item)
		while el.IsOk():
			self.CheckStop()
			pos = what(el)
			el, cookie = self.tree.GetNextChild(item, cookie)
			
	def GenerateToc(self):
		self.tocFile = os.path.join(self.dir, "toc.hhc")
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
		f = open(self.tocFile, "w")
		f.write('<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">\n')
		t = ET.ElementTree(html)
		t.write(f)
		f.close()
		
	def GenerateProjectFile(self):
		self.projFile = os.path.join(self.dir, "project.hhp")
		f = open(self.projFile, "w")
		i = """[OPTIONS]
Language=0x409 English (United States)
Default Font=Arial,8,0
Title=%s
Full-text search=Yes
Compatibility=1.1
Auto Index=Yes
Compiled file=%s.chm
Contents file=toc.hhc

[FILES]
""" % (
			self.project.name,
			self.project.name
		)
		f.write(i)
		self.DoWithChildren(
			self.tree.GetRootItem(),
			lambda i: self.GenerateProjectItem(i, f)
		)
		f.close()		
		
	def Compile(self):
		try:
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
			loader = TemplateLoader('.')
			self.tpl = loader.load(self.project.template)
			
			# traverse tree and insert urls into repository
			self.DoWithChildren(self.tree.GetRootItem(), self.InsertIntoRepository)
			
			# traverse tree and get documents
			self.DoWithChildren(self.tree.GetRootItem(), self.Grab)
			
			# generate project files
			self.GenerateToc()
			self.GenerateProjectFile()
			
			# launch help compiler
			self.Send("\nLaunching MS Help Compiler...")
			hc = os.path.join(os.environ['PROGRAMFILES'], "HTML Help Workshop\\hhc.exe")
			os.chdir(self.dir)
			proc = subprocess.Popen(("%s project.hhp" % (hc,)), stdout=subprocess.PIPE)
			for l in proc.stdout:
				self.CheckStop()
				self.Send(l.strip("\n"))
			
			# delete temp dir
			print self.dir
			"""
			for root, dirs, files in os.walk(self.dir, topdown=False):
				for name in files:
					os.remove(os.path.join(root, name))
				for name in dirs:
					os.rmdir(os.path.join(root, name))
			"""
		except Exception, ex:
			#msg = "\nERROR:\n" + traceback.format_exc()
			msg = "\nERROR:\n" + str(ex)
			self.Send(msg)
	
	def Stop(self):
		self.stop = True
		
	def CheckStop(self):
		if self.stop:
			raise Exception("Stopped")
		
	def run(self):
		self.Compile()
		evt = EventCompleted()
		wx.PostEvent(self.owner, evt)		
	
