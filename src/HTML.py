###############################################################
# Name:			 HTML.py
# Purpose:	 Export song to HTML
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2010-05-05
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

from Renderer import *

class HtmlExporter(object):
	def __init__(self, sf):
		object.__init__(self)
		self.sf = sf
		self.out = ""

	def Draw(self, song, dc):
		# dc is a dummy parameter
		classes = {
			SongBlock.title: 'title',
			SongBlock.chorus: 'chorus',
			SongBlock.verse: 'verse',
		}
		for block in song.boxes:
			b = "<div class=\"%s\">" % (classes[block.type])
			for line in block.boxes:
				tc = "<td>"
				tt = "<td>"
				new_line = True
				for t in line.boxes:
					if t.type == SongText.chord:
						if not new_line:
							tc += "</td><td>"
							tt += "</td><td>"
						tc += t.text
					else:
						tt += t.text
					new_line = False
				tc += "</td>"
				tt += "</td>"
				b += "<table>\n<tr class=\"chord\">%s</tr>\n<tr>%s</tr>\n</table>\n" % (tc, tt)
			b += "</div>"
			self.out += b
		return 0, 0

	def getHtml(self):
		return self.out
