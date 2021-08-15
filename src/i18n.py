###############################################################
# Name:			 i18n.py
# Purpose:	 Support internationalization
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-09-11
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

import gettext
import inspect
import os
import os.path
import locale
import sys
from Globals import *


registered_modules = []
# 2-character language code of current language
current_language = None
# wxPython wx.Locale object for current language
mylocale = None
# 2-character language code of default language, set during init
defaultLang = None
# Array mapping 2-character language codes of languages supported by Songpress
# to language names. To be set during init phase, by calling init function
supportedLangs = None


"""
Client shall:
1. Call `init`
2. Call either `setLang` (if a langugage is chosen by the user)
   or `setSystemLang`
"""


def init(default_lang, supported_langs):
	global defaultLang
	global supportedLangs
	defaultLang = default_lang
	supportedLangs = supported_langs


_ = lambda x: x


def setLang(l):
	global current_language
	current_language = l
	for mod in registered_modules:
		mod._ = wx.GetTranslation


def getLang():
	return current_language


def setSystemLang():
	l = locale.getdefaultlocale()
	if l is not None and l[0][:2] in supportedLangs:
		setLang(l[0][:2])
	else:
		setLang(defaultLang)


def register(moduleName=None):
	if moduleName is None:
		# Try to determine caller module name
		frm = inspect.stack()[1]
		mod = inspect.getmodule(frm[0])
		moduleName = mod.__name__
	else:
		mod = sys.modules[moduleName]
	registered_modules.append(mod)
	if current_language == defaultLang:
		mod._ = gettext.NullTranslations().gettext
	else:
		mod._ = wx.GetTranslation


def localizeXrc(filename):
	import wx
	if current_language != defaultLang:
		langid = wx.Locale.FindLanguageInfo(current_language).Language
		d, domain = os.path.split(filename)
		localedir = os.path.join(glb.AddPath(d), "locale")
		# Set locale for wxWidgets
		global mylocale
		mylocale = wx.Locale(langid)
		mylocale.AddCatalogLookupPathPrefix(localedir)
		mylocale.AddCatalog(domain)
