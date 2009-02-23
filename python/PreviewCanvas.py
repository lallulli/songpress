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

class PreviewCanvas(object):
	"""Abstract class. Override methods New, Open, Save"""
	###UI generation###

	def __init__(self, parent, vh = VerseHandler(), ch = ChorusHandler()):
		self.frame = wx.Frame(parent, -1, "Preview")
		self.frame.Bind(wx.EVT_PAINT, self.OnPaint, self.frame)
		self.frame.SetBackgroundColour(wx.WHITE)
		self.text = ""
		self.frame.Show()
		self.vh = vh
		self.ch = ch
		
	def OnPaint(self, e):
		def BeginVerse():
			pass
			
		def EndVerse():
			pass
			
		def BeginChorus():
			pass
			
		def EndChorus():
			pass
			
		def ChorusVSkip():
			pass
			
		def AddText(text):
			pass
		
		def AddChord(chord):
			pass
			
		def AddTitle(title):
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
					
			if empty:
				if state == verse:
					EndVerse()
					state = none
				elif state == chorus:
					ChorusVSkip()
		
	def Refresh(self, text):
		self.text = text
		self.frame.Refresh()
