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

class Globals(object):
	def __init__(self):
		object.__init__(self)
		self.path = os.path.abspath(os.path.dirname(sys.argv[0]))
		
	def AddPath(self, filename):
		return os.path.join(self.path, filename)

glb = Globals()