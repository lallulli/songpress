###############################################################
# Name:			 Editor.py
# Purpose:	 Subclass of StyledTextControl providing songpress
#            editor: loading, saving and syntax hilighting
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-16
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################


import wx
from wx import xrc
from wx.stc import *
from SDIMainFrame import *
from SongTokenizer import *
import sys
import wx.lib, wx.lib.newevent
import Transpose
import codecs

EventTextChanged, EVT_TEXT_CHANGED = wx.lib.newevent.NewEvent()

def get_text_from_clipboard():
	"""
	Return text in clipboard, or None
	"""
	if wx.TheClipboard.IsOpened():
		return None
	wx.TheClipboard.Open()
	do = wx.TextDataObject()
	if not wx.TheClipboard.GetData(do):
		return None
	wx.TheClipboard.Close()
	return do.GetText()

class Editor(StyledTextCtrl):

	def __init__(self, spframe, interactive=True, frame=None):
		self.frame = spframe.frame if frame is None else frame
		StyledTextCtrl.__init__(self, self.frame)
		self.spframe = spframe
		self.interactive = interactive
		if self.interactive:
			self.lastPos = 0
			self.frame.Bind(EVT_STC_CHANGE, self.OnTextChange, self)
			self.frame.Bind(EVT_STC_UPDATEUI, self.OnUpdateUI, self)
			self.Bind(EVT_STC_DOUBLECLICK, self.OnDoubleClick, self)
			self.Bind(wx.EVT_CHAR, self.OnChar, self)
			self.autoChangeMode = False
		self.frame.Bind(EVT_STC_STYLENEEDED, self.OnStyleNeeded, self)
		self.STC_STYLE_NORMAL = 11
		self.STC_STYLE_CHORD = 12
		self.STC_STYLE_COMMAND = 13
		self.STC_STYLE_ATTR = 14
		self.STC_STYLE_CHORUS = 15
		self.STC_STYLE_COMMENT = 16
		self.SetFont("Lucida Console", 12)
		self.SetLexer(STC_LEX_CONTAINER)
		self.StyleSetForeground(self.STC_STYLE_NORMAL, wx.Colour(0, 0, 0))
		self.StyleSetForeground(self.STC_STYLE_CHORUS, wx.Colour(0, 0, 0))
		self.StyleSetForeground(self.STC_STYLE_CHORD, wx.Colour(255, 0, 0))
		self.StyleSetForeground(self.STC_STYLE_COMMAND, wx.Colour(0, 0, 255))
		self.StyleSetForeground(self.STC_STYLE_ATTR, wx.Colour(0, 128, 0))
		self.StyleSetForeground(self.STC_STYLE_COMMENT, wx.Colour(128, 128, 128))
		self.StyleSetBold(self.STC_STYLE_CHORUS, True)
		#Dummy "token": we artificially replace every normalToken into a chorusToken when we are
		#inside chorus.  Then, we can associate the chorus style in self.tokenStyle dictionary.
		self.chorusToken = 'chorusToken'
		self.tokenStyle = {
			SongTokenizer.openCurlyToken: self.STC_STYLE_COMMAND,
			SongTokenizer.closeCurlyToken: self.STC_STYLE_COMMAND,
			SongTokenizer.normalToken: self.STC_STYLE_NORMAL,
			SongTokenizer.commandToken: self.STC_STYLE_COMMAND,
			SongTokenizer.attrToken: self.STC_STYLE_ATTR,
			SongTokenizer.chordToken: self.STC_STYLE_CHORD,
			SongTokenizer.closeChordToken: self.STC_STYLE_CHORD,
			SongTokenizer.colonToken: self.STC_STYLE_COMMAND,
			SongTokenizer.commentToken: self.STC_STYLE_COMMENT,
			self.chorusToken: self.STC_STYLE_CHORUS
		}
		#self.chorus[i] == True iff, at the end of line i, we are still in chorus (i.e. bold) mode
		self.chorus = []

	def SetFont(self, face, size):
		font = wx.Font(
			size,
			wx.FONTFAMILY_DEFAULT,
			wx.FONTSTYLE_NORMAL,
			wx.FONTWEIGHT_NORMAL,
			faceName = face
		)
		self.StyleSetFont(STC_STYLE_DEFAULT, font)
		#I don't know why, but the following line is necessary in order to make
		#the font bold
		self.StyleSetFont(self.STC_STYLE_CHORUS, font)

	def New(self):
		self.ClearAll()

	def Open(self):
		self.ClearAll()
		self.LoadFile(self.spframe.document)

	def Save(self):
		#self.SaveFile(self.spframe.document)
		t = self.GetText()
		f = codecs.open(self.spframe.document, 'w', 'utf-8')
		f.write(t)
		f.close()
		

	def GetTextOrSelection(self):
		start, end = self.GetSelection()
		if start == end:
			return self.GetText()
		return self.GetSelectedText()

	def ReplaceTextOrSelection(self, text):
		start, end = self.GetSelection()
		if start == end:
			self.SetText(text)
		else:
			self.ReplaceSelection(text)

	def GetChordUnderCursor(self):
		"""Return info about chord under cursor, or None

		Return a 3-tuple: (begin, end, chord)
			begin: position before open bracket
			end: position after close bracket
			chord: chord, without brackets
		"""
		pos, dummy = self.GetSelection()
		char = ""
		if self.GetSelectedText().find('[') != -1:
			start = pos
			while char != '[':
				next = self.PositionAfter(start)
				char = self.GetTextRange(start, next)
				start = next
			start = self.PositionBefore(start)
		else:
			start = self.PositionBefore(pos)
			while start >= 0 and char != '[' and char != '\n' and char != ']':
				char = self.GetTextRange(start, self.PositionAfter(start))
				if start == 0:
					start = -1
				else:
					start = self.PositionBefore(start)
			if start >= 0:
				start = self.PositionAfter(start)
			else:
				start = 0
		if char == '[':
			end = self.PositionBefore(pos)
			l = self.GetLength()
			while end < l and char != ']' and char != '\n':
				char = self.GetTextRange(end, self.PositionAfter(end))
				end = self.PositionAfter(end)
			if char == ']':
				return (start, end, self.GetTextRange(self.PositionAfter(start), self.PositionBefore(end)))
		return None

	def SelectNextChord(self):
		dummy, pos = self.GetSelection()
		n = self.GetLength()
		c = ''
		while pos < n:
			while pos < n and c != '[':
				c = self.GetTextRange(pos, self.PositionAfter(pos))
				pos = self.PositionAfter(pos)
			if c == '[':
				start = pos
				while pos < n and c != ']' and c != '\n':
					c = self.GetTextRange(pos, self.PositionAfter(pos))
					pos = self.PositionAfter(pos)
				if c == ']':
					self.SetSelection(self.PositionBefore(start), pos)
					return True
		return False

	def SelectPreviousChord(self):
		pos, dummy = self.GetSelection()
		c = ''
		done = False
		while not done:
			while not done and c != ']':
				c = self.GetTextRange(pos, self.PositionAfter(pos))
				if pos <= 0:
					done = True
				else:
					pos = self.PositionBefore(pos)
			if c == ']':
				end = pos
				while not done and c != '[' and c != '\n':
					c = self.GetTextRange(pos, self.PositionAfter(pos))
					if pos <= 0:
						pos = -1
						done = True
					else:
						pos = self.PositionBefore(pos)
				if pos == -1:
					pos = 0
				else:
					pos = self.PositionAfter(pos)
				if c == '[':
					self.SetSelection(pos, self.PositionAfter(self.PositionAfter(end)))
					return True
		return False

	def RemoveChordsInSelection(self):
		self.ReplaceSelection(Transpose.removeChords(self.GetSelectedText()))
		
	def CopyOnlyText(self):
		text = Transpose.removeChordPro(self.GetSelectedText())
		c = wx.TheClipboard
		if c.Open():
			c.SetData(wx.TextDataObject(text))
			c.Close()
		

	def OnTextChange(self, evt):
		if self.interactive:
			self.spframe.SetModified()
			self.spframe.TextUpdated()
			if not self.autoChangeMode:
				currentPos = self.GetCurrentPos()
				if currentPos - self.lastPos > 2:
					evt = EventTextChanged(lastPos=self.lastPos, currentPos=currentPos)
					wx.PostEvent(self.frame, evt)

	def OnUpdateUI(self, evt):
		self.lastPos = self.GetCurrentPos()
		evt.Skip(False)

	def OnDoubleClick(self, evt):
		t = self.GetChordUnderCursor()
		if t is not None:
			self.SetSelection(t[0], t[1])
		evt.Skip()

	def OnChar(self, evt):
		t = self.GetSelectedText()
		if t != '' and t[0] == '[' and t[-1] == ']':
			c = evt.GetKeyCode()
			if (c >= 65 and c <= 90) or (c >= 97 and c <= 122):
				s, e = self.GetSelection()
				self.SetSelection(self.PositionAfter(s), self.PositionBefore(e))
		evt.Skip()

	def AutoChangeMode(self, acm):
		self.autoChangeMode = acm
		
	def PasteChords(self):
		src = get_text_from_clipboard()
		if src is None:
			return
		self.BeginUndoAction()
		start, end = self.GetSelection()
		if start == end:
			l = self.LineFromPosition(start)
			end = self.PositionFromLine(l + len(src.splitlines()))
			if end == -1:
				end = self.GetLength()
			else:
				end = self.PositionBefore(end)
		prev = self.PositionBefore(end)
		while end > start and self.GetCharAt(prev) in [10, 13]:
			end = prev
			prev = self.PositionBefore(end)
		self.SetSelection(start, end)
		self.ReplaceSelection(Transpose.pasteChords(src, self.GetSelectedText()))
		self.EndUndoAction()
		

	def OnStyleNeeded(self, evt):
		end = evt.GetPosition()
		pos = self.GetEndStyled()
		ln = self.LineFromPosition(pos)
		start = self.PositionFromLine(ln)
		if ln > 0 and len(self.chorus) > ln-1:
			bold = self.chorus[ln-1]
		else:
			bold = False
		#changedBold is True iff self.chorus has changed for the current line, and thus we need
		#to process (at least) another line
		changedBold = False
		lc = self.GetLineCount()
		while (changedBold and ln < lc) or start < end:
			self.StartStyling(start, 0x1f)
			l = self.GetLine(ln)
			tkz = SongTokenizer(l)
			for tok in tkz:
				n = len(tok.content.encode('utf-8'))
				t = tok.token
				if bold and t == SongTokenizer.normalToken:
					t = self.chorusToken
				self.SetStyling(n, self.tokenStyle[t])
				if t == SongTokenizer.commandToken:
					if tok.content.upper() == 'SOC':
						bold = True
					elif tok.content.upper() == 'EOC':
						bold = False
			if len(self.chorus) > ln:
				changedBold = self.chorus[ln] != bold
				self.chorus[ln] = bold
			else:
				self.chorus.append(bold)
				changedBold = False
			ln = ln + 1
			start = self.PositionFromLine(ln)


