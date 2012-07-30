###############################################################
# Name:			 SongFormat.py
# Purpose:	 Song format options
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-24
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import wx
from Pref import Prototype
		
class FontFormat(Prototype):
	def __init__(self, ff=None):
		Prototype.__init__(self, ff)
		if ff is None:
			self.size = 12
			self.bold = False
			self.italic = False
			self.underline = False
			self.wxFont = None
			self.face = "Arial"
		self.AddHandler(self.onFontChanged)
		self.onFontChanged(self, '', '')

	def onFontChanged(self, obj, name, value):
		if name in ['face', 'size', 'bold', 'italic', 'underline']:
			if obj.italic:
				style = wx.FONTSTYLE_ITALIC
			else:
				style = wx.FONTSTYLE_NORMAL
			if obj.bold:
				weight = wx.FONTWEIGHT_BOLD
			else:
				weight = wx.FONTWEIGHT_NORMAL
			obj.wxFont = wx.Font(obj.size, wx.FONTFAMILY_DEFAULT, style, weight, obj.underline, obj.face)


class ParagraphFormat(FontFormat):
	def __init__(self, ff=None):
		FontFormat.__init__(self, ff)
		self.leftMargin = 0
		self.topMargin = 12
		self.bottomMargin = 0
		self.chordSpacing = 0.8
		self.textSpacing = 1
		self.vskip = 1
		self.chord = FontFormat(self)
		self.chord.size = self.size * 0.9
		self.chord.italic = True
		self.comment = FontFormat(self)
		self.comment.italic = True

class SongFormat(ParagraphFormat):
	def __init__(self, ff=None):
		ParagraphFormat.__init__(self, ff)
		self.verse = []
		self.chorus = ParagraphFormat(self)
		self.chorus.bold = True
		self.chorus.underline = False
		self.title = ParagraphFormat(self)
		self.title.bold = True
		self.title.underline = True
		self.blockSpacing = 1

	def StubSetVerseCount(self, n):
		i = len(self.verse)
		while i < n:
			self.verse.append(ParagraphFormat(self))
			i = i + 1
