###############################################################
# Name:			 Pref.py
# Purpose:	 Preference management
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-05-01
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

import copy
import string

class PrefProp(object):
	"""Structure for properties"""
	def __init__(self, value, validator, gui):
		object.__init__(self)
		self.value = value
		self.validator = validator
		self.gui = gui
			
class NameNotFoundException(Exception):
	def __init__(self, arg):
		Exception.__init__(self, arg)

class Pref(object):
	"""Class for structured property objects."""
	def __init__(self, parents = [], gui = None):
		self.__prefs = {}
		object.__init__(self)
		self.__parents = dict((x, x) for x in parents)
		self.__parentsByName = dict((x, x) for x in parents)
		self.__owner = None
		self.__CacheParents()
		self.__gui = gui
		
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
		
	def Register(self, name, value, validator = None, gui = None):
		self.__prefs[name] = PrefProp(value, validator, gui)
		if isinstance(value, Pref):
			value.__SetOwner(self)
		
	def __GetPrefByName(self, name):
		if name in self.__prefs:
			return self.__prefs[name]
		for p in self.__parents:
			try:
				return p.__GetPrefByName(name)
			except NameNotFoundException:
				pass
		raise NameNotFoundException(name)
	
	def __getattr__(self, name):
		return self.__GetPrefByName(name).value
		
	def __setattr__(self, name, value):
		if name != '_Pref__prefs' and name in self.__prefs:
			p = self.__prefs[name]
			if p.validator != None:
				valid, value = p.validator.Validate(value)
				if valid:
					p.value = value
			else:
				p.value = value
			if p.gui != None:
				p.gui.Changed()
		else:
			object.__setattr__(self, name, value)
	
	def GetInherit(self, name):
		return not (name in self.__prefs)
		
	def SetInherit(self, name, inherit):
		if inherit:
			if name in self.__prefs:
				del self.__prefs[name]
		else:
			p = self.__GetPrefByName(name)
			self.__prefs[name] = Pref.__DeepCopyPrefProp(p, None, self)
			
	def __GetAllPrefs(self):
		for n in self.__prefs:
			yield n, self.__prefs[n]
		for p in self.__parents:
			for n, v in p.__GetAllPrefs():
				yield n, v
	
	@staticmethod
	def __DeepCopyPrefProp(p, d, owner):
		q = PrefProp(
			Pref.__DeepCopyPref(p.value, d, owner) if isinstance(p.value, Pref) else copy.deepcopy(p.value, d),
			copy.deepcopy(p.validator, d),
			copy.deepcopy(p.gui, d)
		)
		return q
	
	@staticmethod 
	def __DeepCopyPref(p, d, owner):
		c = Pref(
			[pa for pa in p.__parentsByName],
			copy.deepcopy(p.__gui, d)
		)
		c.__owner = owner
		c.__CacheParents()
		for n in p.__prefs:
			c.__prefs[n] = Pref.__DeepCopyPrefProp(p.__prefs[n], p)
		return c

