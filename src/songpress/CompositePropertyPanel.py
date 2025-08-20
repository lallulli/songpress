# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

import gettext
_ = gettext.gettext

###########################################################################
## Class CompositePropertyPanel
###########################################################################

class CompositePropertyPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )
		
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer24 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer24.Add( self.m_bitmap1, 0, wx.ALL, 5 )
		
		self.label = wx.StaticText( self, wx.ID_ANY, _("label"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label.Wrap( -1 )
		bSizer24.Add( self.label, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.check = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.check.SetValue(True) 
		bSizer24.Add( self.check, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		bSizer21.Add( bSizer24, 0, wx.EXPAND, 5 )
		
		"""
		self.value = self.get_widget()
		bSizer21.Add( self.value, 1, wx.ALIGN_CENTER|wx.BOTTOM|wx.EXPAND|wx.LEFT|wx.TOP, 5 )
		"""
		
		self.SetSizer( bSizer21 )
		self.Layout()
		bSizer21.Fit( self )
		
		# Connect Events
		self.check.Bind( wx.EVT_CHECKBOX, self.OnCheck )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnCheck( self, event ):
		event.Skip()
	

