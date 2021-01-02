###############################################################
# Name:			 SongpressFrame.py
# Purpose:	 Main frame for Songpress
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-16
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

import wx
# import wx.aui as aui
from wx.lib.agw import aui
import wx.adv
from wx import xrc
from SDIMainFrame import *
from Editor import *
from PreviewCanvas import *
from Renderer import *
from FontComboBox import FontComboBox
from FontFaceDialog import FontFaceDialog
from MyPreferencesDialog import MyPreferencesDialog
from HTML import HtmlExporter, TabExporter
from Transpose import *
from MyTransposeDialog import *
from MyNotationDialog import *
from MyNormalizeDialog import *
from MyListDialog import MyListDialog
import MyUpdateDialog
from Globals import glb
from Preferences import Preferences
import subprocess
import os
import os.path
import i18n
import platform

if platform.system() == 'Windows':
	import wx.msw

i18n.register('SongpressFrame')


class SongpressFindReplaceDialog(object):
	def __init__(self, owner, replace=False):
		object.__init__(self)
		self.down = True
		self.st = ''
		self.data = wx.FindReplaceData(wx.FR_DOWN)
		self.owner = owner
		self.flags = 0
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
		self.st = self.data.GetFindString()
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
		r = self.data.GetReplaceString()
		self.st = self.data.GetFindString()
		if self.owner.text.GetSelectedText().lower() == self.st.lower():
			self.owner.text.ReplaceSelection(r)
			self.FindNext()

	def OnReplaceAll(self, evt):
		self.owner.text.BeginUndoAction()
		s = self.data.GetFindString()
		r = self.data.GetReplaceString()
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


if platform.system() == 'Linux':
    # Apparently there is a problem with linux FileOpen dialog box in wxPython:
    # it does not support multiple extensions in a filter.
    _import_formats = [
        (_("All supported files"), ["crd", "cho", "chordpro", "chopro", "tab", "cpm"]),
        #(_("Chordpro files (*.crd)"), ["crd"]),
        #(_("Tab files (*.tab)"), ["tab"]),
        #(_("Chordpro files (*.cho)"), ["cho"]),
        #(_("Chordpro files (*.chordpro)"), ["chordpro"]),
        #(_("Chordpro files (*.chopro)"), ["chopro"]),
        #(_("Chordpro files (*.pro)"), ["pro"]),
    ]
else:
    _import_formats = [
        (_("All supported files"), ["crd", "cho", "chordpro", "chopro", "pro", "tab"]),
        (_("Chordpro files (*.crd, *.cho, *.chordpro, *.chopro, *.pro)"), ["crd", "cho", "chordpro", "chopro", "pro"]),
        (_("Tab files (*.tab)"), ["tab"]),
    ]


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
			glb.VERSION,
			_("http://www.skeed.it/songpress"),
			(_(u"Copyright (c) 2009-{year} Luca Allulli - Skeed\nLocalization:\n{translations}")).format(
				year=glb.YEAR,
				translations="\n".join([u"- {}: {}".format(glb.languages[x], glb.translators[x]) for x in glb.languages])
			),
			_("Licensed under the terms and conditions of the GNU General Public License, version 2"),
			_(
				"Special thanks to:\n  * The Pyhton programming language (http://www.python.org)\n  * wxWidgets (http://www.wxwidgets.org)\n  * wxPython (http://www.wxpython.org)\n  * Editra (http://editra.org/) (for the error reporting dialog and... the editor itself!)\n  * python-pptx (for PowerPoint export)"),
			_import_formats,
		)
		self.pref = Preferences()
		self.SetDefaultExtension(self.pref.defaultExtension)
		self.text = Editor(self)
		dt = SDIDropTarget(self)
		self.text.SetDropTarget(dt)
		self.frame.Bind(wx.stc.EVT_STC_UPDATEUI, self.OnUpdateUI, self.text)
		# Other objects
		self.previewCanvas = PreviewCanvas(self.frame, self.pref.format, self.pref.notations, self.pref.decorator)
		self.AddMainPane(self.text)
		self.AddPane(self.previewCanvas.main_panel, aui.AuiPaneInfo().Right().BestSize(240, 400), _('Preview'), 'preview')
		if self.previewCanvas.link is not None:
			self.previewCanvas.main_panel.Bind(wx.adv.EVT_HYPERLINK, self.OnCopyAsImage, self.previewCanvas.link)
		self.mainToolBar = aui.AuiToolBar(self.frame, wx.ID_ANY, wx.DefaultPosition, agwStyle=aui.AUI_TB_PLAIN_BACKGROUND)
		self.mainToolBar.SetToolBitmapSize(wx.Size(16, 16))
		self.AddTool(self.mainToolBar, 'new', 'img/new.png', _("New"), _("Create a new song"))
		self.AddTool(self.mainToolBar, 'open', 'img/open.png', _("Open"), _("Open an existing song"))
		self.AddTool(self.mainToolBar, 'save', 'img/save.png', _("Save"), _("Save song with the current filename"))
		self.mainToolBar.AddSeparator()
		self.undoTool = self.AddTool(self.mainToolBar, 'undo', 'img/undo.png', _("Undo"), _("Undo last edit"))
		self.redoTool = self.AddTool(self.mainToolBar, 'redo', 'img/redo.png', _("Redo"), _("Redo previously undone edit"))
		self.redoTool = wx.xrc.XRCID('redo')
		self.mainToolBar.AddSeparator()
		self.cutTool = self.AddTool(self.mainToolBar, 'cut', 'img/cut.png', _("Cut"),
																_("Move selected text in the clipboard"))
		self.copyTool = self.AddTool(self.mainToolBar, 'copy', 'img/copy.png', _("Copy"),
																 _("Copy selected text in the clipboard"))
		self.copyOnlyTextTool = wx.xrc.XRCID('copyOnlyText')
		if platform.system() == 'Windows':
			self.AddTool(self.mainToolBar, 'copyAsImage', 'img/copyAsImage2.png', _("Copy as Image"),
									 _("Copy the whole FORMATTED song (or selected verses) to the clipboard"))
		self.pasteTool = self.AddTool(self.mainToolBar, 'paste', 'img/paste.png', _("Paste"),
																	_("Read text from the clipboard and place it at the cursor position"))
		self.pasteChordsTool = self.AddTool(self.mainToolBar, 'pasteChords', 'img/pasteChords.png', _("PasteChords"),
																				_("Integrate chords of copied text into current selection"))
		self.mainToolBar.Realize()
		self.mainToolBarPane = self.AddPane(self.mainToolBar, aui.AuiPaneInfo().ToolbarPane().Top().Row(1).Position(1),
																				_('Standard'), 'standard')
		self.formatToolBar = aui.AuiToolBar(self.frame, wx.ID_ANY, agwStyle=aui.AUI_TB_PLAIN_BACKGROUND)
		self.formatToolBar.SetExtraStyle(aui.AUI_TB_PLAIN_BACKGROUND)
		self.fontChooser = FontComboBox(self.formatToolBar, -1, self.pref.format.face)
		self.formatToolBar.AddControl(self.fontChooser)
		self.frame.Bind(wx.EVT_COMBOBOX, self.OnFontSelected, self.fontChooser)
		wx.UpdateUIEvent.SetUpdateInterval(500)
		self.frame.Bind(wx.EVT_UPDATE_UI, self.OnIdle, self.frame)
		self.frame.Bind(wx.EVT_TEXT_CUT, self.OnTextCutCopy, self.text)
		self.frame.Bind(wx.EVT_TEXT_COPY, self.OnTextCutCopy, self.text)
		self.fontChooser.Bind(wx.EVT_TEXT_ENTER, self.OnFontSelected, self.fontChooser)
		self.fontChooser.Bind(wx.EVT_KILL_FOCUS, self.OnFontSelected, self.fontChooser)
		self.AddTool(self.formatToolBar, 'title', 'img/title.png', _("Insert title"),
								 _("Insert a command to display song title"))
		self.AddTool(self.formatToolBar, 'chord', 'img/chord.png', _("Insert chord"),
								 _("Insert square brackets that will host a chord"))
		self.AddTool(self.formatToolBar, 'chorus', 'img/chorus.png', _("Insert chorus"),
								 _("Insert a couple of commands that will contain chorus"))
		self.AddTool(
			self.formatToolBar,
			'verseWithCustomLabelOrWithoutLabel',
			'img/verse.png',
			_("Insert verse with custom label or without label"),
			_("Insert a commands that will display a verse with a custom label"),
		)
		labelVersesTool = self.formatToolBar.AddToggleTool(  # AddToggleTool (agw) or AddTool
			wx.xrc.XRCID('labelVerses'),
			wx.Bitmap(wx.Image(glb.AddPath("img/labelVerses.png"))),
			wx.NullBitmap,
			True,
			None,
			_("Show verse labels"),
			_("Show or hide verse and chorus labels"),
		)
		self.labelVersesToolId = labelVersesTool.GetId()
		showChordsIcon = wx.StaticBitmap(self.formatToolBar, -1, wx.Bitmap(wx.Image(glb.AddPath('img/showChords.png'))))
		self.formatToolBar.AddControl(showChordsIcon)
		self.showChordsChooser = wx.Slider(self.formatToolBar, -1, 0, 0, 2, wx.DefaultPosition, (100, -1),
																			 wx.SL_AUTOTICKS | wx.SL_HORIZONTAL)
		tt1 = wx.ToolTip(_("Hide or show chords in formatted song"))
		tt2 = wx.ToolTip(_("Hide or show chords in formatted song"))
		self.showChordsChooser.SetToolTip(tt1)
		showChordsIcon.SetToolTip(tt2)
		self.frame.Bind(wx.EVT_SCROLL, self.OnFontSelected, self.showChordsChooser)
		self.formatToolBar.AddControl(
			self.showChordsChooser,
			"pippo"
		)
		self.formatToolBar.Realize()
		self.formatToolBarPane = self.AddPane(self.formatToolBar, aui.AuiPaneInfo().ToolbarPane().Top().Row(1).Position(2),
																					_('Format'), 'format')
		self.BindMyMenu()
		self.frame.Bind(EVT_TEXT_CHANGED, self.OnTextChanged)
		self.exportMenuId = xrc.XRCID('export')
		self.exportToClipboardAsAVectorImage = xrc.XRCID('exportToClipboardAsAVectorImage')
		self.exportAsEmfMenuId = xrc.XRCID('exportAsEmf')
		self.cutMenuId = xrc.XRCID('cut')
		self.copyMenuId = xrc.XRCID('copy')
		self.copyAsImageMenuId = xrc.XRCID('copyAsImage')
		self.pasteMenuId = xrc.XRCID('paste')
		self.pasteChordsMenuId = xrc.XRCID('pasteChords')
		self.removeChordsMenuId = xrc.XRCID('removeChords')
		self.labelVersesMenuId = xrc.XRCID('labelVerses')
		self.noChordsMenuId = xrc.XRCID('noChords')
		self.oneVerseForEachChordPatternMenuId = xrc.XRCID('oneVerseForEachChordPattern')
		self.wholeSongMenuId = xrc.XRCID('wholeSong')
		if platform.system() != 'Windows':
			self.menuBar.GetMenu(0).FindItemById(self.exportMenuId).GetSubMenu().Delete(self.exportToClipboardAsAVectorImage)
			self.menuBar.GetMenu(1).Delete(self.copyAsImageMenuId)
			self.menuBar.GetMenu(0).FindItemById(self.exportMenuId).GetSubMenu().Delete(self.exportAsEmfMenuId)
		self.findReplaceDialog = None
		self.CheckLabelVerses()
		self.SetFont()
		self.text.SetFont(self.pref.editorFace, self.pref.editorSize)
		self.FinalizePaneInitialization()
		# Reassign caption value to override caption saved in preferences (it could be another language)
		self._mgr.GetPane('preview').caption = _('Preview')
		self._mgr.GetPane('standard').caption = _('Standard')
		self._mgr.GetPane('format').caption = _('Format')
		if 'firstTimeEasyKey' in self.pref.notices:
			msg = _(
				"You are not a skilled guitarist? Songpress can help you: when you open a song, it can detect if chords are difficult. If this is the case, Songpress will alert you, and offer to transpose your song to the easiest key, automatically.\n\nDo you want to turn this option on?")
			d = wx.MessageDialog(self.frame, msg, _("Songpress"), wx.YES_NO | wx.ICON_QUESTION)
			if d.ShowModal() == wx.ID_YES:
				self.pref.autoAdjustEasyKey = True
				msg = _(
					"Please take a minute to set up your skill as a guitarist. For each group of chords, tell Songpress how much you like them.")
				d = wx.MessageDialog(self.frame, msg, _("Songpress"), wx.OK)
				d.ShowModal()
				f = MyPreferencesDialog(self.frame, self.pref, easyChords)
				f.notebook.SetSelection(1)
				if f.ShowModal() == wx.ID_OK:
					self.text.SetFont(self.pref.editorFace, int(self.pref.editorSize))
					self.SetDefaultExtension(self.pref.defaultExtension)
		MyUpdateDialog.check_and_update(self.frame, self.pref)

	def BindMyMenu(self):
		"""Bind a menu item, by xrc name, to a handler"""

		def Bind(handler, xrcname):
			self.Bind(wx.EVT_MENU, handler, xrcname)

		Bind(self.OnCopyAsImage, 'exportToClipboardAsAVectorImage')
		Bind(self.OnExportAsSvg, 'exportAsSvg')
		Bind(self.OnExportAsEmf, 'exportAsEmf')
		Bind(self.OnExportAsPng, 'exportAsPng')
		Bind(self.OnExportAsHtml, 'exportAsHtml')
		Bind(self.OnExportAsTab, 'exportAsTab')
		Bind(self.OnExportAsPptx, 'exportAsPptx')
		Bind(self.OnUndo, 'undo')
		Bind(self.OnRedo, 'redo')
		Bind(self.OnCut, 'cut')
		Bind(self.OnCopy, 'copy')
		Bind(self.OnCopyAsImage, 'copyAsImage')
		Bind(self.OnCopyOnlyText, 'copyOnlyText')
		Bind(self.OnPaste, 'paste')
		Bind(self.OnPasteChords, 'pasteChords')
		Bind(self.OnFind, 'find')
		Bind(self.OnFindNext, 'findNext')
		Bind(self.OnFindPrevious, 'findPrevious')
		Bind(self.OnReplace, 'replace')
		Bind(self.OnSelectNextChord, 'selectNextChord')
		Bind(self.OnSelectPreviousChord, 'selectPreviousChord')
		Bind(self.OnMoveChordRight, 'moveChordRight')
		Bind(self.OnMoveChordLeft, 'moveChordLeft')
		Bind(self.OnRemoveChords, 'removeChords')
		Bind(self.OnIntegrateChords, 'integrateChords')
		Bind(self.OnTitle, 'title')
		Bind(self.OnSubtitle, 'subtitle')
		Bind(self.OnChord, 'chord')
		Bind(self.OnChorus, 'chorus')
		Bind(self.OnVerse, 'verseWithCustomLabelOrWithoutLabel')
		Bind(self.OnComment, 'comment')
		Bind(self.OnFormatFont, 'font')
		Bind(self.OnLabelVerses, 'labelVerses')
		Bind(self.OnChorusLabel, 'chorusLabel')
		Bind(self.OnNoChords, 'noChords')
		Bind(self.OnOneVerseForEachChordPattern, 'oneVerseForEachChordPattern')
		Bind(self.OnWholeSong, 'wholeSong')
		Bind(self.OnTranspose, 'transpose')
		Bind(self.OnSimplifyChords, 'simplifyChords')
		Bind(self.OnChangeChordNotation, 'changeChordNotation')
		Bind(self.OnNormalizeChords, 'cleanupChords')
		Bind(self.OnConvertTabToChordpro, 'convertTabToChordpro')
		Bind(self.OnRemoveSpuriousBlankLines, 'removeSpuriousBlankLines')
		Bind(self.OnOptions, 'options')
		Bind(self.OnGuide, 'guide')
		Bind(self.OnNewsAndUpdates, 'newsAndUpdates')
		Bind(self.OnDonate, 'donate')

	def AddTool(self, toolbar, resource_string, icon_path, label, help):
		tool = wx.xrc.XRCID(resource_string)
		toolbar.AddTool(
			tool,
			label,
			wx.Bitmap(wx.Image(glb.AddPath(icon_path))),
			wx.NullBitmap,
			wx.ITEM_NORMAL,
			label,
			help,
			None
		)
		return tool

	def New(self):
		self.text.AutoChangeMode(True)
		self.text.New()
		self.text.AutoChangeMode(False)
		self.UpdateEverything()

	def Open(self):
		self.text.AutoChangeMode(True)
		self.text.Open()
		self.text.AutoChangeMode(False)
		self.UpdateEverything()
		self.AutoAdjust(0, self.text.GetLength())

	def Save(self):
		self.text.Save()
		self.UpdateEverything()

	def SavePreferences(self):
		self.pref.Save()

	def UpdateUndoRedo(self):
		self.mainToolBar.EnableTool(self.undoTool, self.text.CanUndo())
		self.mainToolBar.EnableTool(self.redoTool, self.text.CanRedo())

	def UpdateCutCopyPaste(self):
		s, e = self.text.GetSelection()
		self.mainToolBar.EnableTool(self.cutTool, s != e)
		self.menuBar.Enable(self.cutMenuId, s != e)
		self.mainToolBar.EnableTool(self.copyTool, s != e)
		self.menuBar.Enable(self.copyOnlyTextTool, s != e)
		self.menuBar.Enable(self.copyMenuId, s != e)
		if platform.system() == 'Windows':
			cp = self.text.CanPaste()
		else:
			# Workaround for weird error in wxGTK
			cp = True
		self.mainToolBar.EnableTool(self.pasteTool, cp)
		self.menuBar.Enable(self.pasteMenuId, cp)
		self.mainToolBar.EnableTool(self.pasteChordsTool, cp)
		self.menuBar.Enable(self.pasteChordsMenuId, cp)
		self.menuBar.Enable(self.removeChordsMenuId, s != e)

	def UpdateEverything(self):
		self.UpdateUndoRedo()
		self.UpdateCutCopyPaste()

	def TextUpdated(self):
		self.previewCanvas.Refresh(self.text.GetText())

	# self.UpdateEverything()

	def DrawOnDC(self, dc):
		decorator = self.pref.decorator if self.pref.labelVerses else SongDecorator()
		r = Renderer(self.pref.format, decorator, self.pref.notations)
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
					msg = "File \"%s\" already exists. Do you want to overwrite it?" % (fn,)
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
					else:  # wxID_YES
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
			dc = wx.MemoryDC(wx.EmptyBitmap(1, 1))
			scale = 1
			w, h = self.DrawOnDC(dc)
			b = wx.EmptyBitmap(w * scale, h * scale)
			dc = wx.MemoryDC(b)
			dc.SetUserScale(scale, scale)
			dc.SetBackground(wx.WHITE_BRUSH);
			dc.Clear();
			self.DrawOnDC(dc)
			i = wx.ImageFromBitmap(b)
			i.SaveFile(n, wx.BITMAP_TYPE_PNG)

	def OnExportAsHtml(self, evt):
		n = self.AskExportFileName(_("HTML file"), "html")
		if n is not None:
			h = HtmlExporter(self.pref.format)
			r = Renderer(self.pref.format, h, self.pref.notations)
			start, end = self.text.GetSelection()
			if start == end:
				r.Render(self.text.GetText(), None)
			else:
				r.Render(self.text.GetText(), None, self.text.LineFromPosition(start), self.text.LineFromPosition(end))
			with open(n, "w", encoding='utf-8') as f:
				f.write(h.getHtml())

	def OnExportAsTab(self, evt):
		n = self.AskExportFileName(_("TAB file"), "tab")
		if n is not None:
			t = TabExporter(self.pref.format)
			r = Renderer(self.pref.format, t, self.pref.notations)
			start, end = self.text.GetSelection()
			if start == end:
				r.Render(self.text.GetText(), None)
			else:
				r.Render(self.text.GetText(), None, self.text.LineFromPosition(start), self.text.LineFromPosition(end))
			with open(n, "w", encoding='utf-8') as f:
				f.write(t.getTab())

	def OnExportAsSvg(self, evt):
		n = self.AskExportFileName(_("SVG image"), "svg")
		if n is not None:
			dc = wx.MemoryDC(wx.Bitmap(1, 1))
			w, h = self.DrawOnDC(dc)
			dc = wx.SVGFileDC(n, w, h)
			self.DrawOnDC(dc)

	def OnExportAsEmf(self, evt):
		n = self.AskExportFileName(_("Enhanced Metafile"), "emf")
		if n is not None:
			dc = wx.msw.MetafileDC(n)
			self.DrawOnDC(dc)
			dc.Close()

	def OnExportAsEps(self, evt):
		n = self.AskExportFileName(_("EPS image"), "eps")
		if n is not None:
			pd = wx.PrintData()
			pd.SetPaperId(wx.PAPER_NONE)
			pd.SetPrintMode(wx.PRINT_MODE_FILE)
			pd.SetFilename(n)
			dc = wx.PostScriptDC(pd)
			dc.StartDoc(_("Exporting image as EPS..."))
			self.DrawOnDC(dc)
			dc.EndDoc()


	def OnExportAsPptx(self, evt):
		try:
			import songimpress
		except ImportError:
			msg = _("Please install the python-pptx module to use this feature")
			d = wx.MessageDialog(self.frame, msg, "Songpress", wx.OK | wx.ICON_ERROR)
			d.ShowModal()
			return
		text = replaceTitles(self.text.GetTextOrSelection(), '---')
		text = removeChordPro(text).strip()
		if text != '':
			template_rel = os.path.join('templates', 'slides')
			template_paths = [f for f in glb.ListLocalGlobalDir(template_rel) if f[-5:].upper() == '.PPTX']
			template_names = [os.path.split(f)[1][:-5] for f in template_paths]
			mld = MyListDialog(
				self.frame,
				_("Please select a template for your PowerPoint presentation:"),
				_("Export as PowerPoint"),
				template_names,
			)
			if mld.ShowModal() == wx.ID_OK:
				output_file = self.AskExportFileName(_("PPTX presentation"), "pptx")
				if output_file is not None:
					i = mld.GetSelectedIndex()
					songimpress.to_presentation(text.splitlines(), output_file, template_paths[i])

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

	def OnCopyOnlyText(self, evt):
		self.text.CopyOnlyText()

	def OnCopyAsImage(self, evt):
		dc = wx.msw.MetafileDC()
		self.DrawOnDC(dc)
		m = dc.Close()
		m.SetClipboard(dc.MaxX(), dc.MaxY())

	def OnPaste(self, evt):
		self.text.Paste()

	def OnPasteChords(self, evt):
		self.text.PasteChords()

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
				e1 = self.text.PositionAfter(e)
				self.text.SetSelection(e, e1)
				l = self.text.GetTextRange(e, e1)
				self.text.ReplaceSelection('')
				self.text.SetSelection(s, s)
				self.text.ReplaceSelection(l)
				s2 = self.text.PositionAfter(self.text.PositionAfter(s))
				self.text.SetSelection(s2, s2)
				self.text.EndUndoAction()

	def OnMoveChordLeft(self, evt):
		r = self.text.GetChordUnderCursor()
		if r is not None:
			s, e, c = r
			if s > 0:
				self.text.BeginUndoAction()
				s1 = self.text.PositionBefore(s)
				e1 = self.text.PositionBefore(e)
				l = self.text.GetTextRange(s1, s)
				self.text.SetSelection(e, e)
				self.text.ReplaceSelection(l)
				self.text.SetSelection(s1, s)
				self.text.ReplaceSelection('')
				s = self.text.PositionAfter(s1)
				self.text.SetSelection(s, s)
				self.text.EndUndoAction()

	def OnRemoveChords(self, evt):
		self.text.RemoveChordsInSelection()

	def OnIntegrateChords(self, evt):
		ln = self.text.GetCurrentLine()
		if ln < self.text.GetLineCount() - 1:
			chords = self.text.GetLine(ln).strip("\r\n")
			text = self.text.GetLine(ln + 1).strip("\r\n")
			chordpro = integrateChords(chords, text)
			self.text.SetSelectionStart(self.text.PositionFromLine(ln))
			self.text.SetSelectionEnd(self.text.GetLineEndPosition(ln + 1))
			self.text.ReplaceSelection(chordpro)

	def OnFontSelected(self, evt):
		font = self.fontChooser.GetValue()
		showChords = self.showChordsChooser.GetValue()
		self.pref.SetFont(font, showChords)
		self.SetFont(True)
		evt.Skip()

	def OnGuide(self, evt):
		if platform.system() == 'Windows':
			helpfile = os.path.join("help", "songpress-%s.chm" % (i18n.getLang(),))
			subprocess.Popen("hh " + glb.AddPath(helpfile))
		else:
			wx.LaunchDefaultBrowser(_("http://www.skeed.it/songpress-manual"))

	def OnIdle(self, evt):
		try:
			cp = self.text.CanPaste()
			self.mainToolBar.EnableTool(self.pasteTool, cp)
			self.menuBar.Enable(self.pasteMenuId, cp)
			self.mainToolBar.EnableTool(self.pasteChordsTool, cp)
			self.menuBar.Enable(self.pasteChordsMenuId, cp)
		except wx._core.PyDeadObjectError:
			# When frame is closed, this method may still be executed, generating an exception
			# because UI elements have been destroyed. Simply ignore it.
			pass
		evt.Skip()

	def OnNewsAndUpdates(self, evt):
		MyUpdateDialog.check_and_update(self.frame, self.pref, True)

	def OnDonate(self, evt):
		wx.LaunchDefaultBrowser(_("http://www.skeed.it/songpress#donate"))

	def OnFormatFont(self, evt):
		f = FontFaceDialog(self.frame, wx.ID_ANY, _("Songpress"), self.pref.format, self.pref.decorator,
											 self.pref.decoratorFormat)
		if f.ShowModal() == wx.ID_OK:
			self.pref.SetFont(f.GetValue())
			self.SetFont()

	def OnTranspose(self, evt):
		t = MyTransposeDialog(self.frame, self.pref.notations, self.text.GetTextOrSelection())
		if t.ShowModal() == wx.ID_OK:
			self.text.ReplaceTextOrSelection(t.GetTransposed())

	def OnSimplifyChords(self, evt):
		self.text.AutoChangeMode(True)
		t = self.text.GetTextOrSelection()
		notation = autodetectNotation(t, self.pref.notations)
		count, c, dc, e, de = findEasiestKey(t, self.pref.GetEasyChords(), notation)
		title = _("Simplify chords")
		if count > 0 and dc != de:
			msg = _("The key of your song, %s, is not the easiest to play (difficulty: %.1f/5.0).\n") % (c, 5 * dc)
			msg += _("Do you want to transpose the key %s, which is the easiest one (difficulty: %.1f/5.0)?") % (e, 5 * de)
			d = wx.MessageDialog(self.frame, msg, title, wx.YES_NO | wx.ICON_QUESTION)
			if d.ShowModal() == wx.ID_YES:
				t = transposeChordPro(translateChord(c, notation), translateChord(e, notation), t, notation)
				self.text.ReplaceTextOrSelection(t)
		else:
			if count > 0:
				msg = _("The key of your song, %s, is already the easiest to play (difficulty: %.1f/5.0).\n") % (c, 5 * dc)
			else:
				msg = _("Your song or current selection does not contain any chords.")
			d = wx.MessageDialog(self.frame, msg, title, wx.OK | wx.ICON_INFORMATION)
			d.ShowModal()
		self.text.AutoChangeMode(False)

	def OnChangeChordNotation(self, evt):
		t = MyNotationDialog(self.frame, self.pref.notations, self.text.GetTextOrSelection())
		if t.ShowModal() == wx.ID_OK:
			self.text.ReplaceTextOrSelection(t.ChangeChordNotation())

	def OnNormalizeChords(self, evt):
		t = MyNormalizeDialog(self.frame, self.pref.notations, self.text.GetTextOrSelection())
		if t.ShowModal() == wx.ID_OK:
			self.text.ReplaceTextOrSelection(t.NormalizeChords())

	def OnConvertTabToChordpro(self, evt):
		t = self.text.GetTextOrSelection()
		n = testTabFormat(t, self.pref.notations)
		if n is not None:
			self.text.ReplaceTextOrSelection(tab2ChordPro(t, n))

	def OnRemoveSpuriousBlankLines(self, evt):
		self.text.ReplaceTextOrSelection(removeSpuriousLines(self.text.GetTextOrSelection()))

	def OnOptions(self, evt):
		f = MyPreferencesDialog(self.frame, self.pref, easyChords)
		if f.ShowModal() == wx.ID_OK:
			self.text.SetFont(self.pref.editorFace, int(self.pref.editorSize))
			self.SetDefaultExtension(self.pref.defaultExtension)

	def StripSelection(self):
		"""
		Update selection, moving blank characters out of it
		"""
		t = self.text.GetText()
		s, e = self.text.GetSelection()
		mod = False
		while e > s and t[e - 1].strip() == '':
			e -= 1
			mod = True
		while s < e and t[s].strip() == '':
			s += 1
			mod = True
		if mod:
			self.text.SetSelection(s, e)

	def InsertWithCaret(self, st):
		self.StripSelection()
		s, e = self.text.GetSelection()
		c = st.find('|')
		if c != -1:
			sel_text = self.text.GetSelectedText()
			self.text.ReplaceSelection(st[:c] + sel_text + st[c + 1:])
			self.text.SetSelection(s + c, e + c)
		else:
			self.text.ReplaceSelection(st)
			self.text.SetSelection(s + len(st), s + len(st))

	def OnTitle(self, evt):
		self.InsertWithCaret("{title:|}")

	def OnSubtitle(self, evt):
		self.InsertWithCaret("{subtitle:|}")

	def OnChord(self, evt):
		self.InsertWithCaret("[|]")

	def OnVerse(self, evt):
		label = wx.GetTextFromUser(
			_("Insert a label for verse, or press Cancel if you want to omit label."),
			_("Verse label"),
			"",
			self.frame,
		)
		self.InsertWithCaret("{Verse:%s}|" % label)

	def OnChorus(self, evt):
		default = self.pref.decoratorFormat.GetChorusLabel()
		label = wx.GetTextFromUser(
			_("Insert a label for chorus, or press Cancel if you want to omit label."),
			_("Chorus label"),
			default,
			self.frame,
		)
		if label == default:
			self.InsertWithCaret("{soc}\n|\n{eoc}\n")
		else:
			self.InsertWithCaret("{soc:%s}\n|\n{eoc}\n" % label)

	def OnComment(self, evt):
		self.InsertWithCaret("{c:|}")

	def OnLabelVerses(self, evt):
		self.pref.labelVerses = not self.pref.labelVerses
		self.CheckLabelVerses()

	def OnChorusLabel(self, evt):
		c = self.pref.decoratorFormat.GetChorusLabel()
		msg = _("Please enter a label for chorus")
		d = wx.TextEntryDialog(self.frame, msg, _("Songpress"), c)
		if d.ShowModal() == wx.ID_OK:
			c = d.GetValue()
			self.pref.SetChorusLabel(c)
			self.previewCanvas.Refresh(self.text.GetText())

	def OnNoChords(self, evt):
		self.pref.format.showChords = 0
		self.SetFont(True)

	def OnOneVerseForEachChordPattern(self, evt):
		self.pref.format.showChords = 1
		self.SetFont(True)

	def OnWholeSong(self, evt):
		self.pref.format.showChords = 2
		self.SetFont(True)

	def OnTextChanged(self, evt):
		self.AutoAdjust(evt.lastPos, evt.currentPos)

	def AutoAdjust(self, lastPos, currentPos):
		self.text.AutoChangeMode(True)
		t = self.text.GetTextRange(lastPos, currentPos)
		if self.pref.autoAdjustSpuriousLines:
			if testSpuriousLines(t):
				msg = _("It looks like there are spurious blank lines in the song.\n")
				msg += _("Do you want to try to remove them automatically?")
				title = _("Remove spurious blank lines")
				d = wx.MessageDialog(self.frame, msg, title, wx.YES_NO | wx.ICON_QUESTION)
				if d.ShowModal() == wx.ID_YES:
					self.text.SetSelection(lastPos, currentPos)
					t = removeSpuriousLines(t)
					self.text.ReplaceSelection(t)
					currentPos = self.text.GetCurrentPos()
		if self.pref.autoAdjustTab2Chordpro:
			n = testTabFormat(t, self.pref.notations)
			if n is not None:
				msg = _("It looks like your song is in tab format (i.e., chords are above the text).\n")
				msg += _("Do you want to convert it to ChordPro automatically?")
				title = _("Convert to ChordPro")
				d = wx.MessageDialog(self.frame, msg, title, wx.YES_NO | wx.ICON_QUESTION)
				if d.ShowModal() == wx.ID_YES:
					self.text.SetSelection(lastPos, currentPos)
					t = tab2ChordPro(t, n)
					self.text.ReplaceSelection(t)
		if self.pref.autoAdjustEasyKey:
			notation = autodetectNotation(t, self.pref.notations)
			count, c, dc, e, de = findEasiestKey(t, self.pref.GetEasyChords(), notation)
			if count > 10 and dc != de:
				msg = _("The key of your song, %s, is not the easiest to play (difficulty: %.1f/5.0).\n") % (c, 5 * dc)
				msg += _("Do you want to transpose the key %s, which is the easiest one (difficulty: %.1f/5.0)?") % (e, 5 * de)
				title = _("Simplify chords")
				d = wx.MessageDialog(self.frame, msg, title, wx.YES_NO | wx.ICON_QUESTION)
				if d.ShowModal() == wx.ID_YES:
					self.text.SetSelection(lastPos, currentPos)
					t = transposeChordPro(translateChord(c, notation), translateChord(e, notation), t, notation)
					self.text.ReplaceSelection(t)
		self.text.AutoChangeMode(False)

	def SetFont(self, updateFontChooser=True):
		try:
			if updateFontChooser:
				self.fontChooser.SetValue(self.pref.format.face)
				self.showChordsChooser.SetValue(self.pref.format.showChords)
				ids = [self.noChordsMenuId, self.oneVerseForEachChordPatternMenuId, self.wholeSongMenuId]
				self.menuBar.Check(ids[self.pref.format.showChords], True)

			self.previewCanvas.Refresh(self.text.GetText())
		except wx._core.PyDeadObjectError:
			# When frame is closed, this method may still be executed, generating an exception
			# because UI elements have been destroyed. Simply ignore it.
			pass

	def CheckLabelVerses(self):
		self.formatToolBar.ToggleTool(self.labelVersesToolId, self.pref.labelVerses)
		self.formatToolBar.Refresh()
		self.menuBar.Check(self.labelVersesMenuId, self.pref.labelVerses)
		if self.pref.labelVerses:
			self.previewCanvas.SetDecorator(self.pref.decorator)
		else:
			self.previewCanvas.SetDecorator(SongDecorator())
		self.previewCanvas.Refresh(self.text.GetText())


