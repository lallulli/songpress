###############################################################
# Name:			 main.py
# Purpose:	 Entry point for Songpress
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-16
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import wx
from wx import xrc
from SongpressFrame import *

class SongpressApp(wx.App):

	def OnInit(self):
		self.res = xrc.XmlResource('xrc/songpress.xrc')
		songpressFrame = SongpressFrame(self.res)
		
		return True


if __name__ == '__main__':
	songpressApp = SongpressApp()
	songpressApp.MainLoop()
