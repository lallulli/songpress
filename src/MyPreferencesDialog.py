###############################################################
# Name:			 PreferencesDialog.py
# Purpose:	 Allow user to set preferences
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-10-02
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

import wx
from FontComboBox import FontComboBox
import i18n
import Editor
from Globals import glb
from PreferencesDialog import PreferencesDialog
from MyDecoSlider import MyDecoSlider
from Transpose import *
from Preferences import get_update_frequencies

i18n.register('MyPreferencesDialog')

class MyPreferencesDialog(PreferencesDialog):
	def __init__(self, parent, preferences, easyChords):
		self.pref = preferences
		self.frame = self
		PreferencesDialog.__init__(self, parent)

		self.easyChords = easyChords

		self.fontCB.Bind(wx.EVT_TEXT_ENTER, self.OnFontSelected, self.fontCB)
		self.fontCB.Bind(wx.EVT_COMBOBOX, self.OnFontSelected, self.fontCB)

		previewSong = _("{t:My Bonnie}\n\nMy [D]Bonnie lies [G]over the [D]ocean\noh [G]bring back my [A]Bonnie to [D]me!\n\n{soc}\n[D]Bring back, [E-]bring back,\n[A]bring back my Bonnie to [D]me!\n{eoc}")
		self.editor.SetText(previewSong)
		self.editor.SetFont(self.pref.editorFace, self.pref.editorSize)
		self.editor.SetReadOnly(True)
		self.autoRemoveBlankLines.SetValue(self.pref.autoAdjustSpuriousLines)
		self.autoTab2Chordpro.SetValue(self.pref.autoAdjustTab2Chordpro)
		self.autoAdjustEasyKey.SetValue(self.pref.autoAdjustEasyKey)
		if self.pref.locale is None:
			lang = i18n.getLang()
		else:
			lang = self.pref.locale
		for l in glb.languages:
			i = self.langCh.Append(glb.languages[l])
			self.langCh.SetClientData(i, l)
			if lang == l:
				self.langCh.SetSelection(i)
		exts = ["crd", "pro", "chopro", "chordpro", "cho"]
		i = 0
		for e in exts:
			self.extension.Append(e)
			if e == self.pref.defaultExtension:
				self.extension.SetSelection(i)
			i += 1
				
		# Default notation
		for n in self.pref.notations:
			i = self.notationCh.Append(n.desc)
			self.notationCh.SetClientData(i, n.id)
		self.notationCh.SetSelection(0)		

		# Update frequency
		sel = 0
		uf = get_update_frequencies()
		for k in uf:
			i = self.frequency.Append(uf[k])
			self.frequency.SetClientData(i, k)
			if k == self.pref.updateFrequency:
				sel = i
		self.frequency.SetSelection(sel)

		# Easy chords
		simplifyGrid = wx.FlexGridSizer(len(easyChords), 2, 0, 0)
		simplifyGrid.AddGrowableCol(1, 1)
		self.simplifyPanel.SetSizer(simplifyGrid)
		self.simplifyPanel.Layout()

		self.decoSliders = {}
		for k in easyChordsOrder:
			simplifyGrid.Add(wx.StaticText(self.simplifyPanel, wx.ID_ANY, getEasyChordsDescription(easyChords[k]), wx.DefaultPosition, wx.DefaultSize, 0), 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
			ds = MyDecoSlider(self.simplifyPanel)
			self.decoSliders[k] = ds
			ds.slider.SetValue(self.pref.GetEasyChordsGroup(k))
			simplifyGrid.Add(ds, 1, wx.EXPAND, 5)

		simplifyGrid.FitInside(self.simplifyPanel)

		#self.simplifyPanel.Refresh()

	def OnFontSelected(self, evt):
		f, s = self.GetFont()
		self.editor.SetFont(f, s)
		evt.Skip()

	def GetFont(self):
		face = self.fontCB.GetValue()
		try:
			s = int(self.sizeCB.GetValue())
		except:
			s = 12
		return (face, s)

	def GetLanguage(self):
		return self.langCh.GetClientData(self.langCh.GetSelection())

	def GetNotation(self):
		return self.notationCh.GetClientData(self.notationCh.GetSelection())

	def GetUpdateFrequency(self):
		return self.frequency.GetClientData(self.frequency.GetSelection())

	def OnOk(self, evt):
		self.pref.editorFace, self.pref.editorSize = self.GetFont()
		self.pref.updateFrequency = self.GetUpdateFrequency()
		l = self.GetLanguage()
		lang = i18n.getLang()
		if l is not None and l != lang:
			msg = _("Language settings will be applied when you restart Songpress.")
			d = wx.MessageDialog(self, msg, _("Songpress"), wx.ICON_INFORMATION | wx.OK)
			d.ShowModal()
		self.pref.locale = l
		self.pref.SetDefaultNotation(self.GetNotation())
		self.pref.autoAdjustSpuriousLines = self.autoRemoveBlankLines.GetValue()
		self.pref.autoAdjustTab2Chordpro = self.autoTab2Chordpro.GetValue()
		self.pref.autoAdjustEasyKey = self.autoAdjustEasyKey.GetValue()
		for k in self.decoSliders:
			self.pref.SetEasyChordsGroup(k, self.decoSliders[k].slider.GetValue())
		self.pref.defaultExtension = self.extension.GetString(self.extension.GetSelection())
		evt.Skip(True)

