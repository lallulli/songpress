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
		chordBaseline = chordMaxTH
		textBaseline = chordMaxTH + chordMaxH * (line.parent.format.chordSpacing - 1) + textMaxTH
		line.h = textBaseline + textMaxH * (line.parent.format.textSpacing - 1)
		# Pass 2: set layout
		x = 0
		chordX = 0
		for t in line.boxes:
			self.dc.SetFont(t.font)
			if t.type == SongText.chord:
				t.x = max(x, chordX)
				x = t.x
				chordX = x + t.GetTotalWidth()
				t.y = chordBaseline - t.GetTotalHeight()
			else:
				t.x = x
				x = t.x + t.GetTotalWidth()
				t.y = textBaseline - t.GetTotalHeight()
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
			y += b.GetTotalHeight() + h * song.blockSpacing
			song.RelocateBox(b)
		self.SetMarginSong(song)
		

	def LayoutCompose(self):
		# Postorder layout composing
		for block in self.s.boxes:
			for line in block.boxes:
				self.LayoutComposeLine(line)
		for block in self.s.boxes:
			self.LayoutComposeBlock(block)				
		self.LayoutComposeSong()
		
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
		dc.SetFont(text.font)
		dc.DrawText(text.text, tx + t.marginLeft, ty + t.marginTop)
		
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
		self.PreDrawSong(song)
		for block in self.s.boxes:
			bx = song.marginLeft + block.x
			by = song.marginTop + block.y
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
	