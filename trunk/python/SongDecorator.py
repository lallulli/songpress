###############################################################
# Name:			 SongDecorator.py
# Purpose:	 Base (and default) handlers for verse and chorus
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-21
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

from SongFormat import *

class SongDecorator(object):
	def __init__(self, sf = None):
		object.__init__(self)
		# Song format
		self.sf = sf
		
	def BeginVerse(self, x, y):
		return (0, 0)

	def EndVerse(self, x, y):
		return y

	def BeginChorus(self, x, y):
		return (0, 0)

	def EndChorus(self, x, y):
		return y
	