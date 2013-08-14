# -*- coding: iso-8859-1 -*-

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
		self.descv = desc
		self.chords = chords
		self.chordDict = {}
		i = 0
		for k in chords:
			self.chordDict[k.upper()] = i
			i += 1
		self.repl = [(re.compile(x[0]), x[1]) for x in repl]
		self.replrev = [(re.compile(x[0]), x[1]) for x in replrev]

	def GetDesc(self):
		return _(self.descv)

	def SetDesc(self, v):
		pass

	desc = property(GetDesc, SetDesc)

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

frNotation = Notation(
	"frNotation",
	_(u"French (Do Ré Mi... Si)"),
	['Do', u'Ré', 'Mi', 'Fa', 'Sol', 'La', 'Si'],
	[
		(r'maj7', '7+'),
		(r'sus4', '4'),
	],
	[
		(r'7\+', 'maj7'),
		(r'^4', 'sus4'),
	]
)

ptNotation = Notation(
	"ptNotation",
	_(u"Portuguese (Dó Ré Mi... Si)"),
	[u'Dó', u'Ré', 'Mi', u'Fá', 'Sol', u'Lá', 'Si'],
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
	'it': itNotation,
	'fr': frNotation,
}

easyChords = {
	'basic': (_("Basic chords (A, E, D)"), ["A", "E", "D"], 4),
	'Cprog': (_("50s progr. in C (C, Am, Dm, G7)"), ["C", "Am", "Dm", "G7"], 4),
	'F': (_("F chord"), ["F"], 2),
	'Gprog': (_("50s progr. in G (G, Em, Am, D7)"), ["G", "Em", "Am", "D7"], 4),
	'Dprog': (_("50s progr. in D (D, Bm, Em, A7)"), ["D", "Bm", "Em", "A7"], 1),
	'Aprog': (_("50s progr. in A (A, F#m, Bm, E7)"), ["A", "F#m", "Bm", "E7"], 1),
	'C#(m)(7)': (_("C#, C#m, C#7 chords"), ["C#", "C#m", "C#7"], 0),
	'Fprog': (_("50s progr. in F (F, Dm, Gm, C7)"), ["F", "Dm", "Gm", "C7"], 0),
	'BB7': (_("B and B7 chords"), ["B", "B7"], 0),
}

def getEasyChordsDescription(e):
	return _(e[0])

easyChordsOrder = ['basic', 'Cprog', 'F', 'Gprog', 'Dprog', 'Aprog', 'C#(m)(7)', 'Fprog', 'BB7']

class GermanNotation(Notation):
	def PreprocessingToStandard(self, c, a):
		if c == '' and a != '' and a[0].upper() == 'B':
			c = 'Hb'
			a = a[1:]
		if a != "" and a[0] == 'm':
			c = c.capitalize()
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
	return (tone[c.upper()] + a - tone[s.upper()] - b) % 12

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
	sl = chord.find("/")
	if sl > -1:
		return "%s/%s" % (transpose(s, d, chord[:sl], notation), transpose(s, d, chord[sl + 1:], notation))
	chord = translateChord(chord, notation, enNotation)
	c, v = splitChord(chord)
	if c == "":
		return chord
	p = chord2pos(c, s)
	return translateChord(__pos2chord(p, d) + v, enNotation, notation)

def translateChord(chord, sNotation=enNotation, dNotation=enNotation):
	#if sNotation == dNotation:
	#	return chord
	sl = chord.find("/")
	if sl > -1:
		return "%s/%s" % (translateChord(chord[:sl], sNotation, dNotation), translateChord(chord[sl + 1:], sNotation, dNotation))
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
	return orderedKeys[key]

def integrateChords(chords, text):
	"""Integrate chord line in text line, as chordpro"""
	r = re.compile(r'(\S+)')
	i = r.finditer(chords)
	l = [x for x in i]
	l.reverse()
	if l != []:
		lc = l[0].start()
		lt = len(text)
		for i in xrange(0, lc-lt):
			text += ' '
		for m in l:
			s = m.start()
			text = text[:s] + '[' + m.group() + ']' + text[s:]
	return text

def testChordLine(line, notation=enNotation):
	"""Return True iff line contains only chords"""
	# First, tokenize line: if a token is not a chord => False
	r = re.compile(r'(\S+)')
	l = 0
	n = 0
	for m in r.finditer(line):
		c = m.group()
		e, a = splitChord(c, notation)
		e, a = notation.PreprocessingToStandard(e, a)
		if e == '':
			return False
		l += len(translateChord(c, notation, enNotation))
		n += 1
	# We don't consider an empty line a chord line
	if n == 0:
		return False
	# Looks okay... if a whitespace is occurring twice => True
	if line.find("  ") != -1:
		return True
	# Uhm, weird... are chord tokens "short"? Yes <=> True
	return l/float(n) <= 2.3

def testTabFormat(text, notations):
	"""
	Test whether text is in tab format

	It happens iff at least 3 lines are chord lines.
	Return the best matching notation, or None
	notations is a list of notations to be tested
	"""
	lines = text.splitlines()
	max = 0
	maxn = None
	for n in notations:
		nc = 0
		for l in lines:
			if testChordLine(l, n):
				nc += 1
		if nc > max and nc >= 3:
			max = nc
			maxn = n
	return maxn

def tab2ChordPro(text, notation=enNotation):
	"""Convert text from tab to chordpro format"""
	l = text.splitlines()
	n = len(l)
	i = 0
	out = []
	while i < n:
		if i + 1 < n and testChordLine(l[i], notation) and not testChordLine(l[i+1], notation):
			out.append(integrateChords(l[i], l[i+1]))
			i += 2
		else:
			out.append(l[i])
			i += 1
	return "\n".join(out)

def testSpuriousLines(text):
	"""Determine if there are spurious empty lines

	It happens iff at least 1/3 of the lines are empty,
	and there are at least 3 non-empty lines
	"""
	c = 0
	ll = text.splitlines()
	for l in ll:
		if l.strip() == '':
			c += 1
	return c >= len(ll)/3.0 and len(ll) - c >= 3

def removeSpuriousLines(text):
	"""
	Remove spurious blank lines from text

	If a blank line is isolated, remove it
	If there are several contiguous blank lines, keep only one of them
	"""
	out = []
	ll = text.splitlines()
	ln = len(ll)
	i = 0
	def empty(l):
		return l.strip() == ''
	while i < ln:
		if empty(ll[i]):
			if i + 1 < ln and empty(ll[i + 1]):
				out.append('')
				i += 2
				while i < ln and empty(ll[i]):
					i += 1
			else:
				i += 1
		else:
			out.append(ll[i])
			i += 1
	return "\n".join(out)

def findEasiestKey(text, fav, notation=enNotation):
	"""
	Find easiest key for song.

		text: song text
		fav: dictionary of (s)favourite chords, with the form {chord: weight}
		     (chords in fav are expressed using enNotation)
		return (chord_count, current_key, current_difficulty, easiest_key, easiest_difficulty)
	"""
	current_key = autodetectKey(text, notation)
	ws = dict([(k, 0) for k in scales])
	r = re.compile('\[([^]]*)\]')
	count = 0
	for m in r.finditer(text):
		count += 1
		chord = translateChord(m.group(1), notation)
		for k in ws:
			c = transpose(current_key, k, chord)
			if c in fav:
				ws[k] += fav[c]
	easiest_key = current_key
	m = ws[easiest_key]
	for k in ws:
		if m is None or ws[k] > m:
			easiest_key = k
			m = ws[k]
	difficulty = lambda x: max(0, min(1, (count - x) / float(count)))
	if count > 0:
		return (
				count,
				translateChord(current_key, enNotation, notation),
				difficulty(ws[current_key]),
				translateChord(easiest_key, enNotation, notation),
				difficulty(m),
			)
	return (0, current_key, 0, current_key, 0)

def removeChords(text):
	"""
	Remove all chords in (ChordPro) text.

		text: song text
		return: text without chords
	"""
	return re.sub('\[([^]]*)\]', "", text)

def removeChordPro(text):
	"""
	Remove every ChordPro tag, including chords, from text.

		text: song text
		return: text without ChordPro stuff and chords
	"""
	return removeSpuriousLines(re.sub('(\[([^]]*)\]|{[^}]*})', "", text))


def pasteChords(src, dest):
	"""
	Paste chords from src to dest

	Remove any existing chords in lines in the first k lines of dest,
	if there are k lines in src.
		src: source chordpro text
		dest: destination text
	"""
	ss = src.splitlines()
	sd = dest.splitlines()
	out = []
	m = min(len(ss), len(sd))
	r = re.compile('\[([^]]*)\]')
	for i in xrange(0, m):
		cd = r.sub("", sd[i])
		for x in r.finditer(ss[i]):
			s = x.start()
			if len(cd) < s:
				cd += "".join([" " for y in xrange(len(cd), s)])
			cd = cd[:s] + x.group(0) + cd[s:]
		out.append(cd)
	for i in xrange(m, len(sd)):
		out.append(r.sub("", sd[i]))
	return "\n".join(out)
