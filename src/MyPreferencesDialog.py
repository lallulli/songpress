###############################################################
# Name:			 PreferencesDialog.py
# Purpose:	 Allow user to set preferences
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-10-02
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import wx
from FontComboBox import FontComboBox
import i18n
import Editor
from Globals import glb
from PreferencesDialog import PreferencesDialog
from MyDecoSlider import MyDecoSlider

#i18n.register('MyPreferencesDialog')
_ = lambda x: x

class MyPreferencesDialog(PreferencesDialog):
	def __init__(self, parent, id, title, preferences, easyChords):
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
		if not self.pref.locale is None:
			lang = i18n.getLang()
		else:
			lang = self.pref.locale
		for l in glb.languages:
			i = self.langCh.Append(glb.languages[l])
			self.langCh.SetClientData(i, l)
			if lang == l:
				self.langCh.SetSelection(i)

		# Default notation
		for n in self.pref.notations:
			i = self.notationCh.Append(n.desc)
			self.notationCh.SetClientData(i, n.id)
		self.notationCh.SetSelection(0)

		# Easy chords
		simplifyGrid = wx.FlexGridSizer(len(easyChords), 2, 0, 0)
		simplifyGrid.AddGrowableCol(1, 1)
		self.simplifyPanel.SetSizer(simplifyGrid)
		self.simplifyPanel.Layout()

		for k in easyChords:
			simplifyGrid.Add(wx.StaticText(self.simplifyPanel, wx.ID_ANY, k[0], wx.DefaultPosition, wx.DefaultSize, 0), 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
			simplifyGrid.Add(MyDecoSlider(self.simplifyPanel), 1, wx.EXPAND, 5)

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

	def OnOk(self, evt):
		self.pref.editorFace, self.pref.editorSize = self.GetFont()
		l = self.GetLanguage()
		lang = i18n.getLang()
		if l != lang:
			msg = _("Language settings will be applied when you restart Songpress.")
			d = wx.MessageDialog(self, msg, _("Songpress"), wx.ICON_INFORMATION | wx.OK)
			d.ShowModal()
		self.pref.locale = l
		self.pref.SetDefaultNotation(self.GetNotation())
		self.pref.autoAdjustSpuriousLines = self.autoRemoveBlankLines.GetValue()
		self.pref.autoAdjustTab2Chordpro = self.autoTab2Chordpro.GetValue()
		evt.Skip(True)

