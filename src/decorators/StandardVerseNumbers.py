###############################################################
# Name:			 StandardVerseNumbers.py
# Purpose:	 Decorator that adds verse numbering
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-03-14
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

from SongDecorator import *
from SongFormat import *
import i18n
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
		config = wx.Config.Get()
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

	def InitDraw(self):
		self.dc.SetFont(self.format.wxFont)
		self.baseWidth, self.baseHeight = self.dc.GetTextExtent("0")
		self.verseWidth, self.verseHeight = self.dc.GetTextExtent(str(self.s.labelCount))
		self.verseTotalWidth = self.baseWidth * (
				self.format.leftMargin + self.format.leftPadding + self.format.rightMargin + self.format.rightPadding
			) + self.verseWidth
		self.dc.SetFont(self.format.chorus.wxFont)
		#self.chorusWidth, self.chorusHeight = self.dc.GetTextExtent(self.format.chorus.label)
		#self.chorusTotalWidth = self.baseWidth * (
		#		self.format.leftMargin + self.format.leftPadding + self.format.rightMargin + self.format.rightPadding
		#	) + self.chorusWidth
		
	def SetMarginBlock(self, block):
		if block.type == block.verse:
			font = self.format.wxFont
			self.dc.SetFont(font)
			if block.label is not None:
				text = block.label
				if text == '':
					w = self.verseWidth
					h = self.verseHeight
				else:
					w, h = self.dc.GetTextExtent(text)
				w += self.baseWidth * (
					self.format.leftMargin + self.format.leftPadding + self.format.rightMargin + self.format.rightPadding
				)
			else:
				w = self.verseTotalWidth
		elif block.type == block.title:
			w = 0
		else:
			if block.label is not None:
				text = block.label
			else:
				text = self.format.chorus.label
			font = self.format.chorus.wxFont
			self.dc.SetFont(font)
			w, h = self.dc.GetTextExtent(text)
			w += self.baseWidth * (
				self.format.leftMargin + self.format.leftPadding + self.format.rightMargin + self.format.rightPadding
			)
		block.SetMargin(0, 0, 0, w)

	def PreDrawBlock(self, block, bx, by):
		if block.type != block.title and len(block.boxes) > 0:
			if block.type == block.verse:
				font = self.format.wxFont
				self.dc.SetFont(font)
				background = self.wxGrey
				foreground = self.wxBlack
				if block.label is not None:
					text = block.label
					if text == '':
						w = self.verseWidth
						h = self.verseHeight
					else:
						w, h = self.dc.GetTextExtent(text)
				else:
					text = str(block.verseLabelNumber)
					w = self.verseWidth
					h = self.verseHeight
					
			else:
				background = self.wxBlack
				foreground = self.wxWhite
				if block.label is not None:
					text = block.label
				else:
					text = self.format.chorus.label
				font = self.format.chorus.wxFont
				self.dc.SetFont(font)
				w, h = self.dc.GetTextExtent(text)
			if text != '':
				realW, realH = self.dc.GetTextExtent(text)
				# rx, ry: top-left corner of rectangle
				# tx, ty: top-left corner of text
				rx = bx + self.format.leftMargin * self.baseWidth
				tx = (rx
					+ self.baseWidth * self.format.leftPadding
					+ 0.5 * (w - realW))
				ty = by + block.boxes[0].textBaseline + block.marginTop - h
				ry = ty - self.format.topPadding * self.baseHeight
				brush = wx.Brush(background, wx.SOLID)
				self.dc.SetBrush(brush)
				self.dc.DrawRectangle(rx, ry,
					w + self.baseWidth * (self.format.leftPadding + self.format.rightPadding),
					h + self.baseHeight * (self.format.topPadding + self.format.bottomPadding))
				brush = wx.Brush(foreground, wx.SOLID)
				self.dc.SetBrush(brush)
				self.dc.SetTextForeground(foreground)
				self.dc.SetBackgroundMode(wx.TRANSPARENT)
				self.dc.DrawText(text, tx, ty)
				self.dc.SetTextForeground(self.wxBlack)
