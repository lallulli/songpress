###############################################################
# Name:			 Tokenizer.py
# Purpose:	 Abstract tokenizer
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-31
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

import re

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
	
		
class Tokenizer(object):
	def __init__(self, l):
		object.__init__(self)
		self.line = l
		self.pos = 0
		self.state = self.normal
		self.prevToken = None
		self.repeatToken = False
		
	def __iter__(self):
		return self
		
	def next(self):
		if self.repeatToken:
			self.repeatToken = False
			return self.prevToken
		if self.pos >= len(self.line):
			#End of line
			raise StopIteration
		for t in self.transition[self.state]:
			#print "Trying: %s" % (t[0],)
			m = t[0].r.match(self.line, self.pos)
			if m != None:
				#print("Matched!")
				break
		if m == None:
			return None				
		tok = Token(t[0], self.pos, m.end(0), m.group(0))
		#print (type(m.group(0)), m.group(0))
		self.state = t[1]
		#print("Found %s" % (tok,))
		self.pos = m.end(0)
		self.prevToken = tok
		return tok

	def Repeat(self, repeat = True):
		self.repeatToken = repeat