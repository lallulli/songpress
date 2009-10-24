###############################################################
# Name:			 main.py
# Purpose:	 Entry point for web2help
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-08-24
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import wx
from wx import xrc
from Web2helpFrame import *
from Globals import glb

class Web2helpApp(wx.App):

	def OnInit(self):
		self.config = wx.FileConfig("web2help")
		wx.Config.Set(self.config)
		self.res = xrc.XmlResource(glb.AddPath("xrc/web2help.xrc"))
		web2helpFrame = Web2helpFrame(self.res)
		
		return True

if __name__ == '__main__':
	web2helpApp = Web2helpApp()
	web2helpApp.MainLoop()
