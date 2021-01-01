###############################################################
# Name:			 Preferences.py
# Purpose:	 Hold program preferences
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2010-01-31
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

from SongFormat import *
from decorators import StandardVerseNumbers
from SongDecorator import SongDecorator
from Transpose import *
import i18n
import datetime

i18n.register('Preferences')

def get_update_frequencies():
	return {
		0: _("Never"),
		7: _("Week"),
		14: _("Two weeks"),
		30: _("Month"),
		60: _("Two months"),
	}
	
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
		* autoAdjustEasyKey
		* locale
		* updateFrequency (days, or 0 for never)
		* ignoredUpdates
		* updateUrl
		* updateLastCheck
		* Set/GetEasyChordsGroup
		* GetEasyChords
	"""
	def __init__(self):
		object.__init__(self)
		self.config = wx.Config.Get()
		self.format = SongFormat()
		self.decoratorFormat = StandardVerseNumbers.Format(self.format, _("Chorus"))
		self.decorator = StandardVerseNumbers.Decorator(self.decoratorFormat)
		self.notations = [enNotation, itNotation, deNotation, tradDeNotation, frNotation, ptNotation]
		self.easyChordsGroup = {}
		self.Load()

	def SetFont(self, font, showChords=None):
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
		self.format.subtitle.face = font
		self.decoratorFormat.face = font
		self.decoratorFormat.chorus.face = font
		if showChords is not None:
			self.format.showChords = showChords

	def Load(self):
		self.notices = {}
		self.config.SetPath('/Format')
		l = self.config.Read('ChorusLabel')
		if l:
			self.chorusLabel = l
			self.decoratorFormat.SetChorusLabel(l)
		else:
			self.chorusLabel = None
		showChords = int(self.config.Read('ShowChords', "2"))
		self.config.SetPath('/Format/Font')
		face = self.config.Read('Face')
		if face:
			self.fontFace = face
		else:
			self.fontFace = "Arial"
		self.SetFont(self.fontFace, showChords)
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
			self.editorFace = wx.SystemSettings().GetFont(wx.SYS_ANSI_FIXED_FONT).GetFaceName() # "Lucida Console"
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
		easyKey = self.config.Read('easyKey')
		if easyKey:
			self.autoAdjustEasyKey = bool(int(easyKey))
		else:
			self.autoAdjustEasyKey = False
			self.notices['firstTimeEasyKey'] = True
		self.config.SetPath('/AutoAdjust/EasyChordsGroups')
		for k in easyChordsOrder:
			l = self.config.Read(k)
			if l:
				l = int(l)
			else:
				l = easyChords[k][2]
			self.SetEasyChordsGroup(k, l)
		self.config.SetPath('/App')
		ext = self.config.Read('defaultExtension')
		if not ext:
			self.defaultExtension = 'crd'
		else:
			self.defaultExtension = ext
		lang = self.config.Read('locale')
		if not lang:
			self.locale = None
		else:
			self.locale = lang
		self.config.SetPath('/AutoUpdate')
		f = self.config.Read('frequency')
		if not f:
			self.updateFrequency = 7
		else:
			self.updateFrequency = int(f)
		i = self.config.Read('ignored')
		if not i:
			self.ignoredUpdates = set()
		else:
			self.ignoredUpdates = set(i.split(','))
		u = self.config.Read('url')
		if not u:
			self.updateUrl = 'https://songpress.skeed.it/xmlrpc'
		else:
			self.updateUrl = u
		d = self.config.Read('lastCheck')
		if not d:
			self.updateLastCheck = None
		else:
			self.updateLastCheck = datetime.datetime.fromordinal(int(d))
		

	def Bool2String(self, param):
		return "1" if param else "0"

	def Save(self):
		self.config.SetPath('/Format')
		if self.chorusLabel is not None:
			self.config.Write('ChorusLabel', self.chorusLabel)
		self.config.Write('ShowChords', str(self.format.showChords))
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
		self.config.Write('easyKey', self.Bool2String(self.autoAdjustEasyKey))
		self.config.SetPath('/AutoAdjust/EasyChordsGroups')
		for k in easyChordsOrder:
			self.config.Write(k, str(self.GetEasyChordsGroup(k)))
		self.config.SetPath('/App')
		self.config.Write('defaultExtension', self.defaultExtension)
		if self.locale is not None:
			lang = self.config.Write('locale', self.locale)
		self.config.SetPath('/AutoUpdate')
		self.config.Write('frequency', str(self.updateFrequency))
		self.config.Write('ignored', ",".join(self.ignoredUpdates))
		self.config.Write('url', self.updateUrl)
		if self.updateLastCheck is not None:
			self.config.Write('lastCheck', str(self.updateLastCheck.toordinal()))

	def SetChorusLabel(self, c):
		self.chorusLabel = c
		self.decoratorFormat.SetChorusLabel(c)

	def SetDefaultNotation(self, notation):
		self.defaultNotation = notation
		self.notations = [x for x in self.notations if x.id == notation] + [x for x in self.notations if x.id != notation]

	def SetEasyChordsGroup(self, group, level):
		self.easyChordsGroup[group] = level
		self.easyChords = None

	def GetEasyChordsGroup(self, group):
		return self.easyChordsGroup[group]

	def GetEasyChords(self):
		if self.easyChords is None:
			self.easyChords = {'Eb': -1}
			for k in easyChords:
				chords = easyChords[k][1]
				l = self.easyChordsGroup[k] / 4.0
				for c in chords:
					if c in self.easyChords:
						self.easyChords[c] = max(self.easyChords[c], l)
					else:
						self.easyChords[c] = l

		return self.easyChords
