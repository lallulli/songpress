###############################################################
# Name:			 Renderer.py
# Purpose:	 Render a song on a self.dc
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

class Renderer(object):
	def __init__(self, sf, sd = SongDecorator()):
		object.__init__(self)
		self.text = ""
		self.sd = sd
		self.dc = None
		# SongFormat
		self.sf = sf
		# states
		self.none = 0
		self.verse = 1
		self.chorus = 2
		self.state = self.none
		# current self.x position (for verse)
		self.x = 0
		# current self.y position
		self.y = 0
		# left margin in current paragraph
		self.xMargin = 0
		# current self.x position for chord
		self.xChord = 0
		# max self.x value in current paragraph
		self.xMax = 0
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

	def BeginVerse(self):
		if self.state == self.none:
			self.state = self.verse
			self.verseNumber += 1
			print("self.verse %d" % (self.verseNumber,))
			self.sf.StubSetVerseCount(self.verseNumber)
			self.format = self.sf.verse[self.verseNumber-1]
			self.x = self.format.leftMargin
			(w, h) = self.sd.BeginVerse(self.x, self.y)
			self.x = self.x + w
			self.y = self.y + h
			self.xMargin = self.x
			self.textFont = self.format.GetWxFont()
			self.chordFont = self.format.chord.GetWxFont()	
			self.commentFont = self.format.comment.GetWxFont()	

	def EndVerse(self):
		self.state = self.none
		self.y = self.sd.EndVerse(self.xMax, self.y)
		self.dc.SetFont(self.textFont)
		(w, h) = self.dc.GetTextExtent("Dummy")
		self.y = self.sd.EndChorus(self.xMax, self.y) + self.format.vskip * h 
		
	def BeginChorus(self):
		self.EndLine()
		self.state = self.chorus
		self.format = self.sf.chorus
		self.x = self.format.leftMargin
		(w, h) = self.sd.BeginChorus(self.x, self.y)
		self.x = self.x + w
		self.y = self.y + h
		self.xMargin = self.x
		self.textFont = self.format.GetWxFont()
		self.chordFont = self.format.chord.GetWxFont()	
		self.commentFont = self.format.comment.GetWxFont()	
		
	def EndChorus(self):
		print("Ending chorus")
		self.EndLine()
		self.state = self.none
		self.dc.SetFont(self.textFont)
		(w, h) = self.dc.GetTextExtent("Dummy")
		self.y = self.sd.EndChorus(self.xMax, self.y) + self.format.vskip * h
		
	def ChorusVSkip(self):
		self.dc.SetFont(self.textFont)
		(w, h) = self.dc.GetTextExtent("Dummy")
		self.y += self.format.vskip * h 
		
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
		self.EndLine()
		self.dc.SetFont(self.sf.title.GetWxFont())
		self.dc.DrawText(title, 0, self.y)
		(w, h) = self.dc.GetTextExtent(title)
		self.y += 2*h
		
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
		
	def EndCurrent(self):
		if self.state == self.verse:
			self.EndVerse()
		elif self.state == self.chorus:
			self.EndChorus()
	
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
	
	def Render(self, text, dc):
		self.text = text
		self.dc = dc
		self.y = 0
		self.verseNumber = 0
		self.state = self.none
		self.format = self.sf
		self.inLine = False
				
		for l in self.text.splitlines():
			self.tkz = SongTokenizer(l)
			empty = True
			for tok in self.tkz:
				empty = False
				t = tok.token
				if t == SongTokenizer.normalToken:
					self.AddText(tok.content)
				elif t == SongTokenizer.chordToken:
					self.AddChord(tok.content[1:])
				elif t == SongTokenizer.commandToken:
					cmd = tok.content
					if cmd == 'soc':
						self.EndCurrent()
						self.BeginChorus()
					elif cmd == 'eoc' and self.state == self.chorus:
						self.EndChorus()
					elif cmd == 'c' or cmd == 'comment':
						a = self.GetAttribute()
						if a != None:
							self.AddText(a, True)
					elif cmd == 't' or cmd == 'title':
						a = self.GetAttribute()
						if a != None:
							self.EndCurrent()
							self.AddTitle(a)
							
			self.EndLine()
			if empty:
				if self.state == self.verse:
					self.EndVerse()
					self.state = self.none
				elif self.state == self.chorus:
					self.ChorusVSkip()
		self.dc = None
		
		