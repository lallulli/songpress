# -*- coding: utf-8 -*- 

from . import i18n

i18n.register('songpress.UpdateDialog')

# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class UpdateDialog
###########################################################################

class UpdateDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _("New updates are available"), pos = wx.DefaultPosition, size = wx.Size( 258,250 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer20 = wx.BoxSizer( wx.VERTICAL )
		
		self.updatesSizer = wx.BoxSizer(wx.VERTICAL)
		
		bSizer20.Add( self.updatesSizer, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.donate = wx.Button( self, wx.ID_ANY, _(">> Donate now! <<"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer20.Add( self.donate, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.SetSizer( bSizer20 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.donate.Bind( wx.EVT_BUTTON, self.OnDonate )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnDonate( self, event ):
		event.Skip()
	

