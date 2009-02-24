###############################################################
# Name:			 SongFormat.py
# Purpose:	 Song format options
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-24
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

class FontFormat(object):
	def __init__():
		self.face = "Arial"
		self.size = 12
		self.bold = False
		self.italic = False
		self.underline = False
		
	def GetWxFont():
		pass
	
class ParagraphFormat(FontFormat):
	def __init__():
		FontFormat.__init__()
		self.leftMargin = 0
		self.topMargin = 12
		self.bottomMargin = 0

class SongFormat(ParagraphFormat):
	def __init__():
		self.verse = []
		self.chorus = ParagraphFormat()
		self.chord = FontFormat()
		self.comment = FontFormat()
		self.title = ParagraphFormat()
	def StubSetVerseCount(n):
		i = len(a)
		while i < n:
			verse.append(ParagraphFormat())
			i = i + 1	
