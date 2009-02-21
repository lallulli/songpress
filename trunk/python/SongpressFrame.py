###############################################################
# Name:			 SongpressFrame.py
# Purpose:	 Main frame for Songpress
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-16
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

import wx
from wx import xrc
from SDIMainFrame import *
from Editor import *
from PreviewCanvas import *

class SongpressFrame(SDIMainFrame):

	def __init__(self, res):
		SDIMainFrame.__init__(self, res, 'MainFrame', 'Songpress - Il Canzonatore', 'Luca Allulli', 'song', 'crd')
		self.text = Editor(self)
		self.previewCanvas = PreviewCanvas(self.frame)

	def New(self):
		self.text.New();
		
	def Open(self):
		self.text.Open()
		
	def Save(self):
		self.text.Save()
		
