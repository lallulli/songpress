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
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import wx
import wx.aui
from wx import xrc
import os
import os.path
import sys
import i18n
import platform

i18n.register('SDIMainFrame')

class SDIDropTarget(wx.FileDropTarget):
	def __init__(self, sdi):
		wx.FileDropTarget.__init__(self)
		self.sdi = sdi
	def OnDropFiles(self, x, y, arr):
		self.sdi.OnDropFiles(arr)

class SDIMainFrame(wx.FileDropTarget):
	"""Abstract class. Override methods New, Open, Save"""
	###UI generation###

	def __init__(
		self,
		res,
		frameName='MainFrame',
		appName='SDIApp',
		authorName='Nobody',
		docType='document',
		docExt='txt',
		appLongName=None,
		icon=None,
		version="1.0",
		url="",
		copyright = "",
		licensing = "",
		thanks = "",
		importFormats = [] # List of tuples: (format name, [extensions])
	):
		self.config = wx.Config.Get()
		self.res = res
		i18n.localizeXrc('xrc/songpress.xrc')
		self.appName = appName
		self.appLongName = self.appName if appLongName == None else appLongName
		self.authorName = authorName
		self.modified = False
		self.version = version
		self.url = url
		self.copyright = copyright
		self.licensing = licensing
		self.thanks = thanks
		self.document = ''
		self.docType = docType
		self.docExt = docExt
		self.importFormats = importFormats
		wx.Config.Set(self.config)
		self.frame = self.res.LoadFrame(None, frameName)
		if icon != None:
			self.frame.SetIcon(wx.Icon(icon, wx.BITMAP_TYPE_ICO))
		self.BindMenu()
		self.frame.Bind(wx.EVT_CLOSE, self.OnClose, self.frame)
		dt = SDIDropTarget(self)
		self.frame.SetDropTarget(dt)
		self.UpdateTitle()
		self._mgr = wx.aui.AuiManager(self.frame)
		self._mgr.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
		self.menuBar = self.frame.GetMenuBar()
		self.panesByMenu = {}
		self.menusByPane = {}
		self.RetrieveRecentFileList()

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
		
	def SetDefaultExtension(self, ext):
		self.docExt = ext

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
			if self.importFormats == []:
				filter = _("%s files (*.%s)|%s") % (
						self.docExt,
						self.docExt,
						self.docExt,
					)
			else:
				filter = "|".join(["%s|%s" % (x[0], ";".join(["*." + y for y in x[1]])) for x in self.importFormats])
			filter += _("|All files (*.*)|*.*")
			dlg = wx.FileDialog(
				self.frame,
				_("Open file"),
				"",
				"",
				filter,
				wx.FD_OPEN
			)

			if dlg.ShowModal() == wx.ID_OK:
				fn = dlg.GetPath()
				if os.path.isfile(fn):
					self.document = fn
					self.Open()
					self.UpdateRecentFileList(fn)
					self.modified = False
					self.UpdateTitle()
				else:
					msg = _("File \"%s\" does not exist.") % (fn, )
					d = wx.MessageDialog(
						self.frame,
						msg,
						self.appLongName,
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
		msg = _("%s version %s\n%s\n\n%s\n\n%s\n\n%s") % (
			self.appLongName,
			self.version,
			self.url,
			self.copyright,
			self.licensing,
			self.thanks
		)
		wx.MessageBox(msg, _('About ') + self.appLongName)

	def OnDropFiles(self, arr):
		"""Handler for drop action: opens the dropped file, if it is exactly one"""
		if len(arr) == 1:
			fn = arr[0]
			if os.path.isfile(fn) and self.AskSaveModified():
				self.document = fn
				self.Open()
				self.UpdateRecentFileList(fn)
				self.modified = False
				self.UpdateTitle()

	def OnClose(self, evt):
		"""Handler for windows close event"""
		if self.AskSaveModified(evt.CanVeto()):
			self.config.SetPath('/SDIMainFrame')
			self.config.Write("Version", self.version)
			p = self._mgr.SavePerspective()
			self.config.Write("Perspective", p)
			self.SavePreferences()
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
			doc = _('Untitled')
		else:
			doc = os.path.basename(self.document)
			(doc, ext) = os.path.splitext(doc)
		self.frame.SetTitle(u"%s%s - %s" % (mod, doc, self.appLongName))

	def AskSaveModified(self, canCancel = True):
		"""If file has been modified, propose to save changes. Return False if cancelled, True otherwise"""
		if not self.modified:
			return True

		if canCancel:
			cc = wx.CANCEL
		else:
			cc = 0

		d = wx.MessageDialog(self.frame, _("Your %s has been modified. Do you want to save it?") % (self.docType), self.appLongName, wx.YES_NO | wx.ICON_QUESTION | cc)
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
				_("Choose a name for the file"),
				"",
				"",
				_("%s files (*.%s)|*.%s|All files (*.*)|*.*") % (
						self.docExt,
						self.docExt,
						self.docExt,
					),
				wx.FD_SAVE
			)

			if dlg.ShowModal() == wx.ID_OK:

				fn = dlg.GetPath()
				if os.path.isfile(fn):
					msg = _("File \"%s\" already exists. Do you want to overwrite it?") % (fn, )
					d = wx.MessageDialog(
						self.frame,
						msg,
						self.appLongName,
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
			if platform.system() == 'Linux':
				# Since wxPython file dialog in Linux does not add default extension
				# when it has not been specified by user, we add it ourselves
				pref, ext = os.path.splitext(fn)
				if ext == '':
					fn = '%s.%s' % (fn, self.docExt)
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
		self.Save()
		self.UpdateRecentFileList(self.document)
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

	def SavePreferences(self):
		"""To be overridden: save preferences to wxConfig object"""
		pass

	def AddMainPane(self, window):
		self._mgr.AddPane(window, wx.aui.AuiPaneInfo().CenterPane().Name('_main'))

	def AddPane(self, window, info, caption, menuName):
		self._mgr.AddPane(window, info.Name(menuName).Caption(caption))
		pane = self._mgr.GetPane(window)
		menuid = xrc.XRCID(menuName)
		self.panesByMenu[menuid] = pane
		self.menusByPane[pane.name] = menuid
		self.Bind(wx.EVT_MENU, self.OnTogglePaneView, menuName)
		return pane

	def OnTogglePaneView(self, evt):
		status = evt.GetInt()
		menu = evt.GetId()
		self.panesByMenu[menu].Show(status)
		self._mgr.Update()

	def OnPaneClose(self, evt):
		pane = evt.GetPane()
		menuid = self.menusByPane[pane.name]
		self.menuBar.Check(menuid, False)

	def RetrieveRecentFileList(self):
		self.recentMenuBase = 800
		self.config.SetPath('/SDIMainFrame/RecentFiles')
		self.recentFiles = []
		for i in xrange(1, 5):
			f = self.config.Read(str(i))
			if f:
				self.recentFiles.append(f)
			self.frame.Bind(wx.EVT_MENU, self.OnRecentFile, id = self.recentMenuBase + i)
		self.UpdateRecentFileMenu()

	def EmptyRecentFileMenu(self):
		fileMenu = self.menuBar.GetMenu(0)
		for i in xrange(1, len(self.recentFiles)+1):
			fileMenu.Remove(self.recentMenuBase + i)

	def UpdateRecentFileMenu(self):
		i = 1
		fileMenu = self.menuBar.GetMenu(0)
		self.config.SetPath('/SDIMainFrame/RecentFiles')
		for k in self.recentFiles:
			d, f = os.path.split(k)
			if len(d) > 25:
				d = d[:25] + "..."
			fileMenu.Append(self.recentMenuBase + i, os.path.join(d, f))
			self.config.Write(str(i), k)
			i += 1

	def UpdateRecentFileList(self, name):
		self.EmptyRecentFileMenu()
		if name in self.recentFiles:
			self.recentFiles.remove(name)
		self.recentFiles.insert(0, name)
		if len(self.recentFiles) > 4:
			self.recentFiles.pop()
		self.UpdateRecentFileMenu()

	def OnRecentFile(self, evt):
		i = evt.GetId() - self.recentMenuBase
		fn = self.recentFiles[i-1]
		if os.path.isfile(fn) and self.AskSaveModified():
			self.document = fn
			self.Open()
			self.UpdateRecentFileList(fn)
			self.modified = False
			self.UpdateTitle()

	def FinalizePaneInitialization(self):
		self.config.SetPath('/SDIMainFrame')
		v = self.config.Read("Version", "0.0")
		vs = v.split('.')
		svs = self.version.split('.')
		p = False
		if vs[:1] == svs[:1]:
			p = self.config.Read("Perspective")
		#print "Config: " + str(p)
		if p:
			self._mgr.LoadPerspective(p)
			for menuid in self.panesByMenu:
				self.menuBar.Check(menuid, self.panesByMenu[menuid].IsShown())
		else:
			self._mgr.Update()
		if len(sys.argv) > 1:
			self.OnDropFiles([sys.argv[1].decode(sys.getfilesystemencoding())])
		self.frame.Show()
