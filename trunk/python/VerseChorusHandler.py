###############################################################
# Name:			 VerseChorusHandler.py
# Purpose:	 Base (and default) handlers for verse and chorus
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-21
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

class VerseHandler(object):
	def Begin(x, y):
		return (0, 0)
	def End(x, y):
		return y
	
class ChorusHandler(object):
	def Begin(x, y):
		return (0, 0)
	def End(x, y):
		return y
	