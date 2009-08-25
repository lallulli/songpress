"""Framework providing common functionality for SDI Main Frames

The module provides an (abstract) class loads an XRC resource describing a SDI Frame.
It expects to find some menu elements, characterized by their XRC name:
	- new
	- open
	- save
	- saveAs
	- exit
	- about
"""

###############################################################
# Name:			 SDIMainFrame.py
# Purpose:	 Abstract class for SDI Main Frames
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-16
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

import wx
import wx.aui
from wx import xrc
import os


class SDIDropTarget(wx.FileDropTarget):
	def __init__(self, sdi):
		wx.FileDropTarget.__init__(self)
		self.sdi = sdi
	def OnDropFiles(self, x, y, arr):
		self.sdi.OnDropFiles(arr)

class SDIMainFrame(wx.FileDropTarget):
	"""Abstract class. Override methods New, Open, Save"""
	###UI generation###

	def __init__(self, res, frameName='MainFrame', appName='SDIApp', authorName='Nobody', docType='document', docExt='txt'):
		self.res = res
		self.appName = appName
		self.authorName = authorName
		self.modified = False
		self.document = ''
		self.docType = docType
		self.docExt = docExt
		self.frame = self.res.LoadFrame(None, frameName)
		self.BindMenu()
		self.frame.Bind(wx.EVT_CLOSE, self.OnClose, self.frame)
		dt = SDIDropTarget(self)
		self.frame.SetDropTarget(dt)
		self.UpdateTitle()
		self._mgr = wx.aui.AuiManager(self.frame)
		self.panesByMenu = {}
		self.menusByPane = {}
		self.frame.Show()

	def Bind(self, event, handler, xrcname):
		"""Bind an event, coming from a control by xrc name, to a handler"""
		self.frame.Bind(event, handler, id=xrc.XRCID(xrcname))

	def BindMenu(self):
		"""Bind a menu item, by xrc name, to a handler"""
		def Bind(handler, xrcname):
			self.Bind(wx.EVT_MENU, handler, xrcname)

		Bind(self.OnNew, 'new')
		Bind(self.OnOpen, 'open')
		Bind(self.OnSave, 'save')
		Bind(self.OnSaveAs, 'saveAs')
		Bind(self.OnExit, 'exit')
		Bind(self.OnAbout, 'about')

	def OnNew(self, evt):
		"""Menu handler for File->New"""
		if self.AskSaveModified():
			self.document = ''
			self.New()
			self.modified = False
			self.UpdateTitle()
		
	def OnOpen(self, evt):
		"""Menu handler for File->Open"""
		if self.AskSaveModified():
			dlg = wx.FileDialog(
				self.frame,
				"Open file",
				"",
				"",
				"%s files (*.%s)|*.%s|All files (*.*)|*.*" % (self.docExt, self.docExt, self.docExt),
				wx.FD_OPEN
			)

			if dlg.ShowModal() == wx.ID_OK:
				fn = dlg.GetPath()
				if os.path.isfile(fn):
					self.document = fn
					self.Open()
					self.modified = False
					self.UpdateTitle()
				else:
					msg = "File \"%s\" does not exist." % (fn, )
					d = wx.MessageDialog(
						self.frame,
						msg,
						self.appName,
						wx.OK | wx.ICON_ERROR
					)
					d.ShowModal()
		
	def OnSave(self, evt):
		"""Menu handler for File->Save"""
		self.SaveFile()
		
	def OnSaveAs(self, evt):
		"""Menu handler for File->Save As"""
		if self.AskSaveFilename():
			self.SaveFile()

	def OnExit(self, evt):
		"""Menu handler for File->Exit"""
		self.frame.Close()

	def OnAbout(self, evt):
		"""Menu handler for ?->About"""
		wx.MessageBox('%s by %s' % (self.appName, self.authorName), 'About ' + self.appName)
		
	def OnDropFiles(self, arr):
		"""Handler for drop action: opens the dropped file, if it is exactly one"""
		if len(arr) == 1:
			fn = arr[0]
			if os.path.isfile(fn) and self.AskSaveModified():
				self.document = fn
				self.Open()
				self.modified = False
				self.UpdateTitle()
	
	def OnClose(self, evt):
		"""Handler for windows close event"""	
		if self.AskSaveModified(evt.CanVeto()):
			p = self._mgr.SavePerspective()
			c = wx.FileConfig()
			c.Write("Perspective", p)
			self.frame.Destroy()
		else:
			evt.Veto()

	###Ordinary methods###

	def SetModified(self, m = True):
		"""Set the modified flag, if main document is modified"""	
		self.modified = m
		self.UpdateTitle()

	def UpdateTitle(self):
		"""Updates form title; to be called when the filename or the modified status changes"""
		if self.modified:
			mod = '* '
		else:
			mod = ''
		if self.document == '':
			doc = 'Untitled'
		else:
			doc = os.path.basename(self.document)
			(doc, ext) = os.path.splitext(doc)
		self.frame.SetTitle("%s%s - %s" % (mod, doc, self.appName))
		
	def AskSaveModified(self, canCancel = True):
		"""If file has been modified, propose to save changes. Return False if cancelled, True otherwise"""	
		if not self.modified:
			return True
		
		if canCancel:
			cc = wx.CANCEL
		else:
			cc = 0
	
		d = wx.MessageDialog(self.frame, "Your %s has been modified. Do you want to save it?" % (self.docType), self.appName, wx.YES_NO | wx.ICON_QUESTION | cc)
		res = d.ShowModal()
		if res == wx.ID_CANCEL:
			return False
		elif res == wx.ID_NO:
			return True
		else: #wxID_YES
			return self.SaveFile();
		
	def AskSaveFilename(self):
		"""Ask and updates the filename (without saving); return False if user cancels, True otherwise"""	
		leave = False;
		consensus = False;
		while not leave:
			dlg = wx.FileDialog(
				self.frame,
				"Choose a name for the file",
				"",
				"",
				"%s files (*.%s)|*.%s|All files (*.*)|*.*" % (self.docExt, self.docExt, self.docExt),
				wx.FD_SAVE
			)

			if dlg.ShowModal() == wx.ID_OK:

				fn = dlg.GetPath()
				if os.path.isfile(fn):
					msg = "File \"%s\" already exists. Do you want to overwrite it?" % (fn, );
					d = wx.MessageDialog(
						self.frame,
						msg,
						self.appName,
						wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION
					)
					res = d.ShowModal()
					if res == wx.ID_CANCEL:
						leave = True
						consensus = False
					elif res == wx.ID_NO:
						leave = False
						consensus = False
					else: #wxID_YES
						leave = True
						consensus = True
				else:
					leave = True
					consensus = True

			else:
				leave = True
				consensus = False

		if consensus:
			self.document = fn
			self.UpdateTitle()
			return wx.ID_OK
		else:
			return False
			
	def SaveFile(self):
		"""Save file, asking for file name if necessary. Return False if user cancels, True otherwise"""
		if self.document == '':
			if not self.AskSaveFilename():
				return False
		if self.modified:
			self.Save()
			self.modified = False
			self.UpdateTitle()
		return True
	
	def New(self):
		"""To be overridden: create a blank document"""
		pass
	
	def Open(self):
		"""To be overridden: open a document"""
		pass
	
	def Save(self):
		"""To be overridden: save a document"""
		return True

	def AddMainPane(self, window):
		self._mgr.AddPane(window, wx.aui.AuiPaneInfo().CenterPane().Name('_main'))

	def AddPane(self, window, info, caption, menuName):
		self._mgr.AddPane(window, info.Name(menuName).Caption(caption))
		pane = self._mgr.GetPane(window)
		menuid = xrc.XRCID(menuName)
		self.panesByMenu[menuid] = pane
		self.menusByPane[pane] = menuid
		self.Bind(wx.EVT_MENU, self.OnTogglePaneView, menuName)		
		return pane
		
	def OnTogglePaneView(self, evt):
		status = evt.GetInt()
		menu = evt.GetId()
		self.panesByMenu[menu].Show(status)
		self._mgr.Update()		
	
	def OnPaneClose(self, evt):
		print "Render: " + str(evt)
		
	def FinalizePaneInitialization(self):
		c = wx.FileConfig()
		p = c.Read("Perspective")
		if p:
			print "yes, " + p
			self._mgr.LoadPerspective(p)
		else:
			self._mgr.Update()
