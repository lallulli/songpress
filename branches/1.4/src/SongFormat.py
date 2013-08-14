###############################################################
# Name:			 SongFormat.py
# Purpose:	 Song format options
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-24
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import wx

class AttributeMonitor(object):
	def __init__(self, handlers):
		object.__init__(self)
		self.am_started = False
		self.am_handlers = handlers

	def __setattr__(self, name, value):
		object.__setattr__(self, name, value)
		if name != 'am_started' and self.am_started:
			for h in self.am_handlers:
				if name in h.names:
					#print name
					h.OnSetAttr(self, name, value)

	def Am_Start(self):
		self.am_started = True

class FontChangeHandler(object):
	names = set(("face", "size", "bold", "italic", "underline"))
	@staticmethod
	def OnSetAttr(format, name, value):
		format.UpdateWxFont()

class FontFormat(AttributeMonitor):
	def __init__(self, ff=None):
		AttributeMonitor.__init__(self, (FontChangeHandler, ))
		# Definable by user
		if ff == None:
			self.face = "Arial"
		else:
			self.face = ff.face
		self.size = 12
		self.bold = False
		self.italic = False
		self.underline = False
		# Auto set
		self.wxFont = None
		self.UpdateWxFont()
		# Start monitor
		self.Am_Start()

	def UpdateWxFont(self):
		#print("Font Updated, face = " + self.face)
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
	def __init__(self, ff=None):
		FontFormat.__init__(self, ff)
		self.leftMargin = 0
		self.topMargin = 12
		self.bottomMargin = 0
		self.chordSpacing = 0.8
		self.textSpacing = 1
		self.vskip = 1
		self.chord = FontFormat(ff)
		self.chord.size = self.size * 0.9
		self.chord.italic = True
		self.comment = FontFormat(ff)
		self.comment.italic = True

class SongFormat(ParagraphFormat):
	def __init__(self, ff=None):
		ParagraphFormat.__init__(self, ff)
		self.verse = []
		self.chorus = ParagraphFormat(ff)
		self.chorus.bold = True
		self.chorus.underline = False
		self.title = ParagraphFormat(ff)
		self.title.bold = True
		self.title.underline = True
		self.blockSpacing = 1
		# showChords:
		# 0. None
		# 1. First verse and chorus
		# 2. Entire song
		self.showChords = 1#2

	def StubSetVerseCount(self, n):
		i = len(self.verse)
		while i < n:
			self.verse.append(ParagraphFormat(self))
			i = i + 1
