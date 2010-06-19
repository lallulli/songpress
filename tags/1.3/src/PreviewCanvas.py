###############################################################
# Name:			 PreviewCanvas.py
# Purpose:	 Window containing preview
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-21
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import wx
from Renderer import *

class PreviewCanvas(object):
	def __init__(self, parent, sf, sd = SongDecorator()):
		object.__init__(self)
		self.panel = wx.ScrolledWindow(parent, style=wx.BORDER_DOUBLE)
		self.panel.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		self.pixedScrolled = 10
		self.panel.SetScrollbars(self.pixedScrolled, self.pixedScrolled, 0, 0)
		self.panel.Bind(wx.EVT_PAINT, self.OnPaint, self.panel)
		self.panel.SetBackgroundColour(wx.WHITE)
		self.text = ""
		self.panel.Show()
		#SongFormat
		self.renderer = Renderer(sf, sd)

	def OnPaint(self, e):
		#print("OnPaint")
		dc = wx.AutoBufferedPaintDC(self.panel)
		self.panel.DoPrepareDC(dc)
		dc.SetBackground(wx.WHITE_BRUSH)
		dc.Clear()
		w, h = self.renderer.Render(self.text, dc)
		self.panel.SetVirtualSize(wx.Size(w, h))

	def Refresh(self, text):
		self.text = text
		self.panel.Refresh()

	def SetDecorator(self, sd):
		self.renderer.SetDecorator(sd)
