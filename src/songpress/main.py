###############################################################
# Name:             main.py
# Purpose:     Entry point for Songpress
# Author:         Luca Allulli (webmaster@roma21.it)
# Created:     2009-01-16
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:     GNU GPL v2
##############################################################

from datetime import timedelta
import platform
import sys, os

import wx

from songpress.get_metrics import get_song_metrics
from songpress.optimization.optimization import Problem
from .Globals import glb
from . import i18n
from . import dev_tool


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
            print("Setting language ", l)
            i18n.setLang(l)
        else:
            print("Setting system language ")
            i18n.setSystemLang()

        from . import SongpressFrame
        self.res = wx.xrc.XmlResource(glb.AddPath("xrc/songpress.xrc"))
        self.songpressFrame = SongpressFrame.SongpressFrame(self.res)
        return True


def main():
    if "--create-shortcuts" in sys.argv:
        from .shortcuts import create_shortcuts
        create_shortcuts()
        return

    sys.excepthook = dev_tool.ExceptionHook
    if platform.system() == 'Windows':
        import ctypes
        appid = f'songpress.{glb.VERSION}'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
    songpressApp = SongpressApp()

    if '--get-metrics' in sys.argv:
        filename = sys.argv[-1]
        sm = get_song_metrics(filename, songpressApp.songpressFrame.pref.format)
        print(sm)
        return

    if '--optimize' in sys.argv:
        filename = sys.argv[-1]
        sm = get_song_metrics(filename, songpressApp.songpressFrame.pref.format)
        p = Problem(sm)
        p.optimize(time_limit=timedelta(seconds=120), restarts=3)
        return

    songpressApp.MainLoop()


if __name__ == '__main__':
    main()
