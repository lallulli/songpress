###############################################################
# Name:			 i18n.py
# Purpose:	 Support internationalization
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-09-11
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import gettext
import inspect
import os
import os.path
import locale

reg = []
lang = ['']
mylocale = [None]
defaultLang = ['']
supportedLangs = [[]]

def GetDomainAndLocale(name):
	d, f = os.path.split(name.replace('.', '/'))
	return (f, os.path.join(d, "locale"))

def init(default_lang, supported_langs):
	defaultLang[0] = default_lang
	supportedLangs[0] = supported_langs

def setLang(l):
	lang[0] = l
	for mod in reg:
		if l != defaultLang[0]:
			d, loc = GetDomainAndLocale(mod.__name__)
			mod._ = gettext.translation(d, loc, languages=lang, codeset="iso-8859-1").ugettext
		else:
			mod._ = gettext.NullTranslations().ugettext

def getLang():
	return lang[0]
			
def setSystemLang():
	l = locale.getdefaultlocale()
	if l is not None and l[0][:2] in supportedLangs[0]:
		setLang(l[0][:2])
	else:
		setLang(defaultLang[0])

def register():
	# Determine caller module name
	frm = inspect.stack()[1]
	mod = inspect.getmodule(frm[0])
	d, loc = GetDomainAndLocale(mod.__name__)
	# Done
	reg.append(mod)
	if lang[0] == defaultLang[0]:
		mod._ = gettext.NullTranslations().ugettext
	else:
		mod._ = gettext.translation(d, loc, languages=lang, codeset="iso-8859-1").ugettext


def localizeXrc(filename):
	import wx
	if lang[0] != defaultLang[0]:
		langid = wx.Locale.FindLanguageInfo(lang[0]).Language		
		d, domain = os.path.split(filename)
		localedir = os.path.join(d, "locale")
		# Set locale for wxWidgets
		mylocale[0] = wx.Locale(langid)
		mylocale[0].AddCatalogLookupPathPrefix(localedir)
		mylocale[0].AddCatalog(domain)
