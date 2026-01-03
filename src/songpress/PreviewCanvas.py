###############################################################
# Name:             PreviewCanvas.py
# Purpose:     Window containing preview
# Author:         Luca Allulli (webmaster@roma21.it)
# Created:     2009-02-21
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:     GNU GPL v2
##############################################################

import platform

import wx
import wx.adv

from .Renderer import *


_ = wx.GetTranslation


class PreviewCanvas(object):
    def __init__(self, parent, sf, notations, sd=SongDecorator(), embedded=False):
        object.__init__(self)
        self.main_panel = wx.Window(parent)
        bSizer = wx.BoxSizer(wx.VERTICAL)
        parent = self.main_panel
        if not embedded:
            self.link = wx.adv.HyperlinkCtrl(parent, 0, _("Copy formatted song to clipboard"), '')
            tt = wx.ToolTip(_("Copy formatted song to clipboard, so that it can be pasted in any program and printed"))
            self.link.SetToolTip(tt)
            bSizer.Add(self.link, 0, wx.EXPAND)
        self.panel = wx.ScrolledWindow(parent, style=wx.BORDER_DOUBLE)
        self.panel.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.pixedScrolled = 10
        self.panel.SetScrollbars(self.pixedScrolled, self.pixedScrolled, 0, 0)
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint, self.panel)
        self.panel.SetBackgroundColour(wx.WHITE)
        self.text = ""
        bSizer.Add(self.panel, 1, wx.EXPAND)
        #SongFormat
        self.renderer = Renderer(sf, sd, notations)
        self.main_panel.SetSizer(bSizer)
        self.main_panel.Layout()


    def OnPaint(self, e):
        #print("OnPaint")
        dc = wx.AutoBufferedPaintDC(self.panel)
        self.panel.PrepareDC(dc)
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()
        w, h = self.renderer.Render(self.text, dc)
        self.panel.SetVirtualSize(wx.Size(int(w), int(h)))
        

    def Refresh(self, text):
        self.text = text
        self.panel.Refresh()

    def SetDecorator(self, sd):
        self.renderer.SetDecorator(sd)
