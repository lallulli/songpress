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
#import xml.etree.ElementTree as ET
import wx
import wx.lib.newevent
import threading
import traceback
from genshi.template import TemplateLoader
from genshi.builder import tag

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
			
	def __in__(self, k):
		return k in self.d
		
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
			if not os.path.isfile(os.path.join(self.tpldir, url)):
				s = urllib2.urlopen(url)
			else:
				s = open(os.path.join(self.tpldir, url), "rb")
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
		if url[:7].lower() == "http://" and url not in self.repo:
			return
		if not os.path.isfile(os.path.join(self.tpldir, url)):
			url = urlparse.urljoin(baseurl, url)
		node[attrib] = self.repo[url]
		if load:
			self.Load(url)
	
	def InsertIntoRepository(self):
		for k in self.treeList:
			self.repo.SetItemWithExt(k[1], '.htm')
		
	def GetPrevItem(self, item):
		prev = self.tree.GetPrevItem(item)
		if item.IsOk():
			return prev.GetItemUrl()
		parent = self.tree.GetItemParent(item)
		if parent != self.tree.GetRootItem():
			prev = self.tree.GetNextItem(item)
			if item.IsOk():
				return next.GetItemUrl()
		return False		
		
	def Grab(self):
		i = 0
		nn = len(self.treeList)
		for k in self.treeList:
			# grab page and extract content
			u = k[1]
			self.Send("Grabbing %s" % (u,))
			s = urllib2.urlopen(u)
			raw = s.read()
			s.close()
			soup = BeautifulSoup.BeautifulSoup(raw)
			title = self.extractTitle(soup.html)
			self.tree.SetItemText(k[0], glb.Join(title, u))
			content = self.extractContent(soup.html)
			if type(content) != list and type(content) != BeautifulSoup.ResultSet:
				content = [content]
			c = "".join([str(x) for x in content])
			next = self.treeList[i + 1][1] if i + 1 < nn else False
			prev = self.treeList[i - 1][1] if i - 1 >= 0 else False
			parent = k[2] if k[2] != "" else False
			# apply template
			text = self.tpl.generate(title=title, content=c, next=next, prev=prev, parent=parent).render('html')
			# re-parse generated html, and "normalize" urls
			soup = BeautifulSoup.BeautifulSoup(text)
			a = soup.findAll('a')
			img = soup.findAll('img')
			for el in a:
				self.TransformUrl(u, el, 'href')
			for el in img:
				self.TransformUrl(u, el, 'src', True)
			self.Load(u, soup.renderContents())
			i += 1

		
	def GenerateTocItem(self, item, e):
		t, u = glb.Split(self.tree.GetItemText(item))
		li = tag.li
		e.append(li)
		object = tag.object(type='text/sitemap')
		li.append(object)
		object.append(tag.param(name="Name", value=t))
		object.append(tag.param(name="Local", value=self.repo[u]))
		object.append(tag.param(name="ImageNumber", value='0'))
		if self.tree.ItemHasChildren(item):
			ul = tag.ul
			li.append(ul)
			self.DoWithChildren(
				item,
				lambda i: self.GenerateTocItem(i, ul)
			)
			
	def GenerateTreeList(self, item):
		t, u = glb.Split(self.tree.GetItemText(item))
		p = self.tree.GetItemParent(item)
		if p != self.tree.GetRootItem():
			pt, pu = glb.Split(self.tree.GetItemText(p))
		else:
			pu = ""
		self.treeList.append((item, u, pu))
		if self.tree.ItemHasChildren(item):
			self.DoWithChildren(
				item,
				self.GenerateTreeList
			)

	def DoWithChildren(self, item, what):
		el, cookie = self.tree.GetFirstChild(item)
		while el.IsOk():
			self.CheckStop()
			pos = what(el)
			el, cookie = self.tree.GetNextChild(item, cookie)
			
	def GenerateToc(self):
		self.tocFile = os.path.join(self.dir, "toc.hhc")
		loader = TemplateLoader('.')
		toctpl = loader.load(glb.AddPath('toc-template.hhc'))
		ul = tag.ul
		self.DoWithChildren(
			self.tree.GetRootItem(),
			lambda i: self.GenerateTocItem(i, ul)
		)
		f = open(self.tocFile, "w")
		f.write(toctpl.generate(list=ul).render('html'))
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
		for k in self.treeList:
			f.write(self.repo[k[1]] + "\n")
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
			self.tpldir, f = os.path.split(self.project.template)
						
			# generate tree list
			self.treeList = []
			self.DoWithChildren(self.tree.GetRootItem(), self.GenerateTreeList)
			
			# insert urls into repository
			self.InsertIntoRepository()
			
			# grab documents
			self.Grab()
			
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
			msg = "\nERROR:\n" + traceback.format_exc()
			#msg = "\nERROR:\n" + str(ex)
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
	
