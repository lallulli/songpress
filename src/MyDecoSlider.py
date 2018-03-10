###############################################################
# Name:			 MyDecoSlider.py
# Purpose:	 Slider with a decorated range indicator
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2010-06-02
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

from DecoSlider import *
import wx

class MyDecoSlider(DecoSlider):
	def __init__(self, parent):
		DecoSlider.__init__(self, parent)

	def OnPaint(self, event):
		dc = wx.PaintDC(self.panel)
		w, h = dc.GetSize()
		dc.Clear()
		green =	wx.Colour(0, 255, 0)
		brush = wx.Brush(green, wx.SOLID)
		dc.SetBrush(brush)
		dc.DrawPolygon([wx.Point(0, 0), wx.Point(w - 1, 0), wx.Point(w - 1, h - 1)])

	def OnSize(self, event):
		self.panel.Refresh()
