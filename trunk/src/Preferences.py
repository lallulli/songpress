###############################################################
# Name:			 Preferences.py
# Purpose:	 Hold program preferences
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2010-01-31
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

from SongFormat import *
from decorators import StandardVerseNumbers
from SongDecorator import SongDecorator
from Transpose import *
import i18n

i18n.register('Preferences')


class Preferences(object):
	"""
		Available preferences

		* format
		* decoratorFormat
		* decorator
		* labelVerses
		* editorFace
		* editorSize
		* notations
		* autoAdjustSpuriousLines
		* autoAdjustTab2Chordpro
	"""
	def __init__(self):
		object.__init__(self)
		self.config = wx.FileConfig("songpress")
		self.format = SongFormat()
		self.decoratorFormat = StandardVerseNumbers.Format(self.format, _("Chorus"))
		self.decorator = StandardVerseNumbers.Decorator(self.decoratorFormat)
		self.notations = [enNotation, itNotation, deNotation, frNotation, ptNotation]
		self.Load()

	def SetFont(self, font):
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
		self.config.SetPath('/Format/Font')
		self.config.Write('FontFace', font)

	def Load(self):
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
		else:
			self.labelVerses = True
		self.config.SetPath('/Editor')
		self.editorFace = self.config.Read('Face')
		self.editorSize = self.config.Read('Size')
		if not self.editorFace:
			self.editorFace = "Lucida Console"
			self.editorSize = '12'
		else:
			self.editorSize = int(self.editorSize)
		n = self.config.Read('DefaultNotation')
		if n:
			self.notations = [x for x in self.notations if x.id == n] + [x for x in self.notations if x.id != n]
		else:
			lang = i18n.getLang()
			if lang in defaultLangNotation:
				n = defaultLangNotation[lang].id
				self.notations = [x for x in self.notations if x.id == n] + [x for x in self.notations if x.id != n]
		self.config.SetPath('/AutoAdjust')
		spuriousLines = self.config.Read('spuriousLines')
		if spuriousLines:
			self.autoAdjustSpuriousLines = bool(int(spuriousLines))
		else:
			self.autoAdjustSpuriousLines = True
		tab2chordpro = self.config.Read('tab2chordpro')
		if tab2chordpro:
			self.autoAdjustTab2Chordpro = bool(int(tab2chordpro))
		else:
			self.autoAdjustTab2Chordpro = True

