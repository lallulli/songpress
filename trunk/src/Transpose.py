###############################################################
# Name:			 Transpose.py
# Purpose:	 Transposing services
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-11-18
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

from Globals import *
import i18n
import re

class Scale(object):
	def __init__(self, desc, chords, repl):
		object.__init__(self)
		self.desc = desc
		self.chords = chords
		self.repl = repl
		self.chordDict = {}
		i = 0
		for k in chords:
			self.chordDict[k] = i
			i += 1
		
	def Ord2Chord(self, pos):
		return self.chords[pos]
		
	def Chord2Ord(self, chord):
		return self.chordDict[chord]
		
	def __AlterationStandard(self, a, s, d):
		i = 0
		n = len(a)
		b = ''
		while i < n:
			subs = False
			for k in self.repl:
				if a[i:].startswith(k[s]):
					b += k[d]
					i += len(k[s])
					subs = True
					break
			if not subs:
				b += a[i]
				i += 1
		return b
	
	def AlterationFromStandard(self, a):
		return self.__AlterationStandard(a, 0, 1)
	
	def AlterationToStandard(self, a):
		return self.__AlterationStandard(a, 1, 0)
		

engScale = Scale(
	'C D E...',
	['C', 'D', 'E', 'F', 'G', 'A', 'B'],
	[]
)

itScale = Scale(
	'Do Re Mi...',
	['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Si'],
	[
		('maj7', '7+'),
		('sus4', '4'),
		('m', '-')
	]
)

naturalScale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

tone = {
	'C': 0,
	'D': 2,
	'E': 4,
	'F': 5,
	'G': 7,
	'A': 9,
	'B': 11
}

interval = [
 (0, 0),
 (0, 1),
 (1, 0),
 (1, 1),
 (2, 0),
 (3, 0),
 (3, 1),
 (4, 0),
 (4, 1),
 (5, 0),
 (5, 1),
 (6, 0),
 (6, 1),
 (7, 0)
]

scales = {
	'C': (0, ['C', 'D', 'E', 'F', 'G', 'A', 'B']),
	'Db': (1, ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C']),
	'D': (2, ['D', 'E', 'F#', 'G', 'A', 'B', 'C#']),
	'Eb': (3, ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D']),
	'E': (4, ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#']),
	'F': (5, ['F', 'G', 'A', 'Bb', 'C', 'D', 'E']),
	'F#': (6, ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#']), # E#?
	'G': (7, ['G', 'A', 'B', 'C', 'D', 'E', 'F#']),
	'Ab': (8, ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G']),
	'A': (9, ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#']),
	'Bb': (10, ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A']),
	'B': (11, ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'])
}

def splitChord(c, locScale=engScale):
	for k in locScale.chords:
		if c.startswith(k):
			if c != k:
				d = c[len(k)]
				if d == "b" or d == "#":
					return (k+d, c[(len(k) + 1):])
				return (k, c[len(k):])
			return (c, "")
	return ("", c)
	
def __alteration(chord):
	if len(chord) == 1:
		return (chord, 0)
	elif chord[1] == '#':
		return (chord[0], 1)
	else:
		return (chord[0], -1)

def __chord2pos(chord, scale):
	c, a = __alteration(chord)
	s, b = __alteration(scale)
	return (tone[c] + a - tone[s] - b) % 12
	
def __pos2chord(pos, scale):
	n, i = interval[pos]
	# if pos in scale, use it
	if i == 0:
		return scales[scale][1][n]
	# else use natural scale
	ref = scales[scale][0]
	diff = (pos + ref) % 12
	return naturalScale[diff]	

def transpose(s, d, chord, scale=engScale):
	chord = translateChord(chord, scale, engScale)
	c, v = splitChord(chord)
	p = __chord2pos(c, s)
	return translateChord(__pos2chord(p, d) + v, engScale, scale)
	
def translateChord(chord, sScale=engScale, dScale=engScale):
	if sScale == dScale:
		return chord
	c, a = splitChord(chord, sScale)
	alt = c[-1]
	if alt == '#' or alt == 'b':
		c = c[:-1]
		a = alt + a
	d = dScale.Ord2Chord(sScale.Chord2Ord(c))
	b = dScale.AlterationFromStandard(sScale.AlterationToStandard(a))
	return d + b
	
def transposeChordPro(s, d, text, scale=engScale):
	r = re.compile('\[([^]]*)\]')
	p = 0
	b = ''
	for m in r.finditer(text):
		b += "%s[%s]" % (
			text[p:m.start()],
			transpose(s, d, m.group(1), scale)
		)
		p = m.end()
	return b + text[p:]

def translateChordPro(text, sScale=engScale, dScale=engScale):
	r = re.compile('\[([^]]*)\]')
	p = 0
	b = ''
	for m in r.finditer(text):
		b += "%s[%s]" % (
			text[p:m.start()],
			translateChord(m.group(1), sScale, dScale)
		)
		p = m.end()
	return b + text[p:]
