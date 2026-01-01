# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Mar 10 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

# Nothing to localize in this module, because all strings are "dummy" placeholders to be replaced

_ = lambda x: x


###########################################################################
## Class ListDialog
###########################################################################

class ListDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=_(u"Songpress"), pos=wx.DefaultPosition,
                                             size=wx.Size(413, 240), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer24 = wx.BoxSizer(wx.VERTICAL)

        self.label = wx.StaticText(self, wx.ID_ANY, _(u"Label text"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.label.Wrap(-1)
        bSizer24.Add(self.label, 0, wx.ALL, 5)

        elementsChoices = []
        self.elements = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, elementsChoices, wx.LB_SINGLE)
        bSizer24.Add(self.elements, 3, wx.ALL | wx.EXPAND, 5)

        m_sdbSizer5 = wx.StdDialogButtonSizer()
        self.m_sdbSizer5OK = wx.Button(self, wx.ID_OK)
        m_sdbSizer5.AddButton(self.m_sdbSizer5OK)
        self.m_sdbSizer5Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer5.AddButton(self.m_sdbSizer5Cancel)
        m_sdbSizer5.Realize();

        bSizer24.Add(m_sdbSizer5, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer24)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass


