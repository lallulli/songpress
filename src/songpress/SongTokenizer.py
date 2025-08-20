###############################################################
# Name:			 SongTokenizer.py
# Purpose:	 Subclass of Tokenizer to tokenize songs
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-31
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

		
import re

from .Tokenizer import *


class SongTokenizer(Tokenizer):
	def __init__(self, l):
		Tokenizer.__init__(self, l)
		
	#Tokens
	openCurlyToken = TokenType('(\{)', 'openCurlyToken')
	closeCurlyToken = TokenType('(\})', 'closeCurlyToken')
	commentToken = TokenType('^([ \t]*#.*)$', 'commentToken')
	normalToken = TokenType('([^[{]+)', 'normalToken')
	commandToken = TokenType('([^}:]+)', 'commandToken')
	attrToken = TokenType('([^}]+)', 'attrToken')
	chordToken = TokenType('(\[[^]]*)', 'chordToken')
	closeChordToken = TokenType('(\])', 'closeChordToken')
	colonToken = TokenType('(:)', 'colonToken')

	#States
	normal = 1
	command = 2
	attr = 3
	
	#Transition function
	transition = {
		normal: (
			(openCurlyToken, command),
			(chordToken, normal),
			(closeChordToken, normal),
			(commentToken, normal),
			(normalToken, normal),
		),
		command: (
			(colonToken, attr),
			(closeCurlyToken, normal),
			(commandToken, command),
		),
		attr: (
			(attrToken, attr),
			(closeCurlyToken, normal),
			(commentToken, normal),
		)
	}

