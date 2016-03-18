###############################################################
# Name:			 PreviewCanvas.py
# Purpose:	 Window containing preview
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-21
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import wx
import platform

from Renderer import *

import i18n
i18n.register('PreviewCanvas')

class PreviewCanvas(object):
	def __init__(self, parent, sf, notations, sd=SongDecorator(), embedded=False):
		object.__init__(self)
		if not embedded:
			self.main_panel = wx.Window(parent)
			bSizer = wx.BoxSizer(wx.VERTICAL)
			self.link = wx.HyperlinkCtrl(self.main_panel, 0, _("Copy formatted song to clipboard"), '')
			tt = wx.ToolTip(_("Copy formatted song to clipboard, so that it can be pasted in any program and printed"))
			self.link.SetToolTip(tt)
			if platform.system() != 'Linux':
				bSizer.Add(self.link, 0, wx.EXPAND)
			parent = self.main_panel
		self.panel = wx.ScrolledWindow(parent, style=wx.BORDER_DOUBLE)
		self.panel.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		self.pixedScrolled = 10
		self.panel.SetScrollbars(self.pixedScrolled, self.pixedScrolled, 0, 0)
		self.panel.Bind(wx.EVT_PAINT, self.OnPaint, self.panel)
		self.panel.SetBackgroundColour(wx.WHITE)
		self.text = ""
		if not embedded:
			bSizer.Add(self.panel, 1, wx.EXPAND)
		#SongFormat
		self.renderer = Renderer(sf, sd, notations)
		if not embedded:
			self.main_panel.SetSizer(bSizer)
			self.main_panel.Layout()


	def OnPaint(self, e):
		#print("OnPaint")
		dc = wx.AutoBufferedPaintDC(self.panel)
		self.panel.PrepareDC(dc)
		dc.SetBackground(wx.WHITE_BRUSH)
		dc.Clear()
		w, h = self.renderer.Render(self.text, dc)
		self.panel.SetVirtualSize(wx.Size(w, h))
		

	def Refresh(self, text):
		self.text = text
		self.panel.Refresh()

	def SetDecorator(self, sd):
		self.renderer.SetDecorator(sd)
