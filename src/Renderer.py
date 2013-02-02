###############################################################
# Name:			 Renderer.py
# Purpose:	 Render a song on a dc
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-21
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import wx
from SongDecorator import *
from SongTokenizer import *
from SongFormat import *
from SongBoxes import *

class Renderer(object):

	def __init__(self, sf, sd = SongDecorator()):
		object.__init__(self)
		self.text = ""
		self.sd = sd
		self.dc = None
		# SongFormat
		self.sf = sf
		self.textFont = None
		self.chordFont = None
		self.commentFont = None
		self.format = None
		self.currentBlock = None
		self.currentLine = None
		self.song = None

	def BeginBlock(self, type, label=None):
		self.EndBlock()
		if type == SongBlock.verse:
			if label is None:
				self.song.verseCount += 1
			self.sf.StubSetVerseCount(self.song.verseCount)
			self.format = self.sf.verse[self.song.verseCount-1]
		elif type == SongBlock.chorus:
			self.format = self.sf.chorus
		else:
			self.format = self.sf.title
		self.currentBlock = SongBlock(type, self.format)
		self.currentBlock.label = label
		self.currentBlock.verseNumber = self.song.verseCount
		self.textFont = self.format.wxFont
		self.chordFont = self.format.chord.wxFont
		self.commentFont = self.format.comment.wxFont

	def EndBlock(self):
		if self.currentBlock != None:
			self.EndLine()
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
			and type != SongText.comment
			and self.currentBlock is not None
			and self.currentBlock.type == SongBlock.title
		):
			self.EndBlock()
		self.BeginVerse()
		self.BeginLine()
		if type == SongText.comment:
			text = "(" + text + ")"
			font = self.commentFont
		elif type == SongText.chord:
			font = self.chordFont
		else:
			font = self.textFont
		t = SongText(text, font, type)
		self.currentLine.AddBox(t)

	def AddTitle(self, title):
		self.BeginBlock(SongBlock.title)
		self.AddText(title, SongText.title)
		#self.EndBlock()

	def BeginLine(self):
		if self.currentLine == None:
			if self.song.drawWholeSong or (self.fromLine <= self.lineCount and self.lineCount <= self.toLine):
				self.currentBlock.drawBlock = True
			self.currentLine = SongLine()

	def EndLine(self):
		if self.currentLine != None:
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
				return None
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
						if a != None:
							self.AddText(a, SongText.comment)
					elif cmd == 't' or cmd == 'title':
						a = self.GetAttribute()
						if a != None:
							self.AddTitle(a)
					elif cmd == 'verse':
						self.BeginVerse(self.GetAttribute())

			self.EndLine()
			if empty:
				if state == SongBlock.verse or state == SongBlock.title:
					self.EndBlock()
				elif state == SongBlock.chorus:
					self.ChorusVSkip()
		self.EndBlock()
		w, h = self.sd.Draw(self.song, dc)
		self.dc = None
		return w, h

	def SetDecorator(self, sd):
		self.sd = sd
