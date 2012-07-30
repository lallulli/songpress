# -*- coding: utf-8 -*-

import i18n
i18n.register('PreferencesDialog')

# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
from FontComboBox import FontComboBox
import Editor

###########################################################################
## Class PreferencesDialog
###########################################################################

class PreferencesDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _("Songpress options"), pos = wx.DefaultPosition, size = wx.Size( 535,410 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.general = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.label1 = wx.StaticText( self.general, wx.ID_ANY, _("Editor font"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label1.Wrap( -1 )
		bSizer12.Add( self.label1, 0, wx.ALL, 5 )
		
		self.fontCB = FontComboBox(self.general, wx.ID_ANY, self.pref.editorFace)
		bSizer12.Add( self.fontCB, 1, wx.ALL, 5 )
		
		self.m_staticText8 = wx.StaticText( self.general, wx.ID_ANY, _("Size"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer12.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		sizeCBChoices = [ _("7"), _("8"), _("9"), _("10"), _("11"), _("12"), _("13"), _("14"), _("16"), _("18"), _("20") ]
		self.sizeCB = wx.ComboBox( self.general, wx.ID_ANY, _("12"), wx.DefaultPosition, wx.DefaultSize, sizeCBChoices, 0 )
		bSizer12.Add( self.sizeCB, 0, wx.ALL, 5 )
		
		bSizer11.Add( bSizer12, 0, wx.EXPAND, 5 )
		
		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText9 = wx.StaticText( self.general, wx.ID_ANY, _("Preview"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		bSizer13.Add( self.m_staticText9, 0, wx.ALL, 5 )
		
		self.editor = Editor.Editor(self.general, False, self.general)
		bSizer13.Add( self.editor, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer11.Add( bSizer13, 1, wx.EXPAND, 5 )
		
		bSizer141 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText101 = wx.StaticText( self.general, wx.ID_ANY, _("Default notation"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText101.Wrap( -1 )
		bSizer141.Add( self.m_staticText101, 0, wx.ALL, 5 )
		
		notationChChoices = []
		self.notationCh = wx.Choice( self.general, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, notationChChoices, 0 )
		self.notationCh.SetSelection( 0 )
		bSizer141.Add( self.notationCh, 1, wx.ALL, 5 )
		
		bSizer11.Add( bSizer141, 0, wx.EXPAND, 5 )
		
		bSizer1411 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1011 = wx.StaticText( self.general, wx.ID_ANY, _("Check for updates every"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1011.Wrap( -1 )
		bSizer1411.Add( self.m_staticText1011, 0, wx.ALL, 5 )
		
		frequencyChoices = []
		self.frequency = wx.Choice( self.general, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, frequencyChoices, 0 )
		self.frequency.SetSelection( 0 )
		bSizer1411.Add( self.frequency, 1, wx.ALL, 5 )
		
		bSizer11.Add( bSizer1411, 0, wx.EXPAND, 5 )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText10 = wx.StaticText( self.general, wx.ID_ANY, _("Language"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		bSizer14.Add( self.m_staticText10, 0, wx.ALL, 5 )
		
		langChChoices = []
		self.langCh = wx.Choice( self.general, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, langChChoices, 0 )
		self.langCh.SetSelection( 0 )
		bSizer14.Add( self.langCh, 1, wx.ALL, 5 )
		
		bSizer11.Add( bSizer14, 0, wx.EXPAND, 5 )
		
		self.general.SetSizer( bSizer11 )
		self.general.Layout()
		bSizer11.Fit( self.general )
		self.notebook.AddPage( self.general, _("General"), True )
		self.autoAdjust = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		self.autoRemoveBlankLines = wx.CheckBox( self.autoAdjust, wx.ID_ANY, _("Offer to remove blank lines"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.autoRemoveBlankLines, 0, wx.ALL, 5 )
		
		self.autoTab2Chordpro = wx.CheckBox( self.autoAdjust, wx.ID_ANY, _("Offer to convert songs in tab"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.autoTab2Chordpro, 0, wx.ALL, 5 )
		
		self.autoAdjustEasyKey = wx.CheckBox( self.autoAdjust, wx.ID_ANY, _("Offer to transpose songs to simplify chords"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.autoAdjustEasyKey, 0, wx.ALL, 5 )
		
		self.simplifyPanel = wx.ScrolledWindow( self.autoAdjust, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.SUNKEN_BORDER|wx.VSCROLL )
		self.simplifyPanel.SetScrollRate( 5, 5 )
		self.simplifyPanel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer18.Add( self.simplifyPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.autoAdjust.SetSizer( bSizer18 )
		self.autoAdjust.Layout()
		bSizer18.Fit( self.autoAdjust )
		self.notebook.AddPage( self.autoAdjust, _("AutoAdjust"), False )
		
		bSizer10.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		m_sdbSizer3 = wx.StdDialogButtonSizer()
		self.m_sdbSizer3OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer3.AddButton( self.m_sdbSizer3OK )
		self.m_sdbSizer3Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer3.AddButton( self.m_sdbSizer3Cancel )
		m_sdbSizer3.Realize();
		bSizer10.Add( m_sdbSizer3, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.SetSizer( bSizer10 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.fontCB.Bind( wx.EVT_KILL_FOCUS, self.OnFontSelected )
		self.sizeCB.Bind( wx.EVT_COMBOBOX, self.OnFontSelected )
		self.sizeCB.Bind( wx.EVT_KILL_FOCUS, self.OnFontSelected )
		self.sizeCB.Bind( wx.EVT_TEXT_ENTER, self.OnFontSelected )
		self.m_sdbSizer3OK.Bind( wx.EVT_BUTTON, self.OnOk )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnFontSelected( self, event ):
		event.Skip()
	
	
	
	
	def OnOk( self, event ):
		event.Skip()
	

