###############################################################
# Name:			 Editor.py
# Purpose:	 Subclass of StyledTextControl providing songpress
#            editor: loading, saving and syntax hilighting
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-16
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

		
import wx
from wx import xrc
from wx.stc import *
from SDIMainFrame import *
from SongTokenizer import *
import sys

class Editor(StyledTextCtrl):

	def __init__(self, spframe):
		StyledTextCtrl.__init__(self, spframe.frame)
		self.spframe = spframe
		self.spframe.frame.Bind(EVT_STC_CHANGE, self.OnTextChange, self)
		font = wx.Font(
			12,
			wx.FONTFAMILY_DEFAULT,
			wx.FONTSTYLE_NORMAL,
			wx.FONTWEIGHT_NORMAL,
			faceName = "Lucida Console"
		)
		self.StyleSetFont(STC_STYLE_DEFAULT, font)
		self.spframe.frame.Bind(EVT_STC_STYLENEEDED, self.OnStyleNeeded, self)
		self.SetLexer(STC_LEX_CONTAINER)
		self.STC_STYLE_NORMAL = 11
		self.STC_STYLE_CHORD = 12
		self.STC_STYLE_COMMAND = 13
		self.STC_STYLE_ATTR = 14
		self.STC_STYLE_CHORUS = 15
		self.StyleSetForeground(self.STC_STYLE_NORMAL, wx.Color(0, 0, 0))
		self.StyleSetForeground(self.STC_STYLE_CHORUS, wx.Color(0, 0, 0))
		self.StyleSetForeground(self.STC_STYLE_CHORD, wx.Color(255, 0, 0))
		self.StyleSetForeground(self.STC_STYLE_COMMAND, wx.Color(0, 0, 255))
		self.StyleSetForeground(self.STC_STYLE_ATTR, wx.Color(0, 128, 0))
		#I don't know why, but the following line is necessary in order to make
		#the font bold
		self.StyleSetFont(self.STC_STYLE_CHORUS, font)		
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
			self.chorusToken: self.STC_STYLE_CHORUS
		}
		#self.chorus[i] == True iff, at the end of line i, we are still in chorus (i.e. bold) mode
		self.chorus = []
	
	def New(self):
		self.ClearAll();
		
	def Open(self):
		self.LoadFile(self.spframe.document)
		
	def Save(self):
		self.SaveFile(self.spframe.document)
		
	def OnTextChange(self, evt):
		print("OnTextChange")
		self.spframe.SetModified()
		self.spframe.TextUpdated()
	
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


