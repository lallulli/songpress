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

reg = []
lang = ['']
mylocale = [None]

def GetDomainAndLocale(name):
	d, f = os.path.split(name.replace('.', '/'))
	return (f, os.path.join(d, "locale"))

def localizeXrc(filename):
	import wx
	langid = wx.LANGUAGE_ITALIAN    # use OS default; or use LANGUAGE_JAPANESE, etc.
	d, domain = os.path.split(filename)
	localedir = os.path.join(d, "locale")
	# Set locale for wxWidgets
	mylocale[0] = wx.Locale(langid)
	mylocale[0].AddCatalogLookupPathPrefix(localedir)
	#print localedir
	mylocale[0].AddCatalog(domain)
	#print domain


def setLang(l):
	lang[0] = l
	for mod in reg:
		d, loc = GetDomainAndLocale(mod.__name__)
		mod._ = gettext.translation(d, loc, languages=lang, codeset="iso-8859-1").ugettext


def register():
	# Determine caller module name
	frm = inspect.stack()[1]
	mod = inspect.getmodule(frm[0])
	d, loc = GetDomainAndLocale(mod.__name__)
	# Done
	reg.append(mod)
	if lang[0] == '':
		mod._ = gettext.NullTranslations().ugettext
	else:
		mod._ = gettext.translation(d, loc, languages=lang, codeset="iso-8859-1").ugettext
	
	
