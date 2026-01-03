# coding: utf-8

###############################################################
# Name:             Globals.py
# Purpose:     Hold global settings
# Author:         Luca Allulli (webmaster@roma21.it)
# Created:     2009-09-04
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:     GNU GPL v2
##############################################################

import os.path
import sys
import shutil

import wx


class Globals(object):
    def __init__(self):
        object.__init__(self)
        current_file = os.path.abspath(__file__)
        self.path = os.path.dirname(current_file)
        self.data_path = None

    def InitDataPath(self):
        sp = wx.StandardPaths.Get()
        portable_config = os.path.join(self.path, 'config.ini')
        if os.path.isfile(portable_config):
            # Monkey-patch StandardPaths instance so that portable config.ini is used
            def my_get(*args, **kwargs):
                return self.path
            sp.GetUserDataDir = my_get

        self.data_path = sp.GetUserDataDir()
        old_config = None
        if os.path.isfile(self.data_path):
            old_config = self.data_path + ".orig"
            shutil.move(self.data_path, old_config)
        if not os.path.exists(self.data_path):
            shutil.copytree(os.path.join(self.path, 'templates', 'local_dir'), self.data_path)
        if old_config is not None:
            # Preserve old config file, but don't use it
            shutil.move(old_config, os.path.join(self.data_path, "config.ini.orig"))

    def AddPath(self, filename):
        return os.path.join(self.path, filename)

    def ListLocalGlobalDir(self, rel_path):
        """
        List both the local (data) and global (program) versions of a directory

        :param rel_path: relative path
        :return: list of absolute paths of files
        """
        out = []
        for f in os.listdir(os.path.join(self.path, rel_path)):
            out.append(os.path.join(self.path, rel_path, f))
        for f in os.listdir(os.path.join(self.data_path, rel_path)):
            out.append(os.path.join(self.data_path, rel_path, f))
        return out

    languages = {
        'en': "English",
        'it': "Italiano",
        'fr': u"Français",
        'es': u"Español",
        'de': u"German",
    }

    translators = {
        'en': "Luca Allulli",
        'it': "Luca Allulli",
        'fr': "Raoul Schmitt",
        'es': "Miguel Dell'Uomini",
        'de': "Axel Schneider",
    }

    default_language = 'en'

    PROG_NAME = 'Songpress'
    VERSION = '1.9.0rc2'
    BUG_REPORT_ADDRESS = 'luca@skeed.it'
    YEAR = '2026'

glb = Globals()
