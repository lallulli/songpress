#!/usr/bin/env python

from UpdatePanel import UpdatePanel
import wx

class MyUpdatePanel(UpdatePanel):
	def __init__(self, parent, preferences, version, description, downloadUrl):
		UpdatePanel.__init__(self, parent)
		self.parent = parent
		self.preferences = preferences
		self.downloadUrl = downloadUrl
		self.v = version
		self.version.SetValue(version)
		self.new_features.SetPage(description)
		
	def __Hide(self):
		self.Show(False)
		self.parent.RemoveChild(self)
		
	def OnDownload(self, evt):
		wx.LaunchDefaultBrowser(self.downloadUrl)
		self.__Hide()
		evt.Skip()
		
	def OnSkip(self, evt):
		self.preferences.ignoredUpdates.add(self.v)
		self.__Hide()
		evt.Skip()
		
	def OnRemind(self, evt):
		self.__Hide()
		evt.Skip()

