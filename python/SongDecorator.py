###############################################################
# Name:			 SongDecorator.py
# Purpose:	 Base (and default) handlers for verse and chorus
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-21
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

from SongFormat import *
from Renderer import *

class SongDecorator(object):
	def __init__(self, sf = None):
		object.__init__(self)
		self.sf = None
		self.dc = None
		# Current y
		self.y = 0
		self.dc = None
		# SongBox
		self.s = None
		
	def LayoutComposeChord(self, text):
		# Modify chord size
		pass
		
	def LayoutComposeChord(self, text):
		# Modify text size
		pass
		
	def LayoutComposeLine(self, line):
		# Pass 1: determine size of text
		chordMaxH = 0
		textMaxH = 0
		for t in line.boxes:
			self.dc.SetFont(t.font)
			t.w, t.h = self.dc.GetTextExtent(t.text)
			if t.type == SongText.chord:
				self.LayoutComposeChord(t)
				chordMaxH = max(chordMaxH, t.h)
			else:
				self.LayoutComposeText(t)
				textMaxH = max(textMaxH, t.h)
		chordBaseline = chordMaxH
		textBaseline = chordMaxH * line.parent.format.chordSpacing + textMaxH
		line.h = textBaseline + textMaxH * (line.parent.format.textSpacing - 1)
		# Pass 2: set layout
		x = 0
		chordX = 0
		for t in line.boxes:
			self.dc.SetFont(t.font)
			if t.type == SongText.chord:
				t.x = max(x, chordX)
				x = t.x
				chordX = x + t.w 
				t.y = chordBaseline - t.h
			else:
				t.x = x
				x = t.x + t.w
				t.y = textBaseline - t.h
		line.w = max(x, chordX)
		
	def LayoutComposeBlock(self):
		pass


	def LayoutCompose(self):
		# Postorder layout composing
		for block in self.s.boxes:
			for line in block.boxes:
				self.LayoutComposeLine(line)
		for block in self.s.boxes:
			self.LayoutComposeBlock(block)				
		self.LayoutComposeSong()

	def LayoutMove(self):
		# Now that sizes are set, we can move elements inside each box if we need to
		for block in self.s.boxes:
			# Move block within song
			self.LayoutMoveBlock(block)
			for line in block.boxes:
				# Move line within block
				# If we need to, we can even move text and chords inside this line
				self.LayoutMoveLine(line)
				
	def DrawBoxes(self):
		self.PreDrawSong(song)
		for block in self.s.boxes:
			self.PreDrawBlock(block)
			for line in block.boxes:
				self.PreDrawLine(line)
				for text in line.boxes:
					self.PreDrawText(text)
					self.DrawText(text)
					self.PostDrawText(text)
				self.PostDrawLine(line)
			self.PostDrawBox(box)
		self.PostDrawSong(song)
		
	def Draw(self, s, dc):
		# SongBox s
		self.s = s
		self.dc = dc
		self.LayoutCompose()
		self.LayoutMove()
		self.DrawBoxes()
	
		
		
	rem = """	
	def PreSong(self):
		return (0, 0)
		
	def PostSong(self):
		pass
		
	def PreVerse(self, width, height):
		return (0, 0)
		
	def PostVerse(self):
		return 0
		
	def PreChord(self, width, height):
		return (0, 0)
		
	def PostChord(self):
		return 0
		
	def PreTitle(self, width, height):
		return (0, 0)
		
	def PostTitle(self):
		return 0
		
	def PreLine(self, width, height):
		return (0, 0)
		
	def PostLine(self):
		return 0
		
	def Draw(self, blocks, width, height, sf, dc):
		self.blocks = blocks
		self.width = width
		self.height = height
		self.sf = sf
		self.dc = dc
		self.y = 0
		(self.globalOffsetX, self.y) = self.PreSong()
		for b in blocks:
			self.currentBlock = b
			if b.type == b.verse:
				Pre = self.PreVerse
				Post = self.PostVerse
			elif b.type == b.chord:
				Pre = self.PreChord
				Post = self.PostChord
			elif b.type == b.title:
				Pre = self.PreTitle
				Post = self.PostTitle
			self.blockLeftMargin = self.globalOffsetX + b.format.leftMargin
			self.blockStartY = self.y
			(x, y) = Pre(b.width, b.height)
			self.blockOffsetX = self.blockLeftMargin + x
			self.y += y
			for cl, tl, w, h in zip(b.chordLines, b.textLines, b.lineWidths, b.lineHeights):
				x, y = self.PreLine(w, h)
				ox = self.blockOffsetX + x
				self.y += y
				if len(cl) > 0:
					dc.SetFont(self.cl[0].font)
					for c in cl:
						dc.DrawText(c.text, c.x + ox, self.y)
					self.y += b.chordHeight * b.format.chordSpacing
				for t in tl:
					dc.SetFont(t.font)
					dc.DrawText(t.text, t.x + ox, self.y)
				self.y += b.textHeight * b.format.textSpacing				
				self.y += self.PostLine()
			self.y += Post()
		self.PostSong()
		self.dc = None
	"""
	