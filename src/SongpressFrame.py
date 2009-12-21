###############################################################
# Name:			 SongpressFrame.py
# Purpose:	 Main frame for Songpress
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-16
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
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
from SongDecorator import SongDecorator
from FontComboBox import FontComboBox
from FontFaceDialog import FontFaceDialog
from PreferencesDialog import PreferencesDialog
from Transpose import *
from MyTransposeDialog import *
from MyNotationDialog import *
from Globals import glb
import subprocess
import os
import os.path
import i18n

i18n.register('SongpressFrame')

class SongpressFindReplaceDialog(object):
	def __init__(self, owner, replace = False):
		object.__init__(self)
		self.data = wx.FindReplaceData(wx.FR_DOWN)
		self.owner = owner
		self.searchString = ""
		self.dialog = wx.FindReplaceDialog(
			owner.frame,
			self.data,
			_("Replace") if replace else _("Find"),
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
		self.flags = 0
		if self.whole:
			self.flags |= wx.stc.STC_FIND_WHOLEWORD
		if self.case:
			self.flags |= wx.stc.STC_FIND_MATCHCASE
		self.FindNext()

	def FindNext(self):
		if self.down:
			self.search = self.owner.text.SearchNext
		else:
			self.search = self.owner.text.SearchPrev
		s, e = self.owner.text.GetSelection()
		if self.down:
			self.owner.text.SetSelection(e, e)
			fromStart = s == 0
		else:
			self.owner.text.SetSelection(s, s)
			fromStart = s == self.owner.text.GetLength()
		self.owner.text.SearchAnchor()		
		p = self.search(self.flags, self.st)
		if p != -1:
			pass
			self.owner.text.SetSelection(p, p + len(self.st))
		else:
			parent = self.dialog if self.dialog != None else self.owner.frame
			if not fromStart:
				if self.down:
					where = _("beginning")
					wherefrom = _("Reached the end")
					newStart = 0
				else:
					where = _("end")
					wherefrom = _("Reached the beginning")
					newStart = self.owner.text.GetLength()
				d = wx.MessageDialog(
					parent,
					_("%s of the song, restarting search from the %s") % (wherefrom, where,),
					self.owner.appName,
					wx.OK | wx.CANCEL | wx.ICON_INFORMATION
				)
				res = d.ShowModal()
				if res == wx.ID_OK:
					self.owner.text.SetSelection(newStart, newStart)
					self.FindNext()
			else:
				d = wx.MessageDialog(
					parent,
					_("The specified text was not found"),
					self.owner.appName,
					wx.OK | wx.ICON_INFORMATION
				)
				res = d.ShowModal()
	
	def OnReplace(self, evt):
		r = evt.GetReplaceString()
		if self.owner.text.GetSelectedText().lower() == self.st.lower():
			self.owner.text.ReplaceSelection(r)
			self.FindNext()
	
	def OnReplaceAll(self, evt):
		self.owner.text.BeginUndoAction()
		s = evt.GetFindString()
		r = evt.GetReplaceString()
		f = self.data.GetFlags()
		self.whole = f & wx.FR_WHOLEWORD
		self.case = f & wx.FR_MATCHCASE
		flags = 0
		if self.whole:
			flags |= wx.stc.STC_FIND_WHOLEWORD
		if self.case:
			flags |= wx.stc.STC_FIND_MATCHCASE
		self.owner.text.SetSelection(0, 0)
		p = 0
		c = 0
		while p != -1:
			p = self.owner.text.FindText(p, self.owner.text.GetLength(), s, flags)
			if p != -1:
				self.owner.text.SetTargetStart(p)
				self.owner.text.SetTargetEnd(p + len(s))
				p += self.owner.text.ReplaceTarget(r)
				c += 1
				
		self.owner.text.EndUndoAction()
		
		d = wx.MessageDialog(
			self.dialog,
			_("%d text occurrences have been replaced") % (c,),
			self.owner.appName,
			wx.OK | wx.ICON_INFORMATION
		)
		res = d.ShowModal()
		
	
	def OnClose(self, evt):
		self.dialog.Destroy()
		self.dialog = None


class SongpressFrame(SDIMainFrame):

	def __init__(self, res):
		SDIMainFrame.__init__(
			self,
			res,
			'MainFrame',
			'songpress',
			'Skeed',
			_('song'),
			'crd',
			_('Songpress - Il Canzonatore'),
			glb.AddPath('img/songpress.ico'),
			_("1.1"),
			_("http://www.skeed.it/songpress.html"),
			_("Copyright (c) 2009 Luca Allulli - Skeed"),
			_("Licensed under the terms and conditions of the GNU General Public License, version 2"),
			_("Special thanks to:\n  * The Pyhton programming language (http://www.python.org)\n  * wxWidgets (http://www.wxwidgets.org)\n  * wxPython (http://www.wxpython.org)")
		)
		self.text = Editor(self)
		dt = SDIDropTarget(self)
		self.text.SetDropTarget(dt)
		self.frame.Bind(wx.stc.EVT_STC_UPDATEUI, self.OnUpdateUI, self.text)
		# Music related objects
		self.notations = [enNotation, itNotation, deNotation, frNotation, ptNotation]
		# Other objects
		self.format = SongFormat()
		self.decoratorFormat = StandardVerseNumbers.Format(self.format, _("Chorus"))
		self.decorator = StandardVerseNumbers.Decorator(self.decoratorFormat)
		self.previewCanvas = PreviewCanvas(self.frame, self.format, self.decorator)
		self.AddMainPane(self.text)
		self.previewCanvas.panel.SetSize(wx.Size(400, 800))
		self.previewCanvasPane = self.AddPane(self.previewCanvas.panel, wx.aui.AuiPaneInfo().Right(), _('Preview'), 'preview')
		self.previewCanvasPane.BestSize(wx.Size(400,800))
		self.mainToolBar = wx.ToolBar(self.frame, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
			wx.TB_FLAT | wx.TB_NODIVIDER)
		self.mainToolBar.SetToolBitmapSize(wx.Size(16, 16))
		self.mainToolBar.AddTool(wx.xrc.XRCID('new'), wx.BitmapFromImage(wx.Image(glb.AddPath(glb.AddPath("img/new.png")))),
			shortHelpString = _("New"),
			longHelpString = _("Create a new song")
		)
		self.mainToolBar.AddTool(wx.xrc.XRCID('open'), wx.BitmapFromImage(wx.Image(glb.AddPath("img/open.png"))),
			shortHelpString = _("Open"),
			longHelpString = _("Open an existing song")
		)
		self.mainToolBar.AddTool(wx.xrc.XRCID('save'), wx.BitmapFromImage(wx.Image(glb.AddPath("img/save.png"))),
			shortHelpString = _("Save"),
			longHelpString = _("Save song with the current filename")
		)
		self.mainToolBar.AddSeparator()
		self.undoTool = wx.xrc.XRCID('undo')
		self.mainToolBar.AddTool(self.undoTool, wx.BitmapFromImage(wx.Image(glb.AddPath("img/undo.png"))),
			shortHelpString = _("Undo"),
			longHelpString = _("Undo last edit")
		)
		self.redoTool = wx.xrc.XRCID('redo')
		self.mainToolBar.AddTool(self.redoTool, wx.BitmapFromImage(wx.Image(glb.AddPath("img/redo.png"))),
			shortHelpString = _("Redo"),
			longHelpString = _("Redo previously undone edit")
		)
		self.mainToolBar.AddSeparator()
		self.cutTool = wx.xrc.XRCID('cut')
		self.mainToolBar.AddTool(self.cutTool, wx.BitmapFromImage(wx.Image(glb.AddPath("img/cut.png"))),
			shortHelpString = _("Cut"),
			longHelpString = _("Move selected text in the clipboard")
		)
		self.copyTool = wx.xrc.XRCID('copy')
		self.mainToolBar.AddTool(self.copyTool, wx.BitmapFromImage(wx.Image(glb.AddPath("img/copy.png"))),
			shortHelpString = _("Copy"),
			longHelpString = _("Copy selected text in the clipboard")
		)
		self.mainToolBar.AddTool(wx.xrc.XRCID('copyAsImage'), wx.BitmapFromImage(wx.Image(glb.AddPath("img/copyAsImage2.png"))),
			shortHelpString = _("Copy as Image"),
			longHelpString = _("Copy the whole FORMATTED song (or selected verses) to the clipboard")
		)
		self.pasteTool = wx.xrc.XRCID('paste')
		self.mainToolBar.AddTool(self.pasteTool, wx.BitmapFromImage(wx.Image(glb.AddPath("img/paste.png"))),
			shortHelpString = _("Paste"),
			longHelpString = _("Read text from the clipboard and place it at the cursor position")
		)
		self.mainToolBar.Realize()
		self.mainToolBarPane = self.AddPane(self.mainToolBar, wx.aui.AuiPaneInfo().ToolbarPane().Top().Row(1).Position(1), _('Standard'), 'standard')		
		self.formatToolBar = wx.ToolBar(self.frame, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
			wx.TB_FLAT | wx.TB_NODIVIDER)
		self.fontChooser = FontComboBox(self.formatToolBar, -1, self.format.face)
		self.formatToolBar.AddControl(self.fontChooser)
		self.frame.Bind(wx.EVT_COMBOBOX, self.OnFontSelected, self.fontChooser)
		wx.UpdateUIEvent.SetUpdateInterval(500)		
		self.frame.Bind(wx.EVT_UPDATE_UI, self.OnIdle, self.frame)
		self.frame.Bind(wx.EVT_TEXT_CUT, self.OnTextCutCopy, self.text)
		self.frame.Bind(wx.EVT_TEXT_COPY, self.OnTextCutCopy, self.text)
		self.fontChooser.Bind(wx.EVT_TEXT_ENTER, self.OnFontSelected, self.fontChooser)
		self.fontChooser.Bind(wx.EVT_KILL_FOCUS, self.OnFontSelected, self.fontChooser)
		self.formatToolBar.AddTool(wx.xrc.XRCID('title'), wx.BitmapFromImage(wx.Image(glb.AddPath("img/title.png"))),
			shortHelpString = _("Insert title"),
			longHelpString = _("Insert a command to display song title")
		)
		self.formatToolBar.AddTool(wx.xrc.XRCID('chord'), wx.BitmapFromImage(wx.Image(glb.AddPath("img/chord.png"))),
			shortHelpString = _("Insert chord"),
			longHelpString = _("Insert square brackets that will host a chord")
		)
		self.formatToolBar.AddTool(wx.xrc.XRCID('chorus'), wx.BitmapFromImage(wx.Image(glb.AddPath("img/chorus.png"))),
			shortHelpString = _("Insert chorus"),
			longHelpString = _("Insert a couple of commands that will contain chorus")
		)
		labelVersesTool = self.formatToolBar.AddTool(wx.xrc.XRCID('labelVerses'), wx.BitmapFromImage(wx.Image(glb.AddPath("img/labelVerses.png"))), isToggle=True,
			shortHelpString = _("Insert comment"),
			longHelpString = _("Insert a command to display a comment")
		)
		self.labelVersesToolId = labelVersesTool.GetId()
		self.formatToolBar.Realize()
		self.formatToolBarPane = self.AddPane(self.formatToolBar, wx.aui.AuiPaneInfo().ToolbarPane().Top().Row(1).Position(2), _('Format'), 'format')
		self.BindMyMenu()
		self.cutMenuId = xrc.XRCID('cut')
		self.copyMenuId = xrc.XRCID('copy')
		self.pasteMenuId = xrc.XRCID('paste')
		self.labelVersesMenuId = xrc.XRCID('labelVerses')
		self.findReplaceDialog = None
		self.LoadConfig()
		self.FinalizePaneInitialization()
		# Reassign caption value to override caption saved in preferences (it could be another language)
		self.previewCanvasPane.caption = _('Preview')
		self.mainToolBar.caption = _('Standard')
		self.formatToolBar.caption = _('Format')	
		
	def BindMyMenu(self):
		"""Bind a menu item, by xrc name, to a handler"""
		def Bind(handler, xrcname):
			self.Bind(wx.EVT_MENU, handler, xrcname)
			
		Bind(self.OnExportAsPng, 'exportAsPng')
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
		Bind(self.OnSelectNextChord, 'selectNextChord')
		Bind(self.OnSelectPreviousChord, 'selectPreviousChord')
		Bind(self.OnMoveChordRight, 'moveChordRight')
		Bind(self.OnMoveChordLeft, 'moveChordLeft')
		Bind(self.OnTitle, 'title')
		Bind(self.OnChord, 'chord')
		Bind(self.OnChorus, 'chorus')
		Bind(self.OnComment, 'comment')
		Bind(self.OnFormatFont, 'font')
		Bind(self.OnLabelVerses, 'labelVerses')
		Bind(self.OnChorusLabel, 'chorusLabel')
		Bind(self.OnTranspose, 'transpose')
		Bind(self.OnChangeChordNotation, 'changeChordNotation')
		Bind(self.OnOptions, 'options')
		Bind(self.OnGuide, 'guide')
		Bind(self.OnNewsAndUpdates, 'newsAndUpdates')
		Bind(self.OnDonate, 'donate')

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
		
	def DrawOnDC(self, dc):
		r = Renderer(self.format, self.decorator)
		start, end = self.text.GetSelection()
		if start == end:
			w, h = r.Render(self.text.GetText(), dc)
		else:
			w, h = r.Render(self.text.GetText(), dc, self.text.LineFromPosition(start), self.text.LineFromPosition(end))
		return w, h
		
	def AskExportFileName(self, type, ext):
		"""Ask the filename (without saving); return None if user cancels, the file name ow"""
		leave = False;
		consensus = False;
		while not leave:
			dlg = wx.FileDialog(
				self.frame,
				"Choose a name for the output file",
				"",
				os.path.splitext(self.document)[0],
				"%s files (*.%s)|*.%s|All files (*.*)|*.*" % (type, ext, ext),
				wx.FD_SAVE
			)

			if dlg.ShowModal() == wx.ID_OK:

				fn = dlg.GetPath()
				if os.path.isfile(fn):
					msg = "File \"%s\" already exists. Do you want to overwrite it?" % (fn, )
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
			return fn
		else:
			return None
		
	def OnExportAsPng(self, evt):
		n = self.AskExportFileName(_("PNG image"), "png")
		if n is not None:
			dc = wx.MemoryDC()
			w, h = self.DrawOnDC(dc)
			b = wx.EmptyBitmap(w, h)
			dc = wx.MemoryDC(b)
			dc.SetBackground(wx.WHITE_BRUSH);
			dc.Clear();
			self.DrawOnDC(dc)
			i = wx.ImageFromBitmap(b)
			i.SaveFile(n, wx.BITMAP_TYPE_PNG)

	def OnUpdateUI(self, evt):
		self.UpdateEverything()
		evt.Skip()

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
		
	def OnTextCutCopy(self, evt):
		self.UpdateCutCopyPaste()
		evt.Skip()
		
	def OnCopy(self, evt):
		self.text.Copy()

	def OnCopyAsImage(self, evt):
		dc = wx.MetaFileDC()
		self.DrawOnDC(dc)
		m = dc.Close()
		m.SetClipboard(dc.MaxX(), dc.MaxY())
		
	def OnPaste(self, evt):
		self.text.Paste()
	
	def OnFind(self, evt):
		self.findReplaceDialog = SongpressFindReplaceDialog(self)
		
	def OnFindNext(self, evt):
		if self.findReplaceDialog != None:
			self.findReplaceDialog.down = True
			self.findReplaceDialog.FindNext()

	def OnFindPrevious(self, evt):
		if self.findReplaceDialog != None:
			self.findReplaceDialog.down = False
			self.findReplaceDialog.FindNext()

	def OnReplace(self, evt):
		self.findReplaceDialog = SongpressFindReplaceDialog(self, True)
		
	def OnSelectNextChord(self, evt):
		self.text.SelectNextChord()
	
	def OnSelectPreviousChord(self, evt):
		self.text.SelectPreviousChord()
		
	def OnMoveChordRight(self, evt):
		r = self.text.GetChordUnderCursor()
		if r is not None:
			n = self.text.GetLength()
			s, e, c = r
			if e < n:
				self.text.BeginUndoAction()
				self.text.SetSelection(e, e + 1)
				l = self.text.GetTextRange(e, e + 1)
				self.text.ReplaceSelection('')
				self.text.SetSelection(s, s)
				self.text.ReplaceSelection(l)
				self.text.SetSelection(s + 2, s + 2)
				self.text.EndUndoAction()
		
	def OnMoveChordLeft(self, evt):
		r = self.text.GetChordUnderCursor()
		if r is not None:
			s, e, c = r
			if s > 0:
				self.text.BeginUndoAction()
				self.text.SetSelection(s - 1, s)
				l = self.text.GetTextRange(s - 1, s)
				self.text.ReplaceSelection('')
				self.text.SetSelection(e - 1, e - 1)
				self.text.ReplaceSelection(l)
				self.text.SetSelection(s, s)
				self.text.EndUndoAction()
	
	def OnFontSelected(self, evt):
		font = self.fontChooser.GetValue()
		self.SetFont(font)
		evt.Skip()
		
	def OnGuide(self, evt):
		helpfile = os.path.join("help", "songpress-%s.chm" % (i18n.getLang(), ))
		subprocess.Popen("hh " + glb.AddPath(helpfile))
		
	def OnIdle(self, evt):
		self.mainToolBar.EnableTool(self.pasteTool, self.text.CanPaste())
		self.menuBar.Enable(self.pasteMenuId, self.text.CanPaste())
		evt.Skip()
		
	def OnNewsAndUpdates(self, evt):
		wx.LaunchDefaultBrowser(_("http://www.skeed.it/songpress.html#News"))
		
	def OnDonate(self, evt):
		wx.LaunchDefaultBrowser(_("http://www.skeed.it/songpress.html#donate"))
		
	def SetFont(self, font):
		self.fontChooser.SetValue(font)	
		self.format.face = font
		self.format.comment.face = font
		self.format.chord.face = font
		self.format.chorus.face = font
		self.format.chorus.chord.face = font
		self.format.chorus.comment.face = font
		for v in self.format.verse:
			v.face = font
			v.chord.face = font
			v.comment.face = font
		self.format.title.face = font
		self.decoratorFormat.face = font
		self.decoratorFormat.chorus.face = font		
		self.previewCanvas.Refresh(self.text.GetText())
		self.config.SetPath('/Format/Font')
		self.config.Write('FontFace', font)
		
	def OnFormatFont(self, evt):
		f = FontFaceDialog(self.frame, wx.ID_ANY, _("Songpress"), self.format, self.decorator, self.decoratorFormat)
		if f.ShowModal() == wx.ID_OK:
			self.SetFont(f.GetValue())
			
	def OnTranspose(self, evt):
		t = MyTransposeDialog(self.frame, self.notations, self.text.GetTextOrSelection())
		if t.ShowModal() == wx.ID_OK:
			self.text.ReplaceTextOrSelection(t.GetTransposed())

	def OnChangeChordNotation(self, evt):
		t = MyNotationDialog(self.frame, self.notations, self.text.GetTextOrSelection())
		if t.ShowModal() == wx.ID_OK:
			self.text.ReplaceTextOrSelection(t.ChangeChordNotation())
			
	def OnOptions(self, evt):
		f = PreferencesDialog(self.frame, wx.ID_ANY, _("Songpress options"), self.notations)
		if f.ShowModal() == wx.ID_OK:
			face, s = f.GetFont()
			self.text.SetFont(face, s)
			self.config.SetPath('/Editor')
			self.config.Write('Face', face)
			self.config.Write('Size', str(s))
			
			l = f.GetLanguage()
			lang = i18n.getLang()
			if l != lang:
				msg = _("Language settings will be applied when you restart Songpress.")
				d = wx.MessageDialog(self.frame, msg, _("Songpress"), wx.ICON_INFORMATION | wx.OK)
				d.ShowModal()
			self.config.SetPath("/App")
			self.config.Write("locale", l)
			self.SetDefaultNotation(f.GetNotation())

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
	
	def OnLabelVerses(self, evt):
		self.labelVerses = not self.labelVerses
		self.CheckLabelVerses()
		
	def OnChorusLabel(self, evt):
		c = self.decoratorFormat.GetChorusLabel()
		msg = _("Please enter a label for chorus")
		d = wx.TextEntryDialog(self.frame, msg, _("Songpress"), c)
		if d.ShowModal() == wx.ID_OK:
			c = d.GetValue()
			self.config.SetPath('/Format')
			self.config.Write('ChorusLabel', c)
			self.decoratorFormat.SetChorusLabel(c)
			self.previewCanvas.Refresh(self.text.GetText())
			
	def CheckLabelVerses(self):
		self.formatToolBar.ToggleTool(self.labelVersesToolId, self.labelVerses)
		self.menuBar.Check(self.labelVersesMenuId, self.labelVerses)
		self.config.SetPath('/Format/Style')
		if self.labelVerses:
			self.previewCanvas.SetDecorator(self.decorator)
			self.config.Write('LabelVerses', "1")
		else:
			self.previewCanvas.SetDecorator(SongDecorator())
			self.config.Write('LabelVerses', "0")
		self.previewCanvas.Refresh(self.text.GetText())
		
	def SetDefaultNotation(self, notation):
		self.notations = [x for x in self.notations if x.id == notation] + [x for x in self.notations if x.id != notation]
		self.config.SetPath('/Editor')
		self.config.Write('DefaultNotation', notation)
		
	def LoadConfig(self):
		self.config.SetPath('/Format')
		l = self.config.Read('ChorusLabel')	
		if l:
			self.decoratorFormat.SetChorusLabel(l)
		self.config.SetPath('/Format/Font')
		face = self.config.Read('Face')
		if face:
			self.SetFont(face)
		self.config.SetPath('/Format/Style')
		labelVerses = self.config.Read('LabelVerses')
		if labelVerses:
			self.labelVerses = bool(int(labelVerses))
			self.CheckLabelVerses()
		else:
			self.labelVerses = True
			self.CheckLabelVerses()
		self.config.SetPath('/Editor')
		f = self.config.Read('Face')
		s = self.config.Read('Size')
		if not f:
			f = "Lucida Console"
			s = '12'
			self.config.Write('Face', f)
			self.config.Write('Size', s)
		self.text.SetFont(f, int(s))
		n = self.config.Read('DefaultNotation')
		if n:
			self.notations = [x for x in self.notations if x.id == n] + [x for x in self.notations if x.id != n]
		else:
			lang = i18n.getLang()
			if lang in defaultLangNotation:
				n = defaultLangNotation[lang].id
				self.notations = [x for x in self.notations if x.id == n] + [x for x in self.notations if x.id != n]
	
