###############################################################
# Name:			 SoongBoxes.py
# Purpose:	 Elements that make up a song
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-02-21
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

import wx
from SongFormat import *

class SongBox(object):
	def __init__(self, x, y, w, h):
		object.__init__(self)
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.marginLeft = 0
		self.marginRight = 0
		self.marginTop = 0
		self.marginBottom = 0
		self.boxes = []

	def RelocateBox(self, box):
		self.w = max(self.w, box.x + box.GetTotalWidth())
		self.h = max(self.h, box.y + box.GetTotalHeight())
		
	def AddBox(self, box):
		self.boxes.append(box)
		box.parent = self
		self.RelocateBox(box)
		
	def SetMargin(self, top, right, bottom, left):
		self.marginTop = top
		self.marginRight = right
		self.marginBottom = bottom
		self.marginLeft = left
		
	def GetTotalHeight(self):
		return self.h + self.marginTop + self.marginBottom

	def GetTotalWidth(self):
		return self.w + self.marginLeft + self.marginRight

	
class SongSong(SongBox):
	def __init__(self, format):
		SongBox.__init__(self, 0, 0, 0, 0)
		self.format = format
		self.verseCount = 0
		self.chorusCount = 0
		self.labelCount = 0
		self.drawWholeSong = False


class SongBlock(SongBox):
	# types
	verse = 1
	chorus = 2
	title = 3

	def __init__(self, type, format):
		SongBox.__init__(self, 0, 0, 0, 0)
		self.type = type
		self.verseNumber = 0
		self.format = format
		self.drawBlock = False
		self.label = None
		self.chords = []
		
	def RemoveChordBoxes(self):
		for l in self.boxes:
			l.RemoveChordBoxes()

			
class SongLine(SongBox):
	def __init__(self):
		SongBox.__init__(self, 0, 0, 0, 0)
		self.hasChords = False
		self.chordBaseline = 0
		self.textBaseline = 0

	def AddBox(self, text):
		if text.type == text.chord:
			self.hasChords = True
		SongBox.AddBox(self, text)
		
	def RemoveChordBoxes(self):
		self.boxes = [b for b in self.boxes if b.type != b.chord]
		
	
class SongText(SongBox):
	text = 1
	chord = 2
	comment = 3
	title = 4
	subtitle = 5
	
	def __init__(self, text, font, type, color):
		SongBox.__init__(self, 0, 0, 0, 0)
		self.text = text
		self.font = font
		self.type = type
		self.color = color
