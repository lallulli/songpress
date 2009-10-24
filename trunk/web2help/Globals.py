###############################################################
# Name:			 Globals.py
# Purpose:	 Hold global settings
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-09-04
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import os.path
import sys
import wx
import re

class Globals(object):
	def __init__(self):
		object.__init__(self)
		self.path = os.path.abspath(os.path.dirname(sys.argv[0]))
		self.splitUrl = re.compile(r'\[(http://.*)\]$')
		
	def AddPath(self, filename):
		return os.path.join(self.path, filename)
		
	def Join(self, title, url):
		if url[:7].lower() != 'http://':
			url = 'http://' + url
		return "%s [%s]" % (title, url)
		
	def Split(self, text):
		m = self.splitUrl.search(text)
		return (text[:m.start(0)-1], m.group(1))


glb = Globals()




