# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Aug 25 2009)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class Properties
###########################################################################

class Properties ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__  ( self, parent, id = wx.ID_ANY, title = u"Project Properties", pos = wx.DefaultPosition, size = wx.Size( 500,400 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
		
		self.SetSizeHintsSz( wx.Size( 300,-1 ), wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Output file:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		bSizer22.Add( self.m_staticText12, 0, wx.ALL, 5 )
		
		self.name = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.chm", wx.DefaultPosition, wx.Size( -1,-1 ), wx.FLP_SAVE|wx.FLP_USE_TEXTCTRL )
		bSizer22.Add( self.name, 1, wx.ALL, 5 )
		
		bSizer1.Add( bSizer22, 0, wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Template:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer2.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.template = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.html", wx.DefaultPosition, wx.Size( -1,-1 ), wx.FLP_DEFAULT_STYLE )
		bSizer2.Add( self.template, 1, wx.ALL, 5 )
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
		
		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"CSS:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		bSizer21.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
		self.css = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.css", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer21.Add( self.css, 1, wx.ALL, 5 )
		
		bSizer1.Add( bSizer21, 0, wx.EXPAND, 5 )
		
		bSizer211 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText111 = wx.StaticText( self, wx.ID_ANY, u"Retrieve title:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )
		bSizer211.Add( self.m_staticText111, 0, wx.ALL, 5 )
		
		self.title = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,60 ), wx.TE_MULTILINE )
		bSizer211.Add( self.title, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer1.Add( bSizer211, 1, wx.EXPAND, 5 )
		
		bSizer2111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1111 = wx.StaticText( self, wx.ID_ANY, u"Retrieve content:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1111.Wrap( -1 )
		bSizer2111.Add( self.m_staticText1111, 0, wx.ALL, 5 )
		
		self.content = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,60 ), wx.TE_MULTILINE )
		bSizer2111.Add( self.content, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer1.Add( bSizer2111, 1, wx.EXPAND, 5 )
		
		bSizer221 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer221.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.ok = wx.Button( self, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer221.Add( self.ok, 0, wx.ALL, 5 )
		
		self.cancel = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer221.Add( self.cancel, 0, wx.ALL, 5 )
		
		bSizer1.Add( bSizer221, 0, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.ok.Bind( wx.EVT_BUTTON, self.OnOk )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnOk( self, event ):
		event.Skip()
	

