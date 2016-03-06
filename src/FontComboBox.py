###############################################################
# Name:			 FontComboBox.py
# Purpose:	 wxWidgets control providing a combo box font
#            selector
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-08-13
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

import wx

class MyFontEnumerator(wx.FontEnumerator):
	def OnFacename(self, name):
		if name[0] != '@':
			self.names.append(name)
		return True
		
	def Enumerate(self):
		self.names = []
		self.EnumerateFacenames()
		return self
		
	def AppendToComboBox(self, cb):
		#self.names.sort(key=lambda x: x.upper())
		cb.AppendItems(self.names)

class FontComboBox(wx.ComboBox):
	def __init__(self, parent, id=-1, defaultFont="Arial"):
		s = wx.Size()
		s.width = 200
		s.height = -1
		wx.ComboBox.__init__(self, parent, id, defaultFont, size=s, style=wx.CB_SORT)
		MyFontEnumerator().Enumerate().AppendToComboBox(self)
