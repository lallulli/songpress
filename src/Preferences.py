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
		* chorusLabel (None or string)
		* labelVerses
		* editorFace
		* editorSize
		* fontFace
		* defaultNotation
		* notations
		* defaultNotation
		* autoAdjustSpuriousLines
		* autoAdjustTab2Chordpro
		* locale
	"""
	def __init__(self):
		object.__init__(self)
		self.config = wx.Config.Get()
		self.format = SongFormat()
		self.decoratorFormat = StandardVerseNumbers.Format(self.format, _("Chorus"))
		self.decorator = StandardVerseNumbers.Decorator(self.decoratorFormat)
		self.notations = [enNotation, itNotation, deNotation, frNotation, ptNotation]
		self.Load()
		self.easiestKeyFav = {'C': 1, 'D': 1, 'Dm': 1, 'D7': 1, 'Eb': -1, 'E': 1, 'Em': 1, 'E7': 0.8, 'F': 0.4, 'G': 1, 'G7': 1, 'A': 1, 'Am': 1, 'A7': 1, 'B7': 0.4}

	def SetFont(self, font):
		self.fontFace = font
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

	def Load(self):
		self.config.SetPath('/Format')
		l = self.config.Read('ChorusLabel')
		if l:
			self.chorusLabel = l
			self.decoratorFormat.SetChorusLabel(l)
		else:
			self.chorusLabel = None
		self.config.SetPath('/Format/Font')
		face = self.config.Read('Face')
		if face:
			self.fontFace = face
		else:
			self.fontFace = "Arial"
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
			self.editorSize = 12
		else:
			self.editorSize = int(self.editorSize)
		n = self.config.Read('DefaultNotation')
		if n:
			self.defaultNotation = n
			self.notations = [x for x in self.notations if x.id == n] + [x for x in self.notations if x.id != n]
		else:
			lang = i18n.getLang()
			if lang in defaultLangNotation:
				n = defaultLangNotation[lang].id
				self.notations = [x for x in self.notations if x.id == n] + [x for x in self.notations if x.id != n]
				self.defaultNotation = None
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
		easiestKey = self.config.Read('easiestKey')
		if easiestKey:
			self.autoAdjustEasiestKey = bool(int(easiestKey))
		else:
			self.autoAdjustEasiestKey = False
		self.config.SetPath('/App')
		lang = self.config.Read('locale')
		if not lang:
			self.locale = None
		else:
			self.locale = lang

	def Bool2String(self, param):
		return "1" if param else "0"

	def Save(self):
		self.config.SetPath('/Format')
		if self.chorusLabel is not None:
			self.config.Write('ChorusLabel', self.chorusLabel)
		self.config.SetPath('/Format/Font')
		face = self.config.Write('Face', self.fontFace)
		self.config.SetPath('/Format/Style')
		self.config.Write('LabelVerses', self.Bool2String(self.labelVerses))
		self.config.SetPath('/Editor')
		self.config.Write('Face', self.editorFace)
		self.config.Write('Size', str(self.editorSize))
		if self.defaultNotation is not None:
			self.config.Write('DefaultNotation', self.defaultNotation)
		self.config.SetPath('/AutoAdjust')
		self.config.Write('spuriousLines', self.Bool2String(self.autoAdjustSpuriousLines))
		self.config.Write('tab2chordpro', self.Bool2String(self.autoAdjustTab2Chordpro))
		self.config.Write('easiestKey', self.Bool2String(self.autoAdjustEasiestKey))
		if self.locale is not None:
			self.config.SetPath('/App')
			lang = self.config.Write('locale', self.locale)

	def SetChorusLabel(self, c):
		self.chorusLabel = c
		self.decoratorFormat.SetChorusLabel(c)

	def SetDefaultNotation(self, notation):
		self.defaultNotation = notation
		self.notations = [x for x in self.notations if x.id == notation] + [x for x in self.notations if x.id != notation]
