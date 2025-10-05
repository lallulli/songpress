# -*- coding: utf-8 -*- 

import wx
import wx.html

_ = wx.GetTranslation


# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################


###########################################################################
## Class UpdatePanel
###########################################################################

class UpdatePanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )
		
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.AddGrowableRow( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, _("Version number"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		fgSizer1.Add( self.m_staticText12, 0, wx.ALL, 5 )
		
		self.version = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer1.Add( self.version, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, _("What's new"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		fgSizer1.Add( self.m_staticText13, 0, wx.ALL, 5 )
		
		self.new_features = wx.html.HtmlWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO )
		fgSizer1.Add( self.new_features, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer17.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer18.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.download = wx.Button( self, wx.ID_ANY, _("Download"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.download, 0, wx.ALL, 5 )
		
		self.remind = wx.Button( self, wx.ID_ANY, _("Remind later"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.remind, 0, wx.ALL, 5 )
		
		self.skip = wx.Button( self, wx.ID_ANY, _("Skip this version"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.skip, 0, wx.ALL, 5 )
		
		bSizer17.Add( bSizer18, 0, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer17 )
		self.Layout()
		bSizer17.Fit( self )
		
		# Connect Events
		self.download.Bind( wx.EVT_BUTTON, self.OnDownload )
		self.remind.Bind( wx.EVT_BUTTON, self.OnRemind )
		self.skip.Bind( wx.EVT_BUTTON, self.OnSkip )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnDownload( self, event ):
		event.Skip()
	
	def OnRemind( self, event ):
		event.Skip()
	
	def OnSkip( self, event ):
		event.Skip()
	

