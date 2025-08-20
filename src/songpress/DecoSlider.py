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
## Class DecoSlider
###########################################################################

class DecoSlider ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )
		
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.slider = wx.Slider( self, wx.ID_ANY, 0, 0, 4, wx.DefaultPosition, wx.DefaultSize, wx.SL_AUTOTICKS|wx.SL_HORIZONTAL )
		bSizer9.Add( self.slider, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.panel.SetMinSize( wx.Size( -1,30 ) )
		
		bSizer9.Add( self.panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer9 )
		self.Layout()
		bSizer9.Fit( self )
		
		# Connect Events
		self.panel.Bind( wx.EVT_PAINT, self.OnPaint )
		self.panel.Bind( wx.EVT_SIZE, self.OnSize )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnPaint( self, event ):
		event.Skip()
	
	def OnSize( self, event ):
		event.Skip()
	

