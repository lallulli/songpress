###############################################################
# Name:			 SongFormat.py
# Purpose:	 Song format options
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-24
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
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
		self.size = 12 if ff is None else ff.size
		self.bold = False if ff is None else ff.bold
		self.italic = False if ff is None else ff.italic
		self.underline = False  if ff is None else ff.underline
		self.color = '#000000' if ff is None else ff.color
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
		self.wxFont = wx.Font(int(self.size), wx.FONTFAMILY_DEFAULT, style, weight, self.underline, self.face)


class ParagraphFormat(FontFormat):
	def __init__(self, ff=None):
		FontFormat.__init__(self, ff)
		self.leftMargin = 0 if ff is None else ff.leftMargin
		self.topMargin = 12 if ff is None else ff.topMargin
		self.bottomMargin = 0 if ff is None else ff.bottomMargin
		self.chordSpacing = 0.8 if ff is None else ff.chordSpacing
		self.textSpacing = 1 if ff is None else ff.textSpacing
		self.chord = FontFormat(ff.chord) if ff is not None else FontFormat()
		self.comment = FontFormat(ff.comment) if ff is not None else FontFormat()
		if ff is None:
			self.chord.size = self.size * 0.9
			self.chord.italic = True
			self.chord.bold = False
			self.comment.italic = True


class SongFormat(ParagraphFormat):
	def __init__(self, ff=None):
		ParagraphFormat.__init__(self, ff)
		self.verse = []
		self.chorus = ParagraphFormat(ff.chorus) if ff is not None else ParagraphFormat()
		self.title = ParagraphFormat(ff.title) if ff is not None else ParagraphFormat()
		self.subtitle = ParagraphFormat(ff.subtitle) if ff is not None else ParagraphFormat()
		self.blockSpacing = 1 if ff is None else ff.blockSpacing
		# showChords:
		# 0. None
		# 1. First verse and chorus
		# 2. Entire song
		self.showChords = 1 if ff is None else ff.showChords
		if ff is None:
			self.chorus.bold = True
			self.chorus.underline = False
			self.title.bold = True
			self.title.underline = True
			self.subtitle.size = self.title.size * 0.95
			self.subtitle.italic = True

	def AddVerse(self):
		self.verse.append(ParagraphFormat(self))

	def InitVerses(self):
		self.verse = []