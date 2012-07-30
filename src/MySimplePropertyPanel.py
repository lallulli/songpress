###############################################################
# Name:			 MySimplePropertyPanel.py
# Purpose:	 Panel to hold a single property setting
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2011-09-11
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import wx
from SimplePropertyPanel import SimplePropertyPanel
from CompositePropertyPanel import CompositePropertyPanel

class Widget(object):
	def __init__(self, parent, attrname, holder):
		object.__init__(self)
		self.holder = holder
		self.attrname = attrname
		self.Set(getattr(holder, attrname))
		self.Bind(wx.EVT_TEXT_ENTER, self.OnWidgetModified, self)
		self.Bind(wx.EVT_KILL_FOCUS, self.OnWidgetModified, self)
		self.holder.AddHandler(self.OnPropertyModified)
		
	def OnWidgetModified(self, evt):
		print "Modified!"
		try:
			setattr(self.holder, self.attrname, self.Get())
		except Exception, e:
			self.Set(getattr(self.holder, self.attrname))
		evt.Skip()
		
	def OnPropertyModified(self, h, name, value):
		print "Property %s modified to %s!" % (name, value)
		if name == self.attrname:
			self.Set(value)
			
	def Enable(self, value):
		pass
						
	def Set(self, value):
		pass
	
	def Get(self):
		return None

class ValueWidget(Widget):
	def Set(self, value):
		self.SetValue(value)
								
	def Get(self):
		return self.GetValue()
	

class StringWidget(ValueWidget, wx.TextCtrl):
	def __init__(self, parent, attrname, holder):
		wx.TextCtrl.__init__(self, parent)
		ValueWidget.__init__(self, parent, attrname, holder)
		
		
def ComboStringWidgetFactory(choices):
	class widget(ValueWidget, wx.ComboBox):
		def __init__(self, parent, attrname, holder):
			wx.ComboBox.__init__(self, parent, choices=choices)
			ValueWidget.__init__(self, parent, attrname, holder)
	return widget

class IntConverter(object):
	def Set(self, value):
		self.SetValue(str(value))
	def Get(self):
		return int(self.GetValue())
	
class FloatConverter(object):
	def Set(self, value):
		self.SetValue(str(value))
	def Get(self):
		return float(self.GetValue())

class NoneConverter(object):
	def Set(self, v):
		pass
	def OnWidgetModified(self, evt):
		evt.Skip()
		
class IntWidget(IntConverter, StringWidget):
	pass

def ComboIntWidgetFactory(choices):
	base = ComboStringWidgetFactory([str(c) for c in choices])
	class widget(IntConverter, base):
		pass
	return widget 

class FloatWidget(FloatConverter, StringWidget):
	pass
		
class NoneWidget(NoneConverter, StringWidget):
	pass


class MySimplePropertyPanel(SimplePropertyPanel):
	def __init__(self, parent, attrname, holder, widgets=None):
		"""
		attrname: name of the attribute
		holder: prototype-based object which holds properties
		widgets: prototype-based object which holds widgets and descriptions
		"""
		self.attrname = attrname
		self.holder = holder
		self.widgets = widgets
		try:
			w = getattr(widgets, attrname)['widget']
		except Exception, e:
			v = getattr(holder, attrname)
			if isinstance(v, str) or isinstance(v, unicode):
				w = StringWidget
			elif isinstance(v, int):
				w = IntWidget
			elif isinstance(v, float):
				w = FloatWidget
			else:
				w = NoneWidget
		try:
			d = getattr(widgets, attrname)['description']
		except Exception, e:
			d = attrname
		self.widget = w
		SimplePropertyPanel.__init__(self, parent)
		self.label.SetLabel(d)
		local = holder.Local(attrname)
		self.check.SetValue(not local)
		self.value.Enable(local)
		self.check.Enable(not holder.Source())
		
	def OnCheck(self, evt):
		if self.check.GetValue():
			# Inherit from parent
			delattr(self.holder, self.attrname)
		else:
			# Stop inheriting: copy value from parent
			setattr(self.holder, getattr(self.holder))
		evt.Skip()
	
		
	def get_widget(self):
		"""
		Create and return a widget for the SimplePropertyPanel under creation
		"""
		return self.widget(self, self.attrname, self.holder)
	
class MyCompositePropertyPanel(CompositePropertyPanel):
	"""
	def __init__(self, parent, attrname, holder, widgets=None):
	"""
	"""
	attrname: name of the attribute
	holder: prototype-based object which holds properties
	widgets: prototype-based object which holds widgets and descriptions
	"""
	pass
	"""
	self.attrname = attrname
	self.holder = holder
	self.widgets = widgets
	try:
		w = getattr(widgets, attrname)['widget']
	except Exception, e:
		v = getattr(holder, attrname)
		if isinstance(v, str) or isinstance(v, unicode):
			w = StringWidget
		elif isinstance(v, int):
			w = IntWidget
		elif isinstance(v, float):
			w = FloatWidget
		else:
			w = NoneWidget
	try:
		d = getattr(widgets, attrname)['description']
	except Exception, e:
		d = attrname
	self.widget = w
	SimplePropertyPanel.__init__(self, parent)
	self.label.SetLabel(d)
	local = holder.Local(attrname)
	self.check.SetValue(not local)
	self.value.Enable(local)
	self.check.Enable(not holder.Source())
	"""
		
	def OnCheck(self, evt):
		if self.check.GetValue():
			# Inherit from parent
			delattr(self.holder, self.attrname)
		else:
			# Stop inheriting: copy value from parent
			setattr(self.holder, getattr(self.holder))
		evt.Skip()
	
		
	def get_widget(self): #REMOVEME
		"""
		Create and return a widget for the SimplePropertyPanel under creation
		"""
		return self.widget(self, self.attrname, self.holder)
