###############################################################
# Name:			 main.py
# Purpose:	 Entry point for Songpress
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-01-16
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

		
import wx
from wx import xrc
from wx.stc import *
from SDIMainFrame import *

class SongpressFrame(SDIMainFrame):

	def __init__(self, res):
		SDIMainFrame.__init__(self, res, 'MainFrame', 'Songpress - Il Canzonatore', 'Luca Allulli', 'song', 'crd')
		self.text = StyledTextCtrl(self.frame)
		self.frame.Bind(EVT_STC_MODIFIED, self.OnTextModified, self.text)
		font = wx.Font(
			12,
			wx.FONTFAMILY_DEFAULT,
			wx.FONTSTYLE_NORMAL,
			wx.FONTWEIGHT_NORMAL,
			faceName = "Times New Roman"
		)
		self.text.StyleSetFont(STC_STYLE_DEFAULT, font)

	def New(self):
		print("File->New");
		
	def Open(self):
		self.text.LoadFile(self.document)
		
	def Save(self):
		self.text.SaveFile(self.document)
		
	def OnTextModified(self, evt):
		self.SetModified()
	
	
	

class SongpressApp(wx.App):

	def OnInit(self):
		self.res = xrc.XmlResource('xrc/songpress.xrc')
		songpressFrame = SongpressFrame(self.res)
		
		return True





if __name__ == '__main__':
	songpressApp = SongpressApp()
	songpressApp.MainLoop()
