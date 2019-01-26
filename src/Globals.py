# coding: utf-8

###############################################################
# Name:			 Globals.py
# Purpose:	 Hold global settings
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-09-04
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

import os.path
import sys
import wx

class Globals(object):
	def __init__(self):
		object.__init__(self)
		self.path = os.path.abspath(os.path.dirname(sys.argv[0]))

	def AddPath(self, filename):
		return os.path.join(self.path, filename)

	languages = {
		'en': "English",
		'it': "Italiano",
		'fr': u"Français",
		'es': u"Español",
	}

	translators = {
		'en': "Luca Allulli",
		'it': "Luca Allulli",
		'fr': "Raoul Schmitt",
		'es': "Miguel Dell'Uomini",
	}

	default_language = 'en'

	PROG_NAME = 'Songpress'
	VERSION = '1.7'
	BUG_REPORT_ADDRESS = 'luca@skeed.it'
	YEAR = '2019'

glb = Globals()




