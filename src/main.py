###############################################################
# Name:             main.py
# Purpose:     Entry point for Songpress
# Author:         Luca Allulli (webmaster@roma21.it)
# Created:     2009-01-16
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:     GNU GPL v2
##############################################################

import sys, os
import SongpressFrame
import wx
from Globals import glb
import i18n
import dev_tool


class SongpressApp(wx.App):
    def OnInit(self):
        self.SetAppName("songpress")
        glb.InitDataPath()
        self.config = wx.FileConfig(localFilename=os.path.join(glb.data_path, "config.ini"))
        wx.Config.Set(self.config)
        i18n.init(glb.default_language, [l for l in glb.languages])
        self.config.SetPath("/App")
        l = self.config.Read("locale")
        if l:
            i18n.setLang(l)
        else:
            i18n.setSystemLang()
        self.res = wx.xrc.XmlResource(glb.AddPath("xrc/songpress.xrc"))
        songpressFrame = SongpressFrame.SongpressFrame(self.res)
        return True


if __name__ == '__main__':
    sys.excepthook = dev_tool.ExceptionHook
    songpressApp = SongpressApp()
    songpressApp.MainLoop()
