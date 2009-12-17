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
import math

i18n.register('Transpose')

class Notation(object):
	def __init__(self, id, desc, chords, repl, replrev):
		object.__init__(self)
		self.id = id
		self.desc = desc
		self.chords = chords
		self.chordDict = {}
		i = 0
		for k in chords:
			self.chordDict[k.upper()] = i
			i += 1
		self.repl = [(re.compile(x[0]), x[1]) for x in repl]
		self.replrev = [(re.compile(x[0]), x[1]) for x in replrev]		
		
	def Ord2Chord(self, pos):
		return self.chords[pos]
		
	def Chord2Ord(self, chord):
		return self.chordDict[chord.upper()]
		
	def __AlterationStandard(self, a, rs):
		for r in rs:
			p = 0
			b = ''
			for m in r[0].finditer(a):
				b += a[p:m.start()] + r[1]
				p = m.end()
			b += a[p:]
			a = b
		return a
		
	def PostprocessingFromStandard(self, c, a):
		return c, a
		
	def PreprocessingToStandard(self, c, a):
		return c, a
	
	def AlterationFromStandard(self, a):
		return self.__AlterationStandard(a, self.repl)
	
	def AlterationToStandard(self, a):
		return self.__AlterationStandard(a, self.replrev)
	

enNotation = Notation(
	"enNotation",
	_("American (C D E... B)"),
	['C', 'D', 'E', 'F', 'G', 'A', 'B'],
	[],
	[]
)

itNotation = Notation(
	"itNotation",
	_("Italian (Do Re Mi... Si)"),
	['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Si'],
	[
		(r'maj7', '7+'),
		(r'sus4', '4'),
		(r'^m', '-')
	],
	[
		(r'7\+', 'maj7'),
		(r'^4', 'sus4'),
		(r'^-', 'm')
	]	
)

defaultLangNotation = {
	'en': enNotation,
	'it': itNotation
}

class GermanNotation(Notation):
	def PreprocessingToStandard(self, c, a):
		if c == '' and a != '' and a[0].upper() == 'B':
			c = 'Hb'
			a = a[1:]
		if a != "" and a[0] == 'm':
			c = c.upper()
		return c, a
			
	def PostprocessingFromStandard(self, c, a):
		if c == 'Hb':
			c = 'B'
		if a != "" and a[0] == 'm':
			c = c.lower() 
		return c, a

deNotation = GermanNotation(
	"deNotation",
	_("German (C D E... H)"),
	['C', 'D', 'E', 'F', 'G', 'A', 'H'],
	[],
	[]
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
	'Gb': (6, ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'Fb']), # E#?
	'G': (7, ['G', 'A', 'B', 'C', 'D', 'E', 'F#']),
	'Ab': (8, ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G']),
	'A': (9, ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#']),
	'Bb': (10, ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A']),
	'B': (11, ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'])
}
orderedKeys = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

vectorModes = ['', 'm', '7', 'm7']

referenceVector = [0.65713162540630443, 0.0, 0.037841466800806009, 0.0, 0.0, 0.0014554410308002313, 0.0, 0.0, 0.026197938554404162, 0.12444020813341977, 0.0014554410308002313, 0.029108820616004623, 0.0, 0.0, 0.0, 0.0, 0.040024628347006361, 0.12589564916422, 0.030564261646804855, 0.0036386025770005779, 0.46210252727907342, 0.013098969277202081, 0.0, 0.0, 0.0, 0.00072772051540011566, 0.0, 0.0, 0.49703311201827893, 0.0, 0.016009851338802544, 0.0, 0.00072772051540011566, 0.0, 0.0, 0.0, 0.0094603667002015022, 0.2648902676056421, 0.0058217641232009253, 0.0043663230924006939, 0.0014554410308002313, 0.0, 0.00072772051540011566, 0.0, 0.0, 0.0014554410308002313, 0.0, 0.0]

def splitChord(c, locNotation=enNotation):
	for k in locNotation.chords:
		if c.upper().startswith(k.upper()):
			if len(c) != len(k):
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

def chord2pos(chord, key="C"):
	c, a = __alteration(chord)
	s, b = __alteration(key)
	return (tone[c] + a - tone[s] - b) % 12
	
def __pos2chord(pos, key):
	n, i = interval[pos]
	# if pos in scale, use it
	if i == 0:
		return scales[key][1][n]
	# else use natural scale
	ref = scales[key][0]
	diff = (pos + ref) % 12
	return naturalScale[diff]	

def transpose(s, d, chord, notation=enNotation):
	chord = translateChord(chord, notation, enNotation)
	c, v = splitChord(chord)
	if c == "":
		return chord
	p = chord2pos(c, s)
	return translateChord(__pos2chord(p, d) + v, enNotation, notation)
	
def translateChord(chord, sNotation=enNotation, dNotation=enNotation):
	if sNotation == dNotation:
		return chord
	c, a = splitChord(chord, sNotation)
	c, a = sNotation.PreprocessingToStandard(c, a)
	if c == "":
		return chord
	alt = c[-1]
	if alt == '#' or alt == 'b':
		c = c[:-1]
	else:
		alt = ""
	d = dNotation.Ord2Chord(sNotation.Chord2Ord(c)) + alt
	b = dNotation.AlterationFromStandard(sNotation.AlterationToStandard(a))
	d, b = dNotation.PostprocessingFromStandard(d, b)
	return d + b
	
def transposeChordPro(s, d, text, notation=enNotation):
	r = re.compile('\[([^]]*)\]')
	p = 0
	b = ''
	for m in r.finditer(text):
		b += "%s[%s]" % (
			text[p:m.start()],
			transpose(s, d, m.group(1), notation)
		)
		p = m.end()
	return b + text[p:]

def translateChordPro(text, sNotation=enNotation, dNotation=enNotation):
	r = re.compile('\[([^]]*)\]')
	p = 0
	b = ''
	for m in r.finditer(text):
		b += "%s[%s]" % (
			text[p:m.start()],
			translateChord(m.group(1), sNotation, dNotation)
		)
		p = m.end()
	return b + text[p:]
	
def autodetectNotation(text, notations):
	r = re.compile('\[([^]]*)\]')
	cnt = [0 for x in notations]
	for m in r.finditer(text):
		for i in xrange(0, len(notations)):
			c, a = splitChord(m.group(1), notations[i])
			if c != "":
				cnt[i] += 1
	return notations[cnt.index(max(cnt))]
	
def normalize(vector):
	count = 0
	for c in vector:
		count += c**2
	if count != 0:
		count = math.sqrt(count)
		return [x/count for x in vector]
	else:
		return vector

def scalarProduct(v1, v2):
	count = 0
	for i in xrange(0, len(v1)):
		count += v1[i]*v2[i]
	return count
	
def vectorizeChords(text, notation=enNotation):
	r = re.compile('\[([^]]*)\]')
	v = [0 for x in xrange(12 * len(vectorModes))]
	for m in r.finditer(text):
		chord = translateChord(m.group(1), notation, enNotation)
		c, a = splitChord(chord)
		if c != "" and a in vectorModes:
			v[chord2pos(c, "C") * len(vectorModes) + vectorModes.index(a)] += 1
	return normalize(v)

def autodetectKey(text, notation=enNotation):
	v = vectorizeChords(text, notation)
	r = referenceVector
	max = 0
	key = 0
	n = len(vectorModes)
	for k in xrange(0, 12):
		s = scalarProduct(v, r)
		if s > max:
			max = s
			key = k
		r = r[-n:] + r[:-n]
	return naturalScale[key]