###############################################################
# Name:			 PreviewCanvas.py
# Purpose:	 Window containing preview
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-21
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

import wx
from Renderer import *

class PreviewCanvas(object):
	def __init__(self, parent, sf, sd = SongDecorator()):
		object.__init__(self)
		self.frame = wx.Frame(parent, -1, "Preview")
		self.frame.Bind(wx.EVT_PAINT, self.OnPaint, self.frame)
		self.frame.SetBackgroundColour(wx.WHITE)
		self.text = ""
		self.frame.Show()
		#SongFormat
		self.renderer = Renderer(sf, sd)
		
	def OnPaint(self, e):		
		print("OnPaint")
		dc = wx.PaintDC(self.frame)
		self.renderer.Render(self.text, dc)
		
	def Refresh(self, text):
		self.text = text
		self.frame.Refresh()
