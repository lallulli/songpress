
# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Mar 10 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
from . import i18n
i18n.register('songpress.NotationDialog')

###########################################################################
## Class NotationDialog
###########################################################################

class NotationDialog(wx.Dialog):

	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=_(u"Change notation"), pos=wx.DefaultPosition,
											 size=wx.Size(361, 175), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

		bSizer1 = wx.BoxSizer(wx.VERTICAL)

		bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

		self.label1 = wx.StaticText(self, wx.ID_ANY, _(u"From notation:"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.label1.Wrap(-1)
		bSizer2.Add(self.label1, 0, wx.ALL, 5)

		fromNotationChoices = []
		self.fromNotation = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, fromNotationChoices, 0)
		self.fromNotation.SetSelection(0)
		bSizer2.Add(self.fromNotation, 1, wx.ALL, 5)

		bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

		bSizer21 = wx.BoxSizer(wx.HORIZONTAL)

		self.label11 = wx.StaticText(self, wx.ID_ANY, _(u"To notation:"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.label11.Wrap(-1)
		bSizer21.Add(self.label11, 0, wx.ALL, 5)

		toNotationChoices = []
		self.toNotation = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, toNotationChoices, 0)
		self.toNotation.SetSelection(0)
		bSizer21.Add(self.toNotation, 1, wx.ALL, 5)

		bSizer1.Add(bSizer21, 1, wx.EXPAND, 5)

		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1OK = wx.Button(self, wx.ID_OK)
		m_sdbSizer1.AddButton(self.m_sdbSizer1OK)
		self.m_sdbSizer1Cancel = wx.Button(self, wx.ID_CANCEL)
		m_sdbSizer1.AddButton(self.m_sdbSizer1Cancel)
		m_sdbSizer1.Realize();

		bSizer1.Add(m_sdbSizer1, 0, wx.ALL | wx.EXPAND, 5)

		self.SetSizer(bSizer1)
		self.Layout()

		# Connect Events
		self.fromNotation.Bind(wx.EVT_CHOICE, self.OnFromNotation)

	def __del__(self):
		pass

	# Virtual event handlers, overide them in your derived class
	def OnFromNotation(self, event):
		event.Skip()


