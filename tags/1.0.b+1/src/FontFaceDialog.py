###############################################################
# Name:			 FontFaceDialog.py
# Purpose:	 wxWidgets dialog with a FontComboBox
#            selector
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-08-14
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import wx
from PreviewCanvas import *
from FontComboBox import FontComboBox

previewSong = """{t:My Bonnie}

My [D]Bonnie is [G]over the [D]ocean
oh [G]bring back my [A]Bonnie to [D]me!

{soc}[D]Bring back, [E-]bring back,
[A]bring back my Bonnie to [D]me!{eoc}
"""

class FontFaceDialog(wx.Dialog):
	def __init__(self, parent, id, title, songFormat, songDecorator, decoratorFormat):
		self.format = songFormat
		self.originalFont = songFormat.face
		self.decoratorFormat = decoratorFormat
		wx.Dialog.__init__(self, parent, id, title, size=wx.Size(380, 280))

		bSizer1 = wx.BoxSizer(wx.VERTICAL)
		hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
		
		m_staticText1 = wx.StaticText(self, wx.ID_ANY, "Font")
		m_staticText1.Wrap(-1);
		hSizer1.Add(m_staticText1, 0, wx.ALL, 5)
		
		self.fontCB = FontComboBox(self, wx.ID_ANY, songFormat.face)
		self.Bind(wx.EVT_COMBOBOX, self.OnFontSelected, self.fontCB)
		hSizer1.Add(self.fontCB, 1, wx.EXPAND | wx.ALL, 5)

		hSizer2 = wx.BoxSizer(wx.HORIZONTAL)
		
		m_staticText2 = wx.StaticText(self, wx.ID_ANY, "Preview")
		m_staticText2.Wrap(-1)
		hSizer2.Add(m_staticText2, 0, wx.ALL, 5)
		
		self.previewCanvas = PreviewCanvas(self, songFormat, songDecorator)
		hSizer2.Add(self.previewCanvas.panel, 1, wx.EXPAND | wx.ALL, 5)
		self.previewCanvas.Refresh(previewSong)
		
		bSizer1.AddSizer(hSizer1, 0, wx.EXPAND, 5)
		bSizer1.AddSizer(hSizer2, 1, wx.EXPAND, 5)
		
		bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
		
		bSizer2.AddStretchSpacer(1)
		
		self.ok = wx.Button(self, wx.ID_OK, "OK")
		bSizer2.Add(self.ok, 0, wx.ALL, 5 )
		
		self.cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
		bSizer2.Add(self.cancel, 0, wx.ALL, 5)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel)
		
		bSizer1.Add(bSizer2, 0, wx.EXPAND, 5)
		
		self.SetSizer(bSizer1)
		self.Layout()
		
	def SetFont(self, font):
		self.format.face = font
		self.format.chord.face = font
		self.format.comment.face = font
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
		self.previewCanvas.Refresh(previewSong)	
		
	def OnFontSelected(self, evt):
		font = self.fontCB.GetValue()
		self.SetFont(font)
		
	def GetValue(self):
		return self.fontCB.GetValue()
		
	def OnCancel(self, evt):
		font = self.originalFont
		self.SetFont(font)
		evt.Skip()
		
