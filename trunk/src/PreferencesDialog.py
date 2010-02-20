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

i18n.register('PreferencesDialog')

class PreferencesDialog(wx.Dialog):
	def __init__(self, parent, id, title, preferences):
		wx.Dialog.__init__(self, parent, id, title, size=wx.Size(540, 480))

		self.pref = preferences

		self.config = wx.Config.Get()
		self.config.SetPath('/Editor')
		font = self.config.Read('Face')
		size = self.config.Read('Size')

		# Font face and size
		hSizer1 = wx.BoxSizer(wx.HORIZONTAL)

		m_staticText1 = wx.StaticText(self, wx.ID_ANY, _("Editor font"))
		m_staticText1.Wrap(-1);
		hSizer1.Add(m_staticText1, 0, wx.ALL, 5)

		self.fontCB = FontComboBox(self, wx.ID_ANY, font)
		self.Bind(wx.EVT_COMBOBOX, self.OnFontSelected, self.fontCB)
		self.fontCB.Bind(wx.EVT_KILL_FOCUS, self.OnFontSelected, self.fontCB)
		self.fontCB.Bind(wx.EVT_TEXT_ENTER, self.OnFontSelected, self.fontCB)
		hSizer1.Add(self.fontCB, 5, wx.EXPAND | wx.ALL, 5)

		m_staticText3 = wx.StaticText(self, wx.ID_ANY, _("Size"))
		m_staticText3.Wrap(-1);
		hSizer1.Add(m_staticText3, 0, wx.ALL, 5)

		self.sizeCB = wx.ComboBox(self, wx.ID_ANY, size)
		self.sizeCB.AppendItems([str(x) for x in [7,8,9,10,11,12,13,14,16,18,20]])
		self.Bind(wx.EVT_COMBOBOX, self.OnFontSelected, self.sizeCB)
		self.sizeCB.Bind(wx.EVT_KILL_FOCUS, self.OnFontSelected, self.sizeCB)
		self.sizeCB.Bind(wx.EVT_TEXT_ENTER, self.OnFontSelected, self.sizeCB)
		hSizer1.Add(self.sizeCB, 1, wx.EXPAND | wx.ALL, 5)

		# Preview
		hSizer2 = wx.BoxSizer(wx.HORIZONTAL)

		m_staticText2 = wx.StaticText(self, wx.ID_ANY, _("Preview"))
		m_staticText2.Wrap(-1)
		hSizer2.Add(m_staticText2, 0, wx.ALL, 5)

		self.frame = self
		self.editor = Editor.Editor(self, False)
		previewSong = _("{t:My Bonnie}\n\nMy [D]Bonnie lies [G]over the [D]ocean\noh [G]bring back my [A]Bonnie to [D]me!\n\n{soc}\n[D]Bring back, [E-]bring back,\n[A]bring back my Bonnie to [D]me!\n{eoc}")
		self.editor.SetText(previewSong)
		self.editor.SetFont(font, int(size))
		self.editor.SetReadOnly(True)

		hSizer2.Add(self.editor, 1, wx.EXPAND | wx.ALL, 5)

		# AutoAdjust
		staticBox = wx.StaticBox(self, wx.ID_ANY, _("Auto adjust"))
		self.staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		self.autoRemoveBlankLines = wx.CheckBox(self, wx.ID_ANY, _("Offer to remove blank lines"))
		self.staticBoxSizer.Add(self.autoRemoveBlankLines)
		self.autoTab2Chordpro = wx.CheckBox(self, wx.ID_ANY, _("Offer to convert songs in tab format to ChordPro"))
		self.staticBoxSizer.Add(self.autoTab2Chordpro)

		# Language
		hSizer3 = wx.BoxSizer(wx.HORIZONTAL)
		m_staticText1 = wx.StaticText(self, wx.ID_ANY, _("Language"))
		m_staticText1.Wrap(-1);
		hSizer3.Add(m_staticText1, 0, wx.ALL, 5)

		self.config.SetPath('/App')
		lang = self.config.Read('locale')
		if not lang:
			lang = i18n.getLang()
		self.langCh = wx.Choice(self, wx.ID_ANY)
		for l in glb.languages:
			i = self.langCh.Append(glb.languages[l])
			self.langCh.SetClientData(i, l)
			if lang == l:
				self.langCh.SetSelection(i)
		hSizer3.Add(self.langCh, 1, wx.EXPAND | wx.ALL, 5)

		# Default notation
		hSizer4 = wx.BoxSizer(wx.HORIZONTAL)
		m_staticText4 = wx.StaticText(self, wx.ID_ANY, _("Default notation"))
		m_staticText4.Wrap(-1);
		hSizer4.Add(m_staticText4, 0, wx.ALL, 5)

		self.notationCh = wx.Choice(self, wx.ID_ANY)
		for n in self.pref.notations:
			i = self.notationCh.Append(n.desc)
			self.notationCh.SetClientData(i, n.id)
		self.notationCh.SetSelection(0)
		hSizer4.Add(self.notationCh, 1, wx.EXPAND | wx.ALL, 5)

		# Buttons
		hSizerZ = wx.BoxSizer(wx.HORIZONTAL)
		hSizerZ.AddStretchSpacer(1)

		self.ok = wx.Button(self, wx.ID_OK, _("OK"))
		hSizerZ.Add(self.ok, 0, wx.ALL, 5 )

		self.cancel = wx.Button(self, wx.ID_CANCEL, _("Cancel"))
		hSizerZ.Add(self.cancel, 0, wx.ALL, 5)

		# Pack horizontal sizers vertically
		bSizer1 = wx.BoxSizer(wx.VERTICAL)
		bSizer1.AddSizer(hSizer1, 0, wx.EXPAND, 5)
		bSizer1.AddSizer(hSizer2, 1, wx.EXPAND, 5)
		bSizer1.AddSizer(self.staticBoxSizer, 0, wx.EXPAND, 5)
		bSizer1.AddSizer(hSizer3, 0, wx.EXPAND, 5)
		bSizer1.AddSizer(hSizer4, 0, wx.EXPAND, 5)
		bSizer1.Add(hSizerZ, 0, wx.EXPAND, 5)

		self.SetSizer(bSizer1)
		self.Layout()


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


