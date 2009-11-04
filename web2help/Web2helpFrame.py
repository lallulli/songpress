###############################################################
# Name:			 Web2helpFrame.py
# Purpose:	 Main frame for web2help
# Author:		 Luca Allulli (luca@skeed.it)
# Created:	 2009-01-16
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import wx
import wx.stc
from wx import xrc
from SDIMainFrame import *
from Globals import glb
from MyProperties import *
from Project import *
from Grabber import *
import xml.etree.ElementTree as ET

class Web2helpFrame(SDIMainFrame):

	def __init__(self, res):
		SDIMainFrame.__init__(
			self,
			res,
			'MainFrame',
			'web2help',
			'Skeed',
			'project',
			'w2h',
			'web2help',
			glb.AddPath('img/web2help.ico'),
			"0.9",
			"http://www.skeed.it/web2help.html",
			"Copyright (c) 2009 Luca Allulli - Skeed",
			"Licensed under the terms and conditions of the GNU General Public License, version 2",
			"Special thanks to:\n  * The Pyhton programming language (http://www.python.org)\n  * wxWidgets (http://www.wxwidgets.org)\n  * wxPython (http://www.wxpython.org)"
		)
		
		# Menu
		self.BindMyMenu()

		# Splitter creation
		self.splitter = wx.SplitterWindow(self.frame);

		# Tree
		self.imageList = wx.ImageList(16, 16)
		self.pageIcon = self.imageList.Add(wx.Bitmap(glb.AddPath('img/page.png')))		
		self.bookIcon = self.imageList.Add(wx.Bitmap(glb.AddPath('img/book.png')))		
		self.tree = wx.TreeCtrl(self.splitter)
		self.tree.SetImageList(self.imageList)
		self.New()
		self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnTreeItemRightClick)
		
		self.NEW = 1
		self.EDIT = 2
		self.DELETE = 3
		self.MOVE_UP = 4
		self.MOVE_DOWN = 5
		
		# Tree Menu
		self.menu = wx.Menu()
		self.menu.Append(self.NEW, "New...")
		self.menu.Append(self.EDIT, "Edit...")
		self.menu.Append(self.DELETE, "Delete")
		self.menu.Append(self.MOVE_UP, "Move Up")
		self.menu.Append(self.MOVE_DOWN, "Move Down")
		self.frame.Bind(wx.EVT_MENU, self.OnNewItem, id=self.NEW)
		self.frame.Bind(wx.EVT_MENU, self.OnEditItem, id=self.EDIT)
		self.frame.Bind(wx.EVT_MENU, self.OnDeleteItem, id=self.DELETE)
		self.frame.Bind(wx.EVT_MENU, self.OnMoveUp, id=self.MOVE_UP)
		self.frame.Bind(wx.EVT_MENU, self.OnMoveDown, id=self.MOVE_DOWN)
		
		# Output pane
		self.output = wx.stc.StyledTextCtrl(self.splitter)
		font = wx.Font(
			10,
			wx.FONTFAMILY_DEFAULT,
			wx.FONTSTYLE_NORMAL,
			wx.FONTWEIGHT_NORMAL,
			faceName = "Lucida Console"
		)
		self.output.StyleSetFont(wx.stc.STC_STYLE_DEFAULT, font)
		self.frame.Bind(EVT_TEXT_MESSAGE, self.OnTextMessage)
		self.frame.Bind(EVT_COMPLETED, self.OnCompileCompleted)

		#self.output.SetReadOnly(True)
		
		# Pack and show
		self.splitter.SplitVertically(self.tree, self.output)
		self.frame.Show()
		
		
	def CopySubtree(self, source, dest, previous=None):
		if previous is None:
			di = self.tree.PrependItem(
			dest,
			self.tree.GetItemText(source),
			self.tree.GetItemImage(source),
			self.tree.GetItemImage(source, wx.TreeItemIcon_Selected)
			#self.tree.GetItemData(source) # Disabled because it causes bad crashes!
		)
		else:
			di = self.tree.InsertItem(
				dest,
				previous,
				self.tree.GetItemText(source),
				self.tree.GetItemImage(source),
				self.tree.GetItemImage(source, wx.TreeItemIcon_Selected)
				#self.tree.GetItemData(source)
			)
		el, cookie = self.tree.GetFirstChild(source)
		pos = None
		while el.IsOk():
			pos = self.CopySubtree(el, di, pos)
			el, cookie = self.tree.GetNextChild(source, cookie)
		if self.tree.IsExpanded(source):
			self.tree.Expand(di)
		return di
		
	def OnNewItem(self, evt):
		msg = "Page URL:"
		d = wx.TextEntryDialog(self.frame, msg, "web2help", "http://")
		if d.ShowModal() == wx.ID_OK:
			self.SetModified()
			u = d.GetValue()
			c = glb.Join("", u)
			i = self.tree.AppendItem(self.activeMenuItem, c, self.pageIcon)
			self.tree.Expand(self.activeMenuItem)
			self.tree.SetItemImage(self.activeMenuItem, self.bookIcon)
		evt.Skip()
		
	def OnEditItem(self, evt):
		if self.activeMenuItem != self.tree.GetRootItem():
			t, u = glb.Split(self.tree.GetItemText(self.activeMenuItem))
			msg = "Page URL:"
			d = wx.TextEntryDialog(self.frame, msg, "web2help", u)
			if d.ShowModal() == wx.ID_OK:
				self.SetModified()
				u = d.GetValue()
				c = glb.Join("", u)
				i = self.tree.SetItemText(self.activeMenuItem, c)
		evt.Skip()
		
	def OnDeleteItem(self, evt):
		if self.activeMenuItem != self.tree.GetRootItem():
			msg = "Removing document and all its children: are you sure?"
			d = wx.MessageDialog(self.frame, msg, "web2help", wx.YES_NO | wx.ICON_WARNING)
			if d.ShowModal() == wx.ID_YES:
				self.SetModified()
				parent = self.tree.GetItemParent(self.activeMenuItem)
				self.tree.Delete(self.activeMenuItem)
				if not self.tree.ItemHasChildren(parent) and parent != self.tree.GetRootItem():
					self.tree.SetItemImage(parent, self.pageIcon)
			self.activeMenuItem = None
		evt.Skip()
		
	def OnMoveUp(self, evt):
		act = self.activeMenuItem
		parent = self.tree.GetItemParent(act)
		prev = self.tree.GetPrevSibling(act)
		if prev.IsOk():
			self.SetModified()		
			prev = self.tree.GetPrevSibling(prev)
			if prev.IsOk():
				self.CopySubtree(act, parent, prev)
			else:
				self.CopySubtree(act, parent)	
			self.tree.Delete(act)
			self.activeMenuItem = None
		evt.Skip()
		
	def OnMoveDown(self, evt):
		act = self.activeMenuItem
		parent = self.tree.GetItemParent(act)
		next = self.tree.GetNextSibling(act)
		if next.IsOk():
			self.SetModified()
			self.CopySubtree(act, parent, next)
			self.tree.Delete(act)
			self.activeMenuItem = None
		evt.Skip()
		
	def OnTreeItemRightClick(self, evt):
		self.activeMenuItem = evt.GetItem()
		self.frame.PopupMenu(self.menu)
		evt.Skip()

		
	def BindMyMenu(self):
		"""Bind a menu item, by xrc name, to a handler"""
		def Bind(handler, xrcname):
			self.Bind(wx.EVT_MENU, handler, xrcname)
			
		Bind(self.OnProjectProperties, 'properties')
		Bind(self.OnCompile, 'compile')


	def New(self):
		self.tree.DeleteAllItems()
		self.tree.AddRoot("Help", self.bookIcon)
		self.project = Project()
		
	def Open(self):
		t = ET.parse(self.document)
		root = t.getroot()
		self.project.Unserialize(root)
		self.TreeUnserialize(root)		
		
	def Save(self):
		root = ET.Element('root')
		root.append(self.project.Serialize())
		root.append(self.TreeSerialize())
		t = ET.ElementTree(root)
		t.write(self.document)
		
	def OnProjectProperties(self, evt):
		p = MyProperties(self.frame, self.project)
		if p.ShowModal() == wx.ID_OK:
			self.SetModified()
		
	def OnCompile(self, evt):
		self.output.ClearAll()
		self.grabber = Grabber(self.tree, self.project, self.frame)
		self.grabber.start()
		self.SetModified()
		self.percentTotal = self.tree.GetCount()
		self.percent = 0		
		self.cancelDialog = wx.ProgressDialog(
			"Compiling...",
			"Web2help is about to retrieve your help files from the web, and convert them into CHM help files",
			self.percentTotal,
			self.frame,
			wx.PD_CAN_ABORT | wx.PD_AUTO_HIDE 
		)
		h = self.cancelDialog.Show()
		
	def OnCompileCompleted(self, evt):
		self.cancelDialog.Update(self.percentTotal)
		self.cancelDialog.Destroy()
		self.cancelDialog = None
		evt.Skip()
		
	def OnTextMessage(self, evt):
		self.output.AppendText(evt.message + "\n")
		if self.percent < self.percentTotal - 1:
			self.percent += 1
		cont, skip = self.cancelDialog.Update(self.percent, evt.message)
		if not cont:
			self.grabber.Stop()
		evt.Skip()
		
	def TreeSerializeNode(self, e, item):
		if item != self.tree.GetRootItem():
			node = ET.SubElement(e, 'node')
			n, u = glb.Split(self.tree.GetItemText(item))
			node.set('name', n)
			node.set('url', u)
		else:
			node = e
		el, cookie = self.tree.GetFirstChild(item)
		while el.IsOk():
			self.TreeSerializeNode(node, el)
			el, cookie = self.tree.GetNextChild(item, cookie)
		
	def TreeSerialize(self):
		e = ET.Element('toc')
		self.TreeSerializeNode(e, self.tree.GetRootItem())
		return e
		
	def TreeUnserializeChildren(self, e, item):
		hasChildren = False
		for n in e:
			hasChildren = True
			name = n.get('name')
			url = n.get('url')
			i = self.tree.AppendItem(item, glb.Join(name, url), self.pageIcon)
			if self.TreeUnserializeChildren(n, i):
				self.tree.SetItemImage(i, self.bookIcon)
		return hasChildren
			
	def TreeUnserialize(self, e):
		self.tree.DeleteAllItems()
		rootitem = self.tree.AddRoot("Help", self.bookIcon)
		toc = e.find('toc')
		self.TreeUnserializeChildren(toc, rootitem)
		self.tree.ExpandAll()
		
		