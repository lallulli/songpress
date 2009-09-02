###############################################################
# Name:			 SongDecorator.py
# Purpose:	 Base (and default) handlers for verse and chorus
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-21
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

from SongFormat import *
from SongBoxes import *

class SongDecorator(object):
	def __init__(self):
		object.__init__(self)
		self.dc = None
		# Current y
		self.y = 0
		self.dc = None
		# SongBox
		self.s = None
		
	def SetMarginText(self, text):
		# Modify text margins
		pass
		
	def SetMarginChord(self, chord):
		# Modify chord margins
		pass
		
	def SetMarginLine(self, line):
		# Modify line margins
		pass

	def SetMarginBlock(self, block):
		# Modify line margins
		pass

	def SetMarginSong(self, song):
		# Modify line margins
		pass
		
	def LayoutComposeLine(self, line):
		# Pass 1: determine size of text
		chordMaxH = 0
		chordMaxTH = 0
		textMaxH = 0
		textMaxTH = 0
		for t in line.boxes:
			self.dc.SetFont(t.font)
			t.w, t.h = self.dc.GetTextExtent(t.text)
			if t.type == SongText.chord:
				self.SetMarginChord(t)
				chordMaxH = max(chordMaxH, t.h)
				chordMaxTH = max(chordMaxTH, t.GetTotalHeight())
			else:
				self.SetMarginText(t)
				textMaxH = max(textMaxH, t.h)
				textMaxTH = max(textMaxTH, t.GetTotalHeight())
		line.chordBaseline = chordMaxTH
		line.textBaseline = chordMaxTH + chordMaxH * (line.parent.format.chordSpacing - 1) + textMaxTH
		line.h = line.textBaseline + textMaxH * (line.parent.format.textSpacing - 1)
		# Pass 2: set layout
		x = 0
		chordX = 0
		for t in line.boxes:
			self.dc.SetFont(t.font)
			if t.type == SongText.chord:
				t.x = max(x, chordX)
				x = t.x
				chordX = x + t.GetTotalWidth()
				t.y = line.chordBaseline - t.GetTotalHeight()
			else:
				t.x = x
				x = t.x + t.GetTotalWidth()
				t.y = line.textBaseline - t.GetTotalHeight()
			line.RelocateBox(t)
		self.SetMarginLine(line)
		
		
	def LayoutComposeBlock(self, block):
		y = 0
		for l in block.boxes:
			l.y = y
			y += l.GetTotalHeight()
			block.RelocateBox(l)
		self.SetMarginBlock(block)

	def LayoutComposeSong(self, song):
		y = 0
		self.dc.SetFont(song.format.wxFont)
		w, h = self.dc.GetTextExtent("Dummy")
		for b in song.boxes:
			b.y = y
			y += b.GetTotalHeight() + h * song.format.blockSpacing
			song.RelocateBox(b)
		self.SetMarginSong(song)
		

	def LayoutCompose(self):
		# Postorder layout composing
		for block in self.s.boxes:
			for line in block.boxes:
				self.LayoutComposeLine(line)
		for block in self.s.boxes:
			self.LayoutComposeBlock(block)				
		self.LayoutComposeSong(self.s)
		
	def LayoutMoveBlock(self, block):
		# Move block within song
		pass
		
	def LayoutMoveLine(self, line):
		# Move line within block
		# If we need to, we can even move text and chords inside this line
		pass

	def LayoutMove(self):
		# Now that sizes are set, we can move elements inside each box if we need to
		for block in self.s.boxes:
			# Move block within song
			self.LayoutMoveBlock(block)
			for line in block.boxes:
				# Move line within block
				# If we need to, we can even move text and chords inside this line
				self.LayoutMoveLine(line)
				
	def PreDrawSong(self, song):
		pass
		
	def PreDrawBlock(self, block, bx, by):
		# bx, by: coordinates of top-left corner of drawable area
		pass
		
	def PreDrawLine(self, line, lx, ly):
		# lx, ly: coordinates of top-left corner of drawable area
		pass
		
	def PreDrawText(self, text, tx, ty):
		# tx, ty: coordinates of top-left corner of drawable area
		pass
		
	def DrawText(self, text, tx, ty):
		# tx, ty: coordinates of top-left corner of drawable area
		self.dc.SetFont(text.font)
		self.dc.DrawText(text.text, tx + text.marginLeft, ty + text.marginTop)
		
	def PostDrawText(self, text, tx, ty):
		# tx, ty: coordinates of top-left corner of drawable area
		pass		
		
	def PostDrawLine(self, line, lx, ly):
		# lx, ly: coordinates of top-left corner of drawable area
		pass		
		
	def PostDrawBlock(self, block, bx, by):
		# bx, by: coordinates of top-left corner of drawable area
		pass
		
	def PostDrawSong(self, song):
		pass
		
	def DrawBoxes(self):
		if self.s.drawWholeSong:
			self.PreDrawSong(self.s)
			firstBlock = False
			firstBlockOffsetY = 0
		else:
			firstBlock = True
		for block in self.s.boxes:
			if block.drawBlock:
				if firstBlock:
					firstBlock = False
					firstBlockOffsetY = self.s.marginTop + block.y
				bx = self.s.marginLeft + block.x
				by = self.s.marginTop + block.y - firstBlockOffsetY
				self.PreDrawBlock(block, bx, by)
				for line in block.boxes:
					lx = bx + block.marginLeft + line.x
					ly = by + block.marginTop + line.y
					self.PreDrawLine(line, lx, ly)
					for text in line.boxes:
						tx = lx + line.marginLeft + text.x
						ty = ly + line.marginTop + text.y
						self.PreDrawText(text, tx, ty)
						self.DrawText(text, tx, ty)
						self.PostDrawText(text, tx, ty)
					self.PostDrawLine(line, lx, ly)
				self.PostDrawBlock(block, bx, by)
		if self.s.drawWholeSong:
			self.PostDrawSong(self.s)
		
	def InitDraw(self):
		pass
		
	def Draw(self, s, dc):
		# SongBox s
		self.s = s
		self.dc = dc
		self.InitDraw()
		self.LayoutCompose()
		self.LayoutMove()
		self.DrawBoxes()
		self.dc = None
		return self.s.GetTotalWidth(), self.s.GetTotalHeight()

	