###############################################################
# Name:			 VerseChorusHandler.py
# Purpose:	 Base (and default) handlers for verse and chorus
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-21
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

class VerseHandler(object):
	def GetOffset(verseNumber):
		return (0, 0)
	def Draw(y, width, height):
		return 0
	
class ChorusHandler(object):
	def GetOffset(verseNumber):
		return (0, 0)
	def Draw(y, width, height):
		return 0
	