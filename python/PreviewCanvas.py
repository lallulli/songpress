###############################################################
# Name:			 PreviewCanvas.py
# Purpose:	 Window containing preview
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-21
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

import wx
from wx import xrc
from VerseChorusHandler import *
from SongTokenizer import *
from SongFormat import *

class TextPortion(object):
	def __init__(text, font, x):
		self.text = text
		self.font = font
		self.x = x

class PreviewCanvas(object):
	"""Abstract class. Override methods New, Open, Save"""
	###UI generation###

	def __init__(self, parent, sf, vh = VerseHandler(), ch = ChorusHandler()):
		self.frame = wx.Frame(parent, -1, "Preview")
		self.frame.Bind(wx.EVT_PAINT, self.OnPaint, self.frame)
		self.frame.SetBackgroundColour(wx.WHITE)
		self.text = ""
		self.frame.Show()
		self.vh = vh
		self.ch = ch
		#SongFormat
		self.sf = sf
		
	def OnPaint(self, e):
	
		def BeginParagraph():
			pass
			
		def EndParagraph():
			pass
	
		def BeginVerse():
			verseNumber = verseNumber + 1
			verseFormat = sf.verse[verseNumber]
			x = verseFormat.leftMargin
			(w, h) = vh.Begin(x, y)
			x = x + w
			y = y + h
			xMargin = x
			textFont = verseFormat.GetWxFont()

		def EndVerse():
			y = vh.End(xMax, y)
			
		def BeginChorus():
			pass
			
		def EndChorus():
			pass
			
		def ChorusVSkip():
			pass
			
		def AddText(text):
			if not appendToLastText:
				lineText.append(TextPortion(text, textFont, x))
				appendToLastText = True
			else:
				lineText[-1].text += text
			dc.SetFont(textFont)
			(w, h) = dc.GetTextExtent(lineText[-1].text)
			x = lineText[-1].x + w
			textHeight = max(textHeight, h)
			appendToLastText = True
		
		def AddChord(chord):
			if xChord > x:
				appendToLastText = False
				x = xChord
			lineChord.append(TextPortion(chord, chordFont, xChord))
			dc.SetFont(chordFont)
			(w, h) = dc.GetTextExtent(chord)
			xChord += w
			chordHeight = max(chordHeight, h)
			
		def AddTitle(title):
			pass
			
		def EndLine():
			# xMax = ..
			# reset lists, append..., etc.
			# draw!
			pass
			
		def EndCurrent():
			if state == verse:
				EndVerse()
			elif state == chorus:
				EndChorus()
		
		def GetArgument():
			tok = tkz.next()
			if tok.token == SongTokenizer.attrToken:
				return tok.content
			tkz.Repeat()
			return None
	
		dc = wx.PaintDC(self.frame)
		# current x position (for verse)
		x = 0
		# current y position
		y = 0
		# left margin in current paragraph
		xMargin = 0
		# current x position for chord
		xChord = 0
		# max x value in current paragraph
		xMax = 0
		appendToLastText = False
		verseNumber = 0
		verseFormat = sf
		lineText = []
		lineChords = []
		textHeight = 0
		widthHeight = 0
		textFont = None
		
		#states
		none = 0
		verse = 1
		chorus = 2
		
		for l in self.text.splitlines():
			tkz = SongTokenizer(l)
			empty = True
			for tok in tkz:
				empty = False
				t = tok.token
				if t == SongTokenizer.normalToken:
					if state == none:
						BeginVerse()
					AddText(tok.content)
				elif t == SongTokenizer.chordToken:
					AddChord(tok.content[1:])
				elif t == SongTokenizer.commandToken:
					cmd = tok.content
					if cmd == 'soc':
						EndCurrent()
						BeginChorus()
					elif cmd == 'eoc' and state == chorus:
						EndChorus()
					elif cmd == 'c' or cmd == 'comment':
						a = GetArgument()
						if a != None:
							AddComment(a)
					elif cmd == 't' or cmd == 'title':
						a = GetArgument()
						if a != None:
							EndCurrent()
							AddTitle(a)			
					
			if !empty:
				EndLine()
			else:
				if state == verse:
					EndVerse()
					state = none
				elif state == chorus:
					ChorusVSkip()
		
	def Refresh(self, text):
		self.text = text
		self.frame.Refresh()
