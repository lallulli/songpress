###############################################################
# Name:			 main.py
# Purpose:	 Entry point for Songpress
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-16
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

		
import wx
from wx import xrc
from SDIMainFrame import *

class SongpressFrame(SDIMainFrame):

	def __init__(self, res):
		SDIMainFrame.__init__(self, res, 'MainFrame', 'Songpress - Il Canzonatore', 'Luca Allulli', 'song', 'crd')


class SongpressApp(wx.App):

	def OnInit(self):
		self.res = xrc.XmlResource('xrc/songpress.xrc')
		songpressFrame = SongpressFrame(self.res)
		return True





if __name__ == '__main__':
	songpressApp = SongpressApp()
	songpressApp.MainLoop()
