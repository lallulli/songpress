###############################################################
# Name:             HTML.py
# Purpose:     Export song to HTML
# Author:         Luca Allulli (webmaster@roma21.it)
# Created:     2010-05-05
# Update:        2026-02-22
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:     GNU GPL v2
##############################################################

from .Renderer import *

class HtmlExporter(object):
    def __init__(self, sf):
        object.__init__(self)
        self.sf = sf
        self.out = ""

    def Draw(self, song, dc):
        classes = {
            SongBlock.title: 'titleblock',
            SongBlock.chorus: 'chorus',
            SongBlock.verse: 'verse',
        }

        template = """<!DOCTYPE html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>%(title)s</title>
    <style>
        body {
            font-family: "%(face)s";
        }
        div.chorus, div.verse, div.titleblock {
            margin-bottom: 1.5em;
        }
        div.chorus {
            font-weight: bold;
        }
        .title {
            font-weight: bold;
            text-decoration: underline;
        }
        .subtitle {
            font-weight: normal;
            font-style: italic;
            font-size: 0.95em;
        }
        .line {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            align-items: flex-end;
            line-height: 1.4;
        }
        .pair {
            display: inline-flex;
            flex-direction: column;
            align-items: flex-start;
        }
        .chord {
            font-style: italic;
            font-size: small;
            font-weight: normal;
            white-space: pre;
            min-height: 1em;
        }
        .text {
            white-space: pre;
        }
    </style>
</head>
<body>
    %(body)s
</body>
</html>"""

        out = ""
        title = "Songpress"

        for block in song.boxes:
            b = '<div class="%s">' % classes[block.type]

            for line in block.boxes:
                pairs = []
                current_pair = [None, ""]

                for t in line.boxes:
                    if t.type == SongText.title:
                        current_pair[1] += '<span class="title">%s</span>' % t.text
                        if block.type == SongBlock.title:
                            title = t.text
                    elif t.type == SongText.subtitle:
                        current_pair[1] += '<span class="subtitle">%s</span>' % t.text
                    elif t.type == SongText.chord:
                        pairs.append(current_pair)
                        current_pair = [t.text, ""]
                    else:
                        current_pair[1] += t.text
                        if block.type == SongBlock.title:
                            title = t.text

                pairs.append(current_pair)

                line_html = '<div class="line">'
                for chord, text in pairs:
                    chord_html = chord if chord is not None else ""
                    line_html += (
                        '<div class="pair">'
                        '<span class="chord">%s</span>'
                        '<span class="text">%s</span>'
                        '</div>'
                    ) % (chord_html or "&#8203;", text or "&#8203;")
                line_html += "</div>"
                b += line_html

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


class TabExporter(object):
    def __init__(self, sf):
        object.__init__(self)
        self.sf = sf
        self.out = ""

    def Draw(self, song, dc):
        # dc is a dummy parameter
        out = []
        for block in song.boxes:
            for line in block.boxes:
                tc = ""
                tt = ""
                spaces = 0
                for t in line.boxes:
                    if t.type == SongText.chord:
                        if spaces >= 0:
                            tc += " " * spaces
                        else:
                            tt += " " * -spaces
                        tc += t.text
                        spaces = -len(t.text)
                    else:
                        tt += t.text
                        spaces += len(t.text)
                if tc != "":
                    out.append(tc)
                out.append(tt)
            out.append("\n")
        self.out = "\n".join(out).strip()
        return 0, 0

    def getTab(self):
        return self.out
