###############################################################
# Name:			 HTML.py
# Purpose:	  Export song to HTML, without table-based layout
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2010-05-05
# Update:    2025-11-20
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################


from Renderer import *
import json

template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>%(title)s</title>

<style>
body {
    font-family: "%(face)s";
    white-space: nowrap;
}

/* Contenitore di ogni riga */
.line {
    position: relative;
    height: 1.4em;
    margin-bottom: 0.8em;
}

/* Token assoluti */
.token {
    position: absolute;
    white-space: pre;
}

/* Accord text */
.chord {
    font-style: italic;
    font-size: 0.9em;
    top: -1.2em;        /* posizione sopra il testo */
}

/* Testo normale */
.text {
    font-size: 1em;
}

.titleblock .text {
    font-weight: bold;
    text-decoration: underline;
}

.subtitle {
    font-style: italic;
}
</style>

</head>
<body>
%(body)s
</body>
</html>
"""

class HtmlExporter:
    def __init__(self, sf):
        self.sf = sf
        self.out = ""

    def Draw(self, song, dc):

        classes = {
            SongBlock.title: 'titleblock',
            SongBlock.chorus: 'chorus',
            SongBlock.verse: 'verse',
        }

        body = ""
        title = "Songpress"

        # --- Process blocks ---
        for block in song.boxes:
            block_html = f'<div class="{classes[block.type]}">'

            for line in block.boxes:

                # Start row
                html_line = '<div class="line">'

                x = 0  # cursor in pixels

                for t in line.boxes:

                    # Measure text width using dc
                    w, h = dc.GetTextExtent(t.text)

                    if t.type == SongText.chord:
                        token_html = f'<span class="token chord" style="left: {x}px">{t.text}</span>'
                    else:
                        if t.type == SongText.title:
                            title = t.text
                            token_html = f'<span class="token text title" style="left: {x}px">{t.text}</span>'
                        elif t.type == SongText.subtitle:
                            token_html = f'<span class="token text subtitle" style="left: {x}px">{t.text}</span>'
                        else:
                            token_html = f'<span class="token text" style="left: {x}px">{t.text}</span>'

                    html_line += token_html

                    # Advance cursor
                    x += w

                html_line += '</div>'
                block_html += html_line

            block_html += '</div>'
            body += block_html

        self.out = template % {
            "title": title,
            "face": self.sf.face,
            "body": body
        }

        return 0, 0

    def getHtml(self):
        return self.out


