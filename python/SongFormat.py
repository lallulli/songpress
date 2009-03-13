###############################################################
# Name:			 SongFormat.py
# Purpose:	 Song format options
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-24
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

import wx

class FontFormat(object):
	def __init__(self):
		object.__init__(self)
		# Definable by user
		self.face = "Arial"
		self.size = 12
		self.bold = False
		self.italic = False
		self.underline = False
		# Auto set
		self.wxFont = None
		self._UpdateWxFont()
		
	#TODO: Call following method automatically upon property change		
	def _UpdateWxFont(self):
		if self.italic:
			style = wx.FONTSTYLE_ITALIC
		else:
			style = wx.FONTSTYLE_NORMAL
		if self.bold:
			weight = wx.FONTWEIGHT_BOLD
		else:
			weight = wx.FONTWEIGHT_NORMAL
		self.wxFont = wx.Font(self.size, wx.FONTFAMILY_DEFAULT, style, weight, self.underline, self.face)
	
class ParagraphFormat(FontFormat):
	def __init__(self):
		object.__init__(self)
		FontFormat.__init__(self)
		self.leftMargin = 0
		self.topMargin = 12
		self.bottomMargin = 0
		self.chordSpacing = 0.8
		self.textSpacing = 1
		self.vskip = 1
		self.chord = FontFormat()
		self.chord.size = self.size * 0.9
		self.chord.italic = True
		self.comment = FontFormat()
		self.comment.italic = True

class SongFormat(ParagraphFormat):
	def __init__(self):
		object.__init__(self)
		ParagraphFormat.__init__(self)
		self.verse = []
		self.chorus = ParagraphFormat()
		self.chorus.bold = True
		self.title = ParagraphFormat()
		self.title.bold = True
		self.title.underline = True
		self.blockSpacing = 1
	def StubSetVerseCount(self, n):
		i = len(self.verse)
		while i < n:
			self.verse.append(ParagraphFormat())
			i = i + 1
