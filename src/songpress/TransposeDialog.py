# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Aug 25 2009)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx


_ = wx.GetTranslation


###########################################################################
## Class TransposeDialog
###########################################################################

class TransposeDialog ( wx.Dialog ):
    
    def __init__( self, parent ):
        wx.Dialog.__init__  ( self, parent, id = wx.ID_ANY, title = _(u"Transpose"), pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.label1 = wx.StaticText( self, wx.ID_ANY, _(u"Chord notation:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label1.Wrap( -1 )
        bSizer2.Add( self.label1, 0, wx.ALL, 5 )
        
        notationChoices = []
        self.notation = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, notationChoices, 0 )
        self.notation.SetSelection( 0 )
        bSizer2.Add( self.notation, 1, wx.ALL, 5 )
        
        bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
        
        bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.label11 = wx.StaticText( self, wx.ID_ANY, _(u"From key:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label11.Wrap( -1 )
        bSizer21.Add( self.label11, 0, wx.ALL, 5 )
        
        fromKeyChoices = []
        self.fromKey = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, fromKeyChoices, 0 )
        self.fromKey.SetSelection( 0 )
        bSizer21.Add( self.fromKey, 1, wx.ALL, 5 )
        
        bSizer1.Add( bSizer21, 1, wx.EXPAND, 5 )
        
        bSizer2111 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.label1111 = wx.StaticText( self, wx.ID_ANY, _(u"Semitones:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label1111.Wrap( -1 )
        bSizer2111.Add( self.label1111, 0, wx.ALL, 5 )
        
        self.semitones = wx.SpinCtrl( self, wx.ID_ANY, u"2", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS|wx.SP_WRAP, -11, 12, 2 )
        bSizer2111.Add( self.semitones, 1, wx.ALL, 5 )
        
        bSizer1.Add( bSizer2111, 1, wx.EXPAND, 5 )
        
        bSizer211 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.label111 = wx.StaticText( self, wx.ID_ANY, _(u"To key:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label111.Wrap( -1 )
        bSizer211.Add( self.label111, 0, wx.ALL, 5 )
        
        toKeyChoices = []
        self.toKey = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, toKeyChoices, 0 )
        self.toKey.SetSelection( 0 )
        bSizer211.Add( self.toKey, 1, wx.ALL, 5 )
        
        bSizer1.Add( bSizer211, 1, wx.EXPAND, 5 )
        
        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
        m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
        self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
        m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
        m_sdbSizer1.Realize();
        bSizer1.Add( m_sdbSizer1, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.SetSizer( bSizer1 )
        self.Layout()
        bSizer1.Fit( self )
        
        # Connect Events
        self.notation.Bind( wx.EVT_CHOICE, self.OnNotation )
        self.fromKey.Bind( wx.EVT_CHOICE, self.OnFromKey )
        self.semitones.Bind( wx.EVT_SPINCTRL, self.OnSemitones )
        self.toKey.Bind( wx.EVT_CHOICE, self.OnToKey )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def OnNotation( self, event ):
        event.Skip()
    
    def OnFromKey( self, event ):
        event.Skip()
    
    def OnSemitones( self, event ):
        event.Skip()
    
    def OnToKey( self, event ):
        event.Skip()
    

