###############################################################
# Name:			 Renderer.py
# Purpose:	 Render a song on a dc
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-21
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

import wx
from SongDecorator import *
from SongTokenizer import *
from SongFormat import *
from SongBoxes import *
from Transpose import translateChord, autodetectNotation
from EditDistance import minEditDist


class BreakException(Exception):
	pass


class Renderer(object):
	def __init__(self, sf, sd=SongDecorator(), notations=[]):
		object.__init__(self)
		self.text = ""
		self.sd = sd
		self.dc = None
		# SongFormat
		self.starting_sf = sf
		self.sf = sf
		self.format = None
		self.currentBlock = None
		self.currentLine = None
		self.song = None
		self.notation = None
		self.notations = notations
		self.chordPatterns = []

	def BeginBlock(self, type, label=None):
		self.EndBlock()
		if type == SongBlock.verse:
			self.song.verseCount += 1
			if label is None:
				self.song.labelCount += 1
			self.sf.AddVerse()
			self.format = self.sf.verse[-1]
		elif type == SongBlock.chorus:
			self.format = self.sf.chorus
			self.song.chorusCount += 1
		else:
			self.format = self.sf.title
		self.currentBlock = SongBlock(type, self.format)
		self.currentBlock.label = label
		self.currentBlock.verseNumber = self.song.verseCount
		self.currentBlock.verseLabelNumber = self.song.labelCount

	def EndBlock(self):
		if self.currentBlock is not None:
			self.EndLine()
			if self.sf.showChords == 1:
				current = self.currentBlock.chords
				found = False
				for p in self.chordPatterns:
					led = len(p)
					med = minEditDist(p, current)
					if med < led and med < 4:
						found = True
						break
				if not found:
					self.chordPatterns.append(current)
				else:
					self.currentBlock.RemoveChordBoxes()
			self.song.AddBox(self.currentBlock)
			self.currentBlock = None

	def BeginVerse(self, label=None):
		if self.currentBlock == None:
			self.BeginBlock(SongBlock.verse, label)
			self.label = label

	def BeginChorus(self, label=None):
		self.BeginBlock(SongBlock.chorus, label)

	def ChorusVSkip(self):
		self.EndLine()
		self.BeginLine()
		self.EndLine()

	def AddText(self, text, type=SongText.text):
		if(
			text.strip() != ''
			and type != SongText.title
			and type != SongText.subtitle
			and type != SongText.comment
			and self.currentBlock is not None
			and self.currentBlock.type == SongBlock.title
		):
			self.EndBlock()
		self.BeginVerse()
		self.BeginLine()
		if type == SongText.comment:
			text = "(" + text + ")"
			format = self.format.comment
		elif type == SongText.chord:
			format = self.format.chord
			if self.sf.showChords == 1:
				self.currentBlock.chords.append(translateChord(text, self.notation, self.notation))
		else:
			format = self.format
		t = SongText(text, format.wxFont, type, format.color)
		if not type == SongText.chord or self.sf.showChords > 0:
			self.currentLine.AddBox(t)

	def AddTitle(self, title):
		if self.currentBlock is None or self.currentBlock.type != SongBlock.title:
			self.BeginBlock(SongBlock.title)
		self.format = self.sf.title
		self.AddText(title, SongText.title)

	def AddSubTitle(self, title):
		if self.currentBlock is None or self.currentBlock.type != SongBlock.title:
			self.BeginBlock(SongBlock.title)
		self.format = self.sf.subtitle
		self.AddText(title, SongText.subtitle)

	def BeginLine(self):
		if self.currentLine == None:
			if self.song.drawWholeSong or (self.fromLine <= self.lineCount and self.lineCount <= self.toLine):
				self.currentBlock.drawBlock = True
			self.currentLine = SongLine()

	def EndLine(self):
		if self.currentLine is not None:
			self.currentBlock.AddBox(self.currentLine)
			self.currentLine = None

	def GetAttribute(self):
		#print("Getting attribute...")
		try:
			tok = self.tkz.next()
			if tok.token != SongTokenizer.colonToken:
				self.tkz.Repeat()
				return None
			tok = self.tkz.next()
			if tok.token != SongTokenizer.attrToken:
				self.tkz.Repeat()
				return ''
			return tok.content
		except StopIteration:
			#print("No attribute")
			pass
		return None

	def GetState(self):
		return None if self.currentBlock == None else self.currentBlock.type

	def Render(self, text, dc, fromLine = -1, toLine = -1):
		#print "Face is " + self.sf.face
		self.text = text
		self.dc = dc
		self.verseNumber = 0
		self.format = self.sf
		self.currentLine = None
		self.currentBlock = None
		self.song = SongSong(self.sf)
		self.song.drawWholeSong = fromLine == -1
		self.lineCount = -1
		self.fromLine = fromLine
		self.toLine = toLine
		self.sf = SongFormat(self.starting_sf)
		if self.sf.showChords == 1:
			self.notation = autodetectNotation(text, self.notations)
			self.chordPatterns = []

		for l in self.text.splitlines():
			self.lineCount += 1
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
					self.AddText(tok.content[1:], SongText.chord)
				elif t == SongTokenizer.commandToken:
					cmd = tok.content.lower()
					if cmd == 'soc' or cmd == 'start_of_chorus':
						a = self.GetAttribute()
						self.BeginChorus(a)
					elif (cmd == 'eoc' or cmd == 'end_of_chorus') and state == SongBlock.chorus:
						self.EndBlock()
					elif cmd == 'c' or cmd == 'comment':
						a = self.GetAttribute()
						if a is not None:
							self.AddText(a, SongText.comment)
					elif cmd == 't' or cmd == 'title':
						a = self.GetAttribute()
						if a is not None:
							self.AddTitle(a)
					elif cmd == 'st' or cmd == 'subtitle':
						a = self.GetAttribute()
						if a is not None:
							self.AddSubTitle(a)
					elif cmd == 'verse':
						self.BeginVerse(self.GetAttribute())
					elif cmd == 'textsize':
						try:
							try:
								size = int(self.GetAttribute())
							except TypeError:
								raise BreakException()
							except ValueError:
								raise BreakException()
							self.format = ParagraphFormat(self.format)
							self.format.size = size
							self.sf.size = size
							self.sf.chorus.size = size
							self.sf.title.size = size
							self.sf.subtitle.size = size
						except BreakException:
							pass
					elif cmd == 'textfont':
						try:
							face = self.GetAttribute()
							if face is None:
								raise BreakException
							self.format = ParagraphFormat(self.format)
							self.format.face = face
							self.sf.face = face
							self.sf.chorus.face = face
							self.sf.title.face = face
							self.sf.subtitle.face = face
						except BreakException:
							pass
					elif cmd == 'textcolour':
						try:
							color = self.GetAttribute()
							if color is None:
								raise BreakException
							self.format = ParagraphFormat(self.format)
							self.format.color = color
							self.sf.color = color
							self.sf.chorus.color = color
							self.sf.title.color = color
							self.sf.subtitle.color = color
						except BreakException:
							pass
					elif cmd == 'chordsize':
						try:
							try:
								size = int(self.GetAttribute())
							except TypeError:
								raise BreakException()
							except ValueError:
								raise BreakException()
							self.format = ParagraphFormat(self.format)
							self.format.chord.size = size
							self.sf.chord.size = size
							self.sf.chorus.chord.size = size
						except BreakException:
							pass
					elif cmd == 'chordfont':
						try:
							face = self.GetAttribute()
							if face is None:
								raise BreakException
							self.format = ParagraphFormat(self.format)
							self.format.chord.face = face
							self.sf.chord.face = face
							self.sf.chorus.chord.face = face
						except BreakException:
							pass
					elif cmd == 'chordcolour':
						try:
							color = self.GetAttribute()
							if color is None:
								raise BreakException
							self.format = ParagraphFormat(self.format)
							self.format.chord.color = color
							self.sf.chord.color = color
							self.sf.chorus.chord.color = color
						except BreakException:
							pass

			self.EndLine()
			if empty:
				if state in {SongBlock.verse, SongBlock.title}:
					self.EndBlock()
				elif state == SongBlock.chorus:
					self.ChorusVSkip()
		self.EndBlock()
		w, h = self.sd.Draw(self.song, dc)
		self.dc = None
		return w, h

	def SetDecorator(self, sd):
		self.sd = sd
