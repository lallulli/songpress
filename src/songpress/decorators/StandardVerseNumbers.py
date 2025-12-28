###############################################################
# Name:             StandardVerseNumbers.py
# Purpose:     Decorator that adds verse numbering
# Author:         Luca Allulli (webmaster@roma21.it)
# Created:     2009-03-14
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:     GNU GPL v2
##############################################################

from songpress.SongDecorator import *
from songpress.SongFormat import *
import wx

class Format(FontFormat):
    def __init__(self, sf, chorusLabel):
        FontFormat.__init__(self)
        self.face = sf.face
        self.size = sf.size
        self.bold = sf.bold
        self.italic = sf.italic
        self.underline = sf.underline
        self.leftMargin = 0.5
        self.rightMargin = 0.5
        self.leftPadding = 0.25
        self.rightPadding = 0.25
        self.topPadding = 0.1
        self.bottomPadding = 0.1
        self.chorus = FontFormat()
        self.chorus.face = sf.chorus.face
        self.chorus.size = sf.chorus.size
        self.chorus.bold = sf.chorus.bold
        self.chorus.italic = sf.chorus.italic
        self.chorus.underline = sf.chorus.underline
        self.chorus.label = chorusLabel

    def SetChorusLabel(self, label):
        self.chorus.label = label

    def GetChorusLabel(self):
        return self.chorus.label


class Decorator(SongDecorator):
    def __init__(self, format):
        SongDecorator.__init__(self)
        self.format = format

    wxBlack = wx.Colour(0, 0, 0)
    wxWhite = wx.Colour(255, 255, 255)
    wxGrey = wx.Colour(200, 200, 200)

    def SetMarginBlock(self, block):
        font = block.format.wxFont
        self.dc.SetFont(font)
        baseWidth, baseHeight = self.dc.GetTextExtent("0")
        if block.type == block.verse:
            text = block.label if block.label is not None else ''
            text_spacer = text if text != '' else str(self.s.labelCount)
            w, h = self.dc.GetTextExtent(text_spacer)

            w += baseWidth * (
                self.format.leftMargin + self.format.leftPadding + self.format.rightMargin + self.format.rightPadding
            )
        elif block.type == block.title:
            w = 0
        else:
            if block.label is not None:
                text = block.label
            else:
                text = self.format.chorus.label
            w, h = self.dc.GetTextExtent(text)
            w += baseWidth * (
                self.format.leftMargin + self.format.leftPadding + self.format.rightMargin + self.format.rightPadding
            )
        block.SetMargin(0, 0, 0, w)

    def PreDrawBlock(self, block, bx, by):
        if block.type != block.title and len(block.boxes) > 0:
            font = block.format.wxFont
            self.dc.SetFont(font)
            baseWidth, baseHeight = self.dc.GetTextExtent("0")
            if block.type == block.verse:
                background = self.wxGrey
                foreground = self.wxBlack
                if block.label is not None:
                    text = block.label
                    text_spacer = text
                    if text == '':
                        text_spacer = str(self.s.labelCount)
                else:
                    text = str(block.verseLabelNumber)
                    text_spacer = str(self.s.labelCount)
                w, h = self.dc.GetTextExtent(text_spacer)

            else:
                background = self.wxBlack
                foreground = self.wxWhite
                if block.label is not None:
                    text = block.label
                else:
                    text = self.format.chorus.label
                w, h = self.dc.GetTextExtent(text)
            if text != '':
                realW, realH = self.dc.GetTextExtent(text)
                rx = bx + self.format.leftMargin * baseWidth
                tx = (rx
                    + baseWidth * self.format.leftPadding
                    + 0.5 * (w - realW))
                ty = by + block.boxes[0].textBaseline + block.marginTop - h
                ry = ty - self.format.topPadding * baseHeight
                brush = wx.Brush(background, wx.SOLID)
                self.dc.SetBrush(brush)
                self.dc.DrawRectangle(int(rx), int(ry),
                    int(w + baseWidth * (self.format.leftPadding + self.format.rightPadding)),
                    int(h + baseHeight * (self.format.topPadding + self.format.bottomPadding)))
                brush = wx.Brush(foreground, wx.SOLID)
                self.dc.SetBrush(brush)
                self.dc.SetTextForeground(foreground)
                self.dc.SetBackgroundMode(wx.TRANSPARENT)
                self.dc.DrawText(text, int(tx), int(ty))
                self.dc.SetTextForeground(self.wxBlack)
