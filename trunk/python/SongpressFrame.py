###############################################################
# Name:			 SongpressFrame.py
# Purpose:	 Main frame for Songpress
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-16
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

import wx
import wx.aui
from wx import xrc
from SDIMainFrame import *
from Editor import *
from PreviewCanvas import *
from SongFormat import *
from Renderer import *
from decorators import StandardVerseNumbers
from FontComboBox import FontComboBox
from FontFaceDialog import FontFaceDialog

class SongpressFindReplaceDialog(object):
	def __init__(self, owner, replace = False):
		object.__init__(self)
		self.data = wx.FindReplaceData()
		self.owner = owner
		self.searchString = ""
		self.dialog = wx.FindReplaceDialog(
			owner.frame,
			self.data,
			"Replace" if replace else "Find",
			wx.FR_REPLACEDIALOG if replace else 0
		)
		owner.frame.Bind(wx.EVT_FIND, self.OnFind, self.dialog)
		owner.frame.Bind(wx.EVT_FIND_NEXT, self.OnFind, self.dialog)
		owner.frame.Bind(wx.EVT_FIND_CLOSE, self.OnClose, id=wx.ID_ANY)
		owner.frame.Bind(wx.EVT_FIND_REPLACE, self.OnReplace, self.dialog)
		owner.frame.Bind(wx.EVT_FIND_REPLACE_ALL, self.OnReplaceAll, self.dialog)
		self.dialog.Show()

	def OnFind(self, evt):
		self.st = evt.GetFindString()
		f = self.data.GetFlags()
		self.down = f & wx.FR_DOWN
		self.whole = f & wx.FR_WHOLEWORD
		self.case = f & wx.FR_MATCHCASE
		self.FindNext()

	def FindNext(self):
		s, e = self.owner.text.GetSelection()
		fromStart = s == 0
		p = self.owner.text.FindText(e, self.owner.text.GetTextLength(), self.st)
		if p != -1:
			self.owner.text.SetSelection(p, p + len(self.st))
		else:
			if not fromStart:
				d = wx.MessageDialog(
					self.owner.frame,
					"Reached the end of the song, restarting search from the beginning",
					self.owner.appName,
					wx.OK | wx.CANCEL | wx.ICON_INFORMATION
				)
				res = d.ShowModal()
				if res == wx.ID_OK:
					self.owner.text.SetSelection(0, 0)
					self.FindNext()
			else:
				d = wx.MessageDialog(
					self.owner.frame,
					"The specified text was not found",
					self.owner.appName,
					wx.OK | wx.ICON_INFORMATION
				)
				res = d.ShowModal()
	
	def OnReplace(self, evt):
		r = evt.GetReplaceString()
		if self.owner.text.GetSelectedText() == self.st:
			self.owner.text.ReplaceSelection(r)
			self.FindNext()
	
	def OnReplaceAll(self, evt):
		f = evt.GetFindString()
		r = evt.GetReplaceString()
		text = self.owner.text.GetText()
		c = text.count(f)
		text = text.replace(f, r)
		self.owner.text.SetText(text)
		d = wx.MessageDialog(
			self.owner.frame,
			"%d text occurrences have been replaced" % (c,),
			self.owner.appName,
			wx.OK | wx.ICON_INFORMATION
		)
		res = d.ShowModal()
		
	
	def OnClose(self, evt):
		self.dialog.Destroy()
		self.dialog = None


class SongpressFrame(SDIMainFrame):

	def __init__(self, res):
		SDIMainFrame.__init__(self, res, 'MainFrame', 'Songpress - Il Canzonatore', 'Luca Allulli', 'song', 'crd')
		self.text = Editor(self)
		self.frame.Bind(wx.stc.EVT_STC_UPDATEUI, self.OnUpdateUI, self.text)
		self.format = SongFormat()
		self.decoratorFormat = StandardVerseNumbers.Format(self.format)
		self.decorator = StandardVerseNumbers.Decorator(self.decoratorFormat)
		self.previewCanvas = PreviewCanvas(self.frame, self.format, self.decorator)
		self.AddMainPane(self.text)
		self.previewCanvas.panel.SetSize(wx.Size(400, 800))
		self.previewCanvasPane = self.AddPane(self.previewCanvas.panel, wx.aui.AuiPaneInfo().Right(), 'Preview', 'preview')
		self.previewCanvasPane.BestSize(wx.Size(400,800))
		self.mainToolBar = wx.ToolBar(self.frame, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
			wx.TB_FLAT | wx.TB_NODIVIDER)
		self.mainToolBar.SetToolBitmapSize(wx.Size(16, 16))
		self.mainToolBar.AddTool(wx.xrc.XRCID('new'), wx.BitmapFromImage(wx.Image("img/new.png")))
		self.mainToolBar.AddTool(wx.xrc.XRCID('open'), wx.BitmapFromImage(wx.Image("img/open.png")))
		self.mainToolBar.AddTool(wx.xrc.XRCID('save'), wx.BitmapFromImage(wx.Image("img/save.png")))
		self.mainToolBar.AddSeparator()
		self.undoTool = wx.xrc.XRCID('undo')
		self.mainToolBar.AddTool(self.undoTool, wx.BitmapFromImage(wx.Image("img/undo.png")))
		self.redoTool = wx.xrc.XRCID('redo')
		self.mainToolBar.AddTool(self.redoTool, wx.BitmapFromImage(wx.Image("img/redo.png")))
		self.mainToolBar.AddSeparator()
		self.cutTool = wx.xrc.XRCID('cut')
		self.mainToolBar.AddTool(self.cutTool, wx.BitmapFromImage(wx.Image("img/cut.png")))
		self.copyTool = wx.xrc.XRCID('copy')
		self.mainToolBar.AddTool(self.copyTool, wx.BitmapFromImage(wx.Image("img/copy.png")))
		self.mainToolBar.AddTool(wx.xrc.XRCID('copyAsImage'), wx.BitmapFromImage(wx.Image("img/copyAsImage2.png")))
		self.pasteTool = wx.xrc.XRCID('paste')
		self.mainToolBar.AddTool(self.pasteTool, wx.BitmapFromImage(wx.Image("img/paste.png")))
		self.mainToolBar.Realize()
		self.mainToolBarPane = self.AddPane(self.mainToolBar, wx.aui.AuiPaneInfo().ToolbarPane().Top().Row(1).Position(1), 'Standard', 'standard')		
		self.formatToolBar = wx.ToolBar(self.frame, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
			wx.TB_FLAT | wx.TB_NODIVIDER)
		self.fontChooser = FontComboBox(self.formatToolBar, -1, self.format.face)
		self.formatToolBar.AddControl(self.fontChooser)
		self.frame.Bind(wx.EVT_COMBOBOX, self.OnFontSelected, self.fontChooser)
		self.frame.Bind(wx.EVT_TEXT_ENTER, self.OnFontSelected, self.fontChooser)
		self.formatToolBar.AddTool(wx.xrc.XRCID('title'), wx.BitmapFromImage(wx.Image("img/title.png")))
		self.formatToolBar.AddTool(wx.xrc.XRCID('chord'), wx.BitmapFromImage(wx.Image("img/chord.png")))
		self.formatToolBar.AddTool(wx.xrc.XRCID('chorus'), wx.BitmapFromImage(wx.Image("img/chorus.png")))
		self.formatToolBar.Realize()
		self.formatToolBarPane = self.AddPane(self.formatToolBar, wx.aui.AuiPaneInfo().ToolbarPane().Top().Row(1).Position(2), 'Format', 'format')
		self.BindMyMenu()
		self.cutMenuId = xrc.XRCID('cut')
		self.copyMenuId = xrc.XRCID('copy')
		self.pasteMenuId = xrc.XRCID('paste')
		self.findReplaceDialog = None
		self.FinalizePaneInitialization()
		
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
		Bind(self.OnReplace, 'replace')
		Bind(self.OnTitle, 'title')
		Bind(self.OnChord, 'chord')
		Bind(self.OnChorus, 'chorus')
		Bind(self.OnComment, 'comment')
		Bind(self.OnFormatFont, 'font')

	def New(self):
		self.text.New()
		self.UpdateEverything()
		
	def Open(self):
		self.text.Open()
		self.UpdateEverything()
		
	def Save(self):
		self.text.Save()
		self.UpdateEverything()
		
	def UpdateUndoRedo(self):
		self.mainToolBar.EnableTool(self.undoTool, self.text.CanUndo())
		self.mainToolBar.EnableTool(self.redoTool, self.text.CanRedo())		
		
	def UpdateCutCopyPaste(self):
		s, e = self.text.GetSelection()
		self.mainToolBar.EnableTool(self.cutTool, s != e)
		self.menuBar.Enable(self.cutMenuId, s != e)
		self.mainToolBar.EnableTool(self.copyTool, s != e)
		self.menuBar.Enable(self.copyMenuId, s != e)
		self.mainToolBar.EnableTool(self.pasteTool, self.text.CanPaste())
		self.menuBar.Enable(self.pasteMenuId, self.text.CanPaste())
		
	def UpdateEverything(self):
		self.UpdateUndoRedo()
		self.UpdateCutCopyPaste()
		
	def TextUpdated(self):
		self.previewCanvas.Refresh(self.text.GetText())
		#self.UpdateEverything()
		
	def OnUpdateUI(self, evt):
		self.UpdateEverything()

	def OnUndo(self, evt):
		if self.text.CanUndo():
			self.text.Undo()
			self.UpdateUndoRedo()

	def OnRedo(self, evt):
		if self.text.CanRedo():
			self.text.Redo()
			self.UpdateUndoRedo()

	def OnCut(self, evt):
		self.text.Cut()
		
	def OnCopy(self, evt):
		self.text.Copy()

	def OnCopyAsImage(self, evt):
		r = Renderer(self.format, self.decorator)
		dc = wx.MetaFileDC()
		start, end = self.text.GetSelection()
		if start == end:
			r.Render(self.text.GetText(), dc)
		else:
			r.Render(self.text.GetText(), dc, self.text.LineFromPosition(start), self.text.LineFromPosition(end))
		m = dc.Close()
		m.SetClipboard(dc.MaxX(), dc.MaxY())
		
	def OnPaste(self, evt):
		self.text.Paste()
	
	def OnFind(self, evt):
		self.findReplaceDialog = SongpressFindReplaceDialog(self)
		
	def OnFindNext(self, evt):
		if self.findReplaceDialog != None:
			self.findReplaceDialog.FindNext()

	def OnReplace(self, evt):
		self.findReplaceDialog = SongpressFindReplaceDialog(self, True)
	
	def OnFontSelected(self, evt):
		font = self.fontChooser.GetValue()
		self.format.face = font
		self.format.chord.face = font
		self.format.chorus.face = font
		self.format.chorus.chord.face = font
		for v in self.format.verse:
			v.face = font
			v.chord.face = font
		self.format.title.face = font
		self.format.comment.face = font
		self.decoratorFormat.face = font
		self.decoratorFormat.chorus.face = font		
		self.previewCanvas.Refresh(self.text.GetText())
		
	def OnFormatFont(self, evt):
		f = FontFaceDialog(self.frame, wx.ID_ANY, "Songpress", self.format, self.decorator, self.decoratorFormat)
		if f.ShowModal() == wx.ID_OK:
			self.fontChooser.SetValue(f.GetValue())
			self.previewCanvas.Refresh(self.text.GetText())
			#self.OnFontSelected(evt)
			
	def InsertWithCaret(self, st):
		s, e = self.text.GetSelection()
		c = st.find('|')
		if c != -1:
			self.text.ReplaceSelection(st[:c] + st[c+1:])
			self.text.SetSelection(s + c, s + c)
		else:
			self.text.ReplaceSelection(st)
			self.text.SetSelection(s + len(st), s + len(st))
			
	def OnTitle(self, evt):
		self.InsertWithCaret("{title:|}\n\n")
			
	def OnChord(self, evt):
		self.InsertWithCaret("[|]")
	
	def OnChorus(self, evt):
		self.InsertWithCaret("{soc}\n|\n{eoc}\n")
	
	def OnComment(self, evt):
		self.InsertWithCaret("{c:|}")
		

