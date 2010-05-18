###############################################################
# Name:			 HTML.py
# Purpose:	 Export song to HTML
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2010-05-05
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

from Renderer import *

template = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<head>
		<title>%(title)s</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<style type="text/css">
			<!--
				div.chorus,div.verse,div.title {
					margin-bottom: 1.5em;
					font-family: "%(face)s";
				}
				div.chorus table,div.verse table, div.title table {
					margin: 0px;
					padding: 0px;
					border: 0px;
					border-collapse: collapse;
				}
				.chorus {
					font-weight: bold;
				}
				.chord {
					font-style: italic;
					font-size: small;
					font-weight: normal;
				}
				.title {
					font-weight: bold;
					text-decoration: underline;
				}
			-->
		</style>
	</head>
	<body>
		%(body)s
	</body>
</html>
"""

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
		out = ""
		title = "Songpress"
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
						tc += t.text.replace(" ", "&nbsp;")
					else:
						tt += t.text.replace(" ", "&nbsp;")
						if block.type == SongBlock.title:
							title = t.text
					new_line = False
				tc += "</td>"
				tt += "</td>"
				b += "<table cellpadding=\"0\">\n<tr class=\"chord\">%s</tr>\n<tr>%s</tr>\n</table>\n" % (tc, tt)
			b += "</div>"
			out += b
		self.out = template % {
				'title': title,
				'body': out,
				'face': self.sf.face,
			}
		return 0, 0

	def getHtml(self):
		return self.out
