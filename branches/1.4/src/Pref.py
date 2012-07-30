###############################################################
# Name:			 Pref.py
# Purpose:	 Preference management
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-05-01
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import copy
import string

def Monitored(C):
	class MC(C):
		def __init__(self, *args, **kwargs):
			C.__init__(self, *args, **kwargs)
			C.__setattr__(self, 'am_handlers', [])
			
		def __setattr__(self, name, value):
			C.__setattr__(self, name, value)
			if name != 'am_handlers':
				try:
					for h in self.am_handlers:
						h(self, name, value)
				except AttributeError:
					# am_handler does not exist. This occurs during init
					pass
	
		def AddHandler(self, handler):
			self.am_handlers.append(handler)

	return MC


@Monitored
class Prototype(object):
	def __init__(self, parents=[]):
		if not isinstance(parents, list):
			if parents is None:
				parents = []
			else:
				parents = [parents]
		object.__init__(self)
		self.__parents = parents
		for p in parents:
			p.AddHandler(self.OnParentFieldChanged)
		
	def __setattr__(self, name, value):
		object.__setattr__(self, name, value)
		
	def __getattribute__(self, name):
		try:
			return object.__getattribute__(self, name)
		except AttributeError:
			for p in self.__parents:
				try:
					return p.__getattribute__(name)
				except AttributeError:
					pass
		raise AttributeError(name)
	
	def __collect_attributes(self):
		a = set()
		for p in self.__parents:
			a.update(p.__collect_attributes())
		for n in self.__dict__:
			if n != 'am_handlers' and n[0] != '_':
				a.add(n)
		return a
	
	def Local(self, name):
		"""Return True iff attribute name is local, i.e. not inherited"""
		return name in self.__dict__
	
	def Source(self):
		"""Return True iff object has no parents"""
		return len(self.__parents) == 0
	
	def __iter__(self):
		for p in self.__collect_attributes():
			yield p
	
	def OnParentFieldChanged(self, obj, name, value):
		# called by parents if their fields change
		for h in self.am_handlers:
			h(self, name, value)