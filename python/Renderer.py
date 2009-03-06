###############################################################
# Name:			 Renderer.py
# Purpose:	 Render a song on a dc
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-21
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

import wx
from SongDecorator import *
from SongTokenizer import *
from SongFormat import *

class TextPortion(object):
	def __init__(self, text, font, x):
		object.__init__(self)
		self.text = text
		self.font = font
		self.x = x
		
class SongBlock(object):
	
	# types
	verse = 1
	chorus = 2
	title = 3
	
	def __init__(self, type, format, dc):
	
		def GetFontHeight(font):
			dc.SetFont(font)
			return dc.GetTextExtent('Dummy')[1]
			
		object.__init__(self)
		self.height = 0
		self.width = 0
		self.textLines = []
		self.yText = []
		self.chordLines = []
		self.yChord = []
		self.type = type
		self.format = format
		self.textHeight = GetFontHeight(self.format.wxFont)
		self.chordHeight = GetFontHeight(self.format.chord.wxFont)
		
	def AddLine(self, text, chords, width):
		self.yChord.append(width)
		self.chordLines.append(chords)
		if(len(chords) > 0):
			self.height += self.chordHeight * self.format.chordSpacing
		self.yText.append(self.height)
		self.textLines.append(text)
		self.height += self.textHeight * self.format.textSpacing
		self.yText.append(self.height)
		self.UpdateWidth(width + self.format.leftMargin)
			
	def UpdateWidth(self, width):
		if width > self.width:
			self.width = width	


class Renderer(object):
	
	def __init__(self, sf, sd = SongDecorator()):
		object.__init__(self)
		self.text = ""
		self.sd = sd
		self.dc = None
		# SongFormat
		self.sf = sf
		# current self.x position (within line)
		self.x = 0
		# current self.x position for chord
		self.xChord = 0
		# overall song width and height (excluding decorations)
		self.width = 0
		self.height = 0
		self.appendToLastText = False
		self.verseNumber = 0
		self.lineText = []
		self.lineChords = []
		self.textHeight = 0
		self.chordHeight = 0
		self.textFont = None
		self.chordFont = None
		self.commentFont = None
		self.format = None
		self.inLine = False
		self.currentBlock = None
		self.blocks = []

	def BeginBlock(self, type):
		self.EndBlock()
		self.currentBlock = SongBlock(type, self.format, self.dc)
		self.textFont = self.format.wxFont
		self.chordFont = self.format.chord.wxFont	
		self.commentFont = self.format.comment.wxFont
	
	def EndBlock(self):
		if self.currentBlock != None:
			self.EndLine()
			if(self.currentBlock.width > self.width):
				self.width = self.currentBlock.width
			if(self.currentBlock.height > self.height):
				self.height = self.currentBlock.height				
			self.blocks.append(self.currentBlock)
			currentBlock = None

	def BeginVerse(self):
		if self.currentBlock == None:
			self.verseNumber += 1
			print("self.verse %d" % (self.verseNumber,))
			self.sf.StubSetVerseCount(self.verseNumber)
			self.format = self.sf.verse[self.verseNumber-1]
			self.BeginBlock(SongBlock.verse)

	def BeginChorus(self):
		self.format = self.sf.chorus
		self.BeginBlock(SongBlock.chorus)
		
	def ChorusVSkip(self):
		self.EndLine()
		self.BeginLine()
		self.EndLine()
		
	def AddText(self, text, comment = False):
		self.BeginVerse()
		self.BeginLine()
		if comment:
			text = "(" + text + ")"
		if (not self.appendToLastText) or comment:
			print("Appending at " + str(self.x))
			if not comment:
				self.lineText.append(TextPortion(text, self.textFont, self.x))
				self.appendToLastText = True
			else:
				self.lineText.append(TextPortion(text, self.commentFont, self.x))
				self.appendToLastText = False
		else:
			self.lineText[-1].text += text
		self.dc.SetFont(self.textFont)
		(w, h) = self.dc.GetTextExtent(self.lineText[-1].text)
		self.x = self.lineText[-1].x + w
		self.textHeight = max(self.textHeight, h)
	
	def AddChord(self, chord):
		self.BeginVerse()
		self.BeginLine()
		if self.xChord > self.x:
			self.appendToLastText = False
			self.x = self.xChord
			print("Ora vale "+str(self.x))
		else:
			self.xChord = self.x
		self.lineChords.append(TextPortion(chord, self.chordFont, self.xChord))
		self.dc.SetFont(self.chordFont)
		(w, h) = self.dc.GetTextExtent(chord)
		self.xChord += w
		self.chordHeight = max(self.chordHeight, h)
		
	def AddTitle(self, title):
		self.format = self.sf.title
		self.BeginBlock(SongBlock.title)	
		self.AddText(title)
		self.EndBlock()
		
	def BeginLine(self):
		if not self.inLine:
			self.inLine = True
			self.lineText = []
			self.lineChords = []
			self.textHeight = 0
			self.chordHeight = 0
			self.x = 0
			self.xChord = 0
			self.appendToLastText = False	
			
	def EndLine(self):
		if self.inLine:
			self.currentBlock.AddLine(self.lineText, self.lineChords, max(self.xChord, self.x))
		old = """
		if self.inLine:
			self.inLine = False
			# Draw chords
			if len(self.lineChords) > 0:
				self.dc.SetFont(self.chordFont)
				for c in self.lineChords:
					self.dc.DrawText(c.text, c.x, self.y)
				self.y += self.chordHeight * self.format.chordSpacing
			# Draw text
			for t in self.lineText:
				self.dc.SetFont(t.font)
				self.dc.DrawText(t.text, t.x, self.y)
			self.y += self.textHeight * self.format.textSpacing
			self.xMax = max(self.xMax, self.xChord, self.x)
		"""
		
	def GetAttribute(self):
		print("Getting attribute...")
		try:
			tok = self.tkz.next()
			if tok.token != SongTokenizer.colonToken:
				self.tkz.Repeat()
				return None
			tok = self.tkz.next()
			if tok.token != SongTokenizer.attrToken:
				self.tkz.Repeat()
				return None
			return tok.content
		except StopIteration:
			print("No attribute")
			pass
		return None
		
	def GetState(self):
		return None if self.currentBlock == None else self.currentBlock.type
	
	def Render(self, text, dc):
		self.text = text
		self.dc = dc
		self.width = 0
		self.verseNumber = 0
		self.format = self.sf
		self.inLine = False
		self.currentBlock = None
		
		for l in self.text.splitlines():
			state = self.GetState()
			self.tkz = SongTokenizer(l)
			empty = True
			for tok in self.tkz:
				state = self.GetState()
				empty = False
				t = tok.token
				if t == SongTokenizer.normalToken:
					self.AddText(tok.content)
				elif t == SongTokenizer.chordToken:
					self.AddChord(tok.content[1:])
				elif t == SongTokenizer.commandToken:
					cmd = tok.content
					if cmd == 'soc':
						self.BeginChorus()
					elif cmd == 'eoc' and state == SongBlock.chorus:
						self.EndBlock()
					elif cmd == 'c' or cmd == 'comment':
						a = self.GetAttribute()
						if a != None:
							self.AddText(a, True)
					elif cmd == 't' or cmd == 'title':
						a = self.GetAttribute()
						if a != None:
							self.AddTitle(a)
							
			self.EndLine()
			if empty:
				if state == SongBlock.verse:
					self.EndBlock()
				elif state == SongBlock.chorus:
					self.ChorusVSkip()
		self.dc = None
		
		