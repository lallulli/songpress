###############################################################
# Name:			 SongpressFrame.py
# Purpose:	 Main frame for Songpress
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-16
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import wx
#import wx.aui
from wx import xrc
from SDIMainFrame import *
from Globals import glb


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
		
		# Tree
		self.tree = wx.TreeCtrl(self.frame)
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
			c = d.GetValue()
			i = self.tree.AppendItem(self.activeMenuItem, c)
			self.tree.Expand(self.activeMenuItem)
		evt.Skip()
		
	def OnEditItem(self, evt):
		evt.Skip()
		
	def OnDeleteItem(self, evt):
		if self.activeMenuItem != self.tree.GetRootItem():
			msg = "Removing document and all its children: are you sure?"
			d = wx.MessageDialog(self.frame, msg, "web2help", wx.YES_NO | wx.ICON_WARNING)
			if d.ShowModal() == wx.ID_YES:				
				self.tree.Delete(self.activeMenuItem)
			self.activeMenuItem = None
		evt.Skip()
		
	def OnMoveUp(self, evt):
		act = self.activeMenuItem
		parent = self.tree.GetItemParent(act)
		prev = self.tree.GetPrevSibling(act)
		if prev.IsOk():
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
			
		Bind(self.OnUndo, 'undo')
		Bind(self.OnRedo, 'redo')
		Bind(self.OnCut, 'cut')
		Bind(self.OnCopy, 'copy')
		Bind(self.OnCopyAsImage, 'copyAsImage')
		Bind(self.OnPaste, 'paste')
		Bind(self.OnFind, 'find')
		Bind(self.OnFindNext, 'findNext')
		Bind(self.OnFindPrevious, 'findPrevious')
		Bind(self.OnReplace, 'replace')
		Bind(self.OnTitle, 'title')
		Bind(self.OnChord, 'chord')
		Bind(self.OnChorus, 'chorus')
		Bind(self.OnComment, 'comment')
		Bind(self.OnFormatFont, 'font')
		Bind(self.OnLabelVerses, 'labelVerses')
		Bind(self.OnChorusLabel, 'chorusLabel')
		Bind(self.OnOptions, 'options')

	def New(self):
		self.tree.DeleteAllItems()
		self.tree.AddRoot("Help")
		
	def Open(self):
		pass
		
	def Save(self):
		pass
		