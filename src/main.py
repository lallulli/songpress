###############################################################
# Name:			 main.py
# Purpose:	 Entry point for Songpress
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-16
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

from SongpressFrame import *
import wx
from wx import xrc
from Globals import glb
import i18n
import dev_tool

class SongpressApp(wx.App):

	def OnInit(self):
		self.config = wx.FileConfig("songpress")
		wx.Config.Set(self.config)
		i18n.init(glb.default_language, [l for l in glb.languages])
		self.config.SetPath("/App")
		l = self.config.Read("locale")
		if l:
			i18n.setLang(l)
		else:
			i18n.setSystemLang()
		self.res = xrc.XmlResource(glb.AddPath("xrc/songpress.xrc"))
		songpressFrame = SongpressFrame(self.res)

		return True


if __name__ == '__main__':
	sys.excepthook = dev_tool.ExceptionHook
	songpressApp = SongpressApp()
	songpressApp.MainLoop()
