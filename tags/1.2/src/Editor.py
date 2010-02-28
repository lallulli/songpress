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

EventTextChanged, EVT_TEXT_CHANGED = wx.lib.newevent.NewEvent()

class Editor(StyledTextCtrl):

	def __init__(self, spframe, interactive=True):
		StyledTextCtrl.__init__(self, spframe.frame if interactive else spframe)
		self.spframe = spframe
		self.interactive = interactive
		if self.interactive:
			self.lastPos = 0
			self.spframe.frame.Bind(EVT_STC_CHANGE, self.OnTextChange, self)
			self.spframe.frame.Bind(EVT_STC_UPDATEUI, self.OnUpdateUI, self)
			self.autoChangeMode = False
		self.spframe.frame.Bind(EVT_STC_STYLENEEDED, self.OnStyleNeeded, self)
		self.STC_STYLE_NORMAL = 11
		self.STC_STYLE_CHORD = 12
		self.STC_STYLE_COMMAND = 13
		self.STC_STYLE_ATTR = 14
		self.STC_STYLE_CHORUS = 15
		self.STC_STYLE_COMMENT = 16
		self.SetFont("Lucida Console", 12)
		self.SetLexer(STC_LEX_CONTAINER)
		self.StyleSetForeground(self.STC_STYLE_NORMAL, wx.Color(0, 0, 0))
		self.StyleSetForeground(self.STC_STYLE_CHORUS, wx.Color(0, 0, 0))
		self.StyleSetForeground(self.STC_STYLE_CHORD, wx.Color(255, 0, 0))
		self.StyleSetForeground(self.STC_STYLE_COMMAND, wx.Color(0, 0, 255))
		self.StyleSetForeground(self.STC_STYLE_ATTR, wx.Color(0, 128, 0))
		self.StyleSetForeground(self.STC_STYLE_COMMENT, wx.Color(128, 128, 128))
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
		self.ClearAll();

	def Open(self):
		self.LoadFile(self.spframe.document)

	def Save(self):
		self.SaveFile(self.spframe.document)

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
		start = pos - 1
		while start >= 0 and char != '[' and char != '\n' and char != ']':
			char = self.GetTextRange(start, start + 1)
			start -= 1
		if char == '[':
			end = pos - 1
			l = self.GetLength()
			while end < l and char != ']' and char != '\n':
				char = self.GetTextRange(end, end + 1)
				end += 1
			if char == ']':
				return (start + 1, end, self.GetTextRange(start + 2, end - 1))
		return None

	def SelectNextChord(self):
		dummy, pos = self.GetSelection()
		n = self.GetLength()
		c = ''
		while pos < n:
			while pos < n and c != '[':
				c = self.GetTextRange(pos, pos + 1)
				pos += 1
			if c == '[':
				start = pos
				while pos < n and c != ']' and c != '\n':
					c = self.GetTextRange(pos, pos + 1)
					pos += 1
				if c == ']':
					self.SetSelection(start, pos - 1)
					return True
		return False

	def SelectPreviousChord(self):
		pos, dummy = self.GetSelection()
		pos -= 1
		c = ''
		while pos >= 0:
			while pos >= 0 and c != ']':
				c = self.GetTextRange(pos, pos + 1)
				pos -= 1
			if c == ']':
				end = pos
				while pos >= 0 and c != '[' and c != '\n':
					c = self.GetTextRange(pos, pos + 1)
					pos -= 1
				if c == '[':
					self.SetSelection(pos + 2, end + 1)
					return True
		return False

	def OnTextChange(self, evt):
		if self.interactive:
			self.spframe.SetModified()
			self.spframe.TextUpdated()
			if not self.autoChangeMode:
				currentPos = self.GetCurrentPos()
				if currentPos - self.lastPos > 2:
					evt = EventTextChanged(lastPos=self.lastPos, currentPos=currentPos)
					wx.PostEvent(self.spframe.frame, evt)


	def OnUpdateUI(self, evt):
		self.lastPos = self.GetCurrentPos()
		evt.Skip(False)

	def AutoChangeMode(self, acm):
		self.autoChangeMode = acm

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


