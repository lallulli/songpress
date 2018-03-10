###############################################################
# Name:			 FormatPanel.py
# Purpose:	 Panel to hold all property settings
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2011-09-11
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

import wx
from MySimplePropertyPanel import MySimplePropertyPanel, MyCompositePropertyPanel
from Pref import Prototype

class FormatPanel(wx.Panel):
	def __init__(self, owner, holder, widgets):
		wx.Panel.__init__(self, owner.frame)
		self.owner = owner
		self.holder = holder
		self.widgets = widgets

		s = wx.BoxSizer( wx.VERTICAL )
		
		for n in holder:
			if isinstance(getattr(holder, n), Prototype):
				w = MyCompositePropertyPanel(self)#, n, holder, widgets)
			else:
				w = MySimplePropertyPanel(self, n, holder, widgets)
			s.Add(w, 0, wx.ALL | wx.EXPAND, 0)

		self.SetSizer(s)
		self.Layout()
		s.Fit(self)

