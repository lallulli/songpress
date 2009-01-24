###############################################################
# Name:			 main.py
# Purpose:	 Entry point for Songpress
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-16
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

		
import wx
from wx import xrc
from wx.stc import *
from SDIMainFrame import *
import re
from Enumerate import Enumerate
import sys

class Token(object):
	def __init__(self, token, start, end, content):
		object.__init__(self)
		self.token = token
		self.start = start
		self.end = end
		self.content = content
		
	def __str__(self):
		return '%s, %d, %d, %s' % (str(self.token), self.start, self.end, self.content)
		
class TokenType(object):
	def __init__(self, r, name):
		object.__init__(self)
		self.r = re.compile(r)
		self.name = name
		
	def __str__(self):
		return self.name

class Editor(StyledTextCtrl):

	def __init__(self, spframe):
		StyledTextCtrl.__init__(self, spframe.frame)
		self.spframe = spframe
		self.spframe.frame.Bind(EVT_STC_MODIFIED, self.OnTextModified, self)
		font = wx.Font(
			12,
			wx.FONTFAMILY_DEFAULT,
			wx.FONTSTYLE_NORMAL,
			wx.FONTWEIGHT_NORMAL,
			faceName = "Times New Roman"
		)
		self.StyleSetFont(STC_STYLE_DEFAULT, font)
		self.spframe.frame.Bind(EVT_STC_STYLENEEDED, self.OnStyleNeeded, self)
		self.SetLexer(STC_LEX_CONTAINER)
		self.STC_STYLE_RED = 11
		self.STC_STYLE_BLUE = 12
		self.StyleSetForeground(self.STC_STYLE_RED, wx.Color(255, 0, 0))
		self.StyleSetForeground(self.STC_STYLE_BLUE, wx.Color(0, 0, 255))
		self.reChord = re.compile('(\[[^]]*\])')
		self.__initRegularExpressions()
		
	def __initRegularExpressions(self):
		self.openCurlyToken = TokenType('(\{)', 'openCurlyToken')
		self.closeCurlyToken = TokenType('(\})', 'closeCurlyToken')
		self.normalToken = TokenType('([^[{]+)', 'normalToken')
		self.commandToken = TokenType('([^}:]+)', 'commandToken')
		self.attrToken = TokenType('([^}]+)', 'attrToken')
		self.chordToken = TokenType('(\[[^]]+)', 'chordToken')
		self.closeChordToken = TokenType('(\])', 'closeChordToken')
		self.colonToken = TokenType('(:)', 'colonToken')
	
	def New(self):
		print("File->New");
		
	def Open(self):
		self.LoadFile(self.spframe.document)
		
	def Save(self):
		self.SaveFile(self.spframe.document)
		
	def OnTextModified(self, evt):
		self.spframe.SetModified()
	
	
	def __NextToken(self):
	
		def MatchToken(list):
			for t in list:
				m = t.r.match(self.tokenLine, self.tokenPos)
				if m != None:
					break
			if m == None:
				return None				
			tok = Token(t, self.tokenPos, m.end(0), m.group(0))
			print("Found %s" % (tok,))
			self.tokenPos = m.end(0)
			return tok
	
		#End of line
		if self.tokenPos >= len(self.tokenLine):
			return None
		if self.tokenState == self.normal:
			list = (self.openCurlyToken, self.chordToken, self.closeChordToken, self.normalToken)
		elif self.tokenState == self.command:
			list = (self.colonToken, self.closeCurlyToken, self.commandToken)
		else: #self.tokenState == self.attr:
			list = (self.attrToken, self.closeCurlyToken)

		return MatchToken(list)

	def __StartTokenize(self, l):
		self.tokenLine = l
		self.tokenPos = 0
		self.tokenState = self.normal
		print l
	
	def OnStyleNeeded(self, evt):
		end = evt.GetPosition()
		pos = self.GetEndStyled()
		ln = self.LineFromPosition(pos)
		l = self.GetLine(ln)
		start = self.PositionFromLine(ln)
		self.StartStyling(start, 0x1f)
		self.__StartTokenize(l)
		tok = self.__NextToken()
		while tok != None:
			t = tok.token
			if self.tokenState == self.normal:
				if t == self.normalToken:
					pass
				elif t == self.openCurlyToken:
					self.tokenState = self.command
				else: #t == self.chordToken or t == self.closeChordToken
					pass
			elif self.tokenState == self.command:
				if t == self.commandToken:
					pass
				elif t == self.colonToken:
					self.tokenState = self.attr
				else: #t == self.closeCurlyToken
					self.tokenState = self.normal
			else: # self.tokenState == self.attr
				if t == self.attrToken:
					pass
				else: #t = self.closeCurlyToken
					self.tokenState = self.normal
					
			print "state = %d" % (self.tokenState,)
			
			tok = self.__NextToken()
		
		
		self.SetStyling(pos-start, self.STC_STYLE_BLUE)
		
		


Enumerate(Editor, ('normal', 'command', 'attr'))
