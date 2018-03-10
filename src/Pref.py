###############################################################
# Name:			 Pref.py
# Purpose:	 Preference management
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-05-01
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

import copy
import string
from xml.dom import minidom

class Property(object):
	"""Structure for properties"""
	
	def __getValue(self):
		return self.__value
		
	def __setValue(self, value):
		if self.validator != None:
			valid, value = self.validator(value)
			if valid:
				self.__value = value
		else:
			self.__value = value
		if self.gui != None:
			self.gui.Changed()

	value = property(__getValue, __setValue)
	
	def __init__(self, value, validator = None, gui = None):
		object.__init__(self)
		self.validator = validator
		self.gui = gui(self) if gui != None else None
		self.value = value
	
		
class PropertyDef(object):
	"""Structure for property definitions"""
	def __init__(self, name, ptype, init = None, validator = None, gui = None):
		object.__init__(self)
		self.name = name
		self.ptype = ptype
		self.init = init
		self.validator = validator
		self.gui = gui


class XmlSerializer(object):
	def __init__(self):
		object.__init__(self)
		self.idn = 0
		self.dom = minidom.Document()
		self.ids = {}
		
	def RegisterId(self, p):
		self.idn += 1
		self.ids[p] = self.idn
		return str(self.idn)
		
	def GetId(self, p):
		return str(self.ids[p])
		
	def Serialize(self, p):
		self.dom.appendChild(p.XmlSerialize(self))
				
class XmlDeserializer(object):
	def __init__(self, dom, classes):
		object.__init__(self)
		self.dom = dom
		self.ids = {}
		self.classes = dict((c.__name__, c) for c in classes)
		
	def RegisterId(self, id, p):
		self.ids[id] = p
		
	def GetById(self, p):
		return self.ids[p]
		
	def Serialize(self, p):
		self.dom.appendChild(p.XmlSerialize(self))
		
	def GetClass(self, name):
		return self.classes[name]
		
	def Deserialize(self):
		l = []
		for el in self.dom.childNodes:
			l.append(Preferences.XmlDeserialize(self, el))
		return l
		
		
class NameNotFoundException(Exception):
	def __init__(self, arg):
		Exception.__init__(self, arg)


class Preferences(object):
	"""Class for structured property objects."""
	def __init__(self, parents = [], gui = None):
		self.__prefs = {}
		object.__init__(self)
		self.__parents = dict((x, x) for x in parents)
		self.__parentsByName = dict((x, x) for x in parents)
		self.__owner = None
		self.__CacheParents()
		self.__gui = gui
		for n, v in self.__GetAllPrefDef():
			f = v.init
			if f != None:
				self.__setattr__(n, f())
		
	prefDef = {}
	
	@classmethod
	def Register(cls, name, ptype, init = None, validator = None, gui = None):
		if not ('prefDef' in cls.__dict__):
			cls.prefDef = {}
		cls.prefDef[name] = PropertyDef(name, ptype, init, validator, gui)
		
	def __SetOwner(self, owner):
		self.__owner = owner
		self.__CacheParents()
		
	def __CacheParents(self):
		def Navigate(node, path):
			if node == None:
				return None
			if path == '..':
				return node.__owner
			if path in node.__prefs:
				return node.__prefs.value
			return None
		for n in self.__parentsByName:
			if type(n) == str:
				del self.__parents[self.__parentsByName[n]]
				val = reduce(Navigate, string.split(n, '/'), self)
				self.__parentsByName[n] = val
				self.__parents[val] = n		
		
	def __GetPrefByName(self, name):
		if name in self.__prefs:
			return self.__prefs[name]
		for p in self.__parents:
			try:
				return p.__GetPrefByName(name)
			except NameNotFoundException:
				pass
		raise NameNotFoundException(name)
	
	@classmethod
	def __GetPrefDefByName(cls, name):
		if name in cls.prefDef:
			return cls.prefDef[name]
		for b in cls.__bases__:
			try:
				return b.__GetPrefDefByName(name)
			except Exception:
				pass
		raise NameNotFoundException(name)
	
	def __getattr__(self, name):
		return self.__GetPrefByName(name).value
		
	def __setattr__(self, name, value):
		if name == '_Preferences__prefs':
			object.__setattr__(self, name, value)
			return
		try:
			pd = self.__GetPrefDefByName(name)
			assert isinstance(value, pd.ptype)
			if not name in self.__prefs:
				self.__prefs[name] = Property(value, pd.validator, pd.gui)
			else:
				self.__prefs[name].value = value
			if isinstance(value, Preferences):
				value.__SetOwner(self)
		except NameNotFoundException:
			object.__setattr__(self, name, value)
	
	def GetInherit(self, name):
		return not (name in self.__prefs)
		
	def SetInherit(self, name, inherit):
		if inherit:
			if name in self.__prefs:
				del self.__prefs[name]
		else:
			p = self.__GetPrefByName(name)
			self.__prefs[name] = Preferences.__DeepCopyPrefProp(p, None, self)
			
	def __GetAllPrefs(self):
		for n in self.__prefs:
			yield n, self.__prefs[n]
		for p in self.__parents:
			for n, v in p.__GetAllPrefs():
				yield n, v
	
	@classmethod
	def __GetAllPrefDef(cls):
		if 'prefDef' in cls.__dict__:	
			for n in cls.prefDef:
				yield n, cls.prefDef[n]
		for b in cls.__bases__:
			if isinstance(b, Preferences):
				for n, v in b.__GetAllPrefDef():
					yield n, v
	
	@staticmethod
	def __DeepCopyPrefProp(p, d, owner):
		q = Property(
			Preferences.__DeepCopyPref(p.value, d, owner) if isinstance(p.value, Preferences) else copy.deepcopy(p.value, d),
			copy.deepcopy(p.validator, d),
			copy.deepcopy(p.gui, d)
		)
		return q
	
	@staticmethod 
	def __DeepCopyPref(p, d, owner):
		c = Preferences(
			[pa for pa in p.__parentsByName],
			copy.deepcopy(p.__gui, d)
		)
		c.__owner = owner
		c.__CacheParents()
		for n in p.__prefs:
			c.__prefs[n] = Preferences.__DeepCopyPrefProp(p.__prefs[n], p)
		return c
		
	def XmlSerialize(self, xm):
		xd = xm.dom
		pref = xd.createElement("pref")
		pref.setAttribute("ptype", self.__class__.__name__)
		pref.setAttribute("id", xm.RegisterId(self))
		for n in self.__parentsByName:
			par = xd.createElement("parent")
			if type(n) == str:
				par.setAttribute("rel", n)
			else:
				par.setAttribute("id", xm.GetId(n))
			pref.appendChild(par)
		for n in self.__prefs:
			elem = xd.createElement("elem")
			elem.setAttribute("name", n)
			p = self.__prefs[n].value
			if isinstance(p, Preferences):
				elem.appendChild(p.XmlSerialize(xm))
			else:
				t = xd.createElement(type(p).__name__)
				t.appendChild(xd.createTextNode(str(p)))
				elem.appendChild(t)
			pref.appendChild(elem)
		return pref
		
	@staticmethod
	def XmlDeserialize(xm, pref):
		while pref.nodeName == '#text':
			pref = pref.nextSibling
		if pref.nodeName == 'pref':
			p = [c.getAttribute('rel') if c.hasAttribute('rel') else xm.GetById(c.getAttribute('id')) for c in pref.childNodes if c.nodeName == 'parent']
			c = xm.GetClass(pref.getAttribute('ptype'))
			assert issubclass(c, Preferences)
			pr = c(p)
			xm.RegisterId(pref.getAttribute('id'), pr)
			for c in pref.childNodes:
				if c.nodeName == 'elem':
					name = c.getAttribute('name')
					pr.__setattr__(name, pr.XmlDeserialize(xm, c.firstChild))
			return pr
		elif pref.nodeName == 'str':
			return str(pref.firstChild.nodeValue)
		elif pref.nodeName == 'int':
			return int(pref.firstChild.nodeValue)
			
			

