###############################################################
# Name:			 PreviewCanvas.py
# Purpose:	 Window containing preview
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-21
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

import wx
from wx import xrc
from VerseChorusHandler import *
from SongTokenizer import *

class PreviewCanvas(object):
	"""Abstract class. Override methods New, Open, Save"""
	###UI generation###

	def __init__(self, parent, vh = VerseHandler(), ch = ChorusHandler()):
		self.frame = wx.Frame(parent, -1, "Preview")
		self.frame.Bind(wx.EVT_PAINT, self.OnPaint, self.frame)
		self.frame.SetBackgroundColour(wx.WHITE)
		self.text = ""
		self.frame.Show()
		self.vh = vh
		self.ch = ch
		
	def OnPaint(self, e):
		dc = wx.PaintDC(self.frame)
		for l in self.text.splitlines():
			tkz = SongTokenizer(l)
			for tok in tkz:
				pass
		
	def Refresh(self, text):
		self.text = text
		self.frame.Refresh()
