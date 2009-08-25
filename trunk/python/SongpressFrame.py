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

class SongpressFrame(SDIMainFrame):

	def __init__(self, res):
		SDIMainFrame.__init__(self, res, 'MainFrame', 'Songpress - Il Canzonatore', 'Luca Allulli', 'song', 'crd')
		self.text = Editor(self)
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
		self.frame.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose, self.frame)
		self.FinalizePaneInitialization()
		self.BindMyMenu()
		
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
		self.mainToolBar.EnableTool(self.copyTool, s != e)
		
	def UpdateEverything(self):
		self.UpdateUndoRedo()
		self.UpdateCutCopyPaste()
		
	def TextUpdated(self):
		self.previewCanvas.Refresh(self.text.GetText())
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
		f = wx.FindReplaceDialog(self.frame, wx.FindReplaceData(), "Find")
		f.Show()
		
	def OnFindDialog(self, evt):
		pass
		
	def OnFindNext(self, evt):
		pass

	def OnReplace(self, evt):
		pass
	
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

