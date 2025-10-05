###############################################################
# Name:			 MyUpdateDialog.py
# Purpose:	 Dialog to select updates to apply
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2010-12-14
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

from xmlrpc.client import Server
import datetime
import platform
import traceback
import logging

import wx.lib.delayedresult as delayedresult
import wx

from .UpdateDialog import *
from .Globals import glb
from .MyUpdatePanel import MyUpdatePanel
from .proxiedxmlrpclib import RequestsTransport


from . import i18n


_ = wx.GetTranslation

def check_and_update(parent, preferences, force=False):
	"""
	Check for updates, and interact with user.
	
	Update mode is automatic if force=False, else manual.
	
	parent: parent window of any created modal dialogs
	"""
	def check_for_updates():
		"""
		Check and return available updates.
		
		Honour the frequency of update checking unless force is True.
		
		Return list of pair (version, description),
		where description is an html-formatted text.
		Raise an exception if anything goes wrong.
		"""
		if(
			force
			or preferences.updateLastCheck is None
			or datetime.datetime.now() > preferences.updateLastCheck + datetime.timedelta(days=preferences.updateFrequency)
		):
			tr = RequestsTransport()
			s = Server(preferences.updateUrl, transport=tr)
			# method returns a dictionary with those keys:
			# 'new_url': if defined, new url of the webservice
			# 'updates': list of 3-tuples (version, description, downloadUrl)
			u = s.checkForUpdates(
				glb.VERSION,
				preferences.updateFrequency,
				platform.system(),
				platform.architecture(),
				platform.platform(),
				platform.python_version(),
				wx.version(),
				i18n.getLang(),
			)
			u2 = [x for x in u['updates'] if x[0] not in preferences.ignoredUpdates]
			preferences.updateLastCheck = datetime.datetime.now()
			if 'new_url' in u:
				preferences.updateUrl = u['new_url']
			return u2
		return []

	def consume_updates(dr):
		try:
			u = dr.get()
			if len(u) > 0:
				d = MyUpdateDialog(parent, preferences, u)
				d.ShowModal()
			elif force:
				d = wx.MessageDialog(
					parent,
					_("Your version of Songpress is up to date."),
					_("Songpress"),
					wx.OK | wx.ICON_INFORMATION
				)
				d.ShowModal()
		except Exception as e:
			logging.error(traceback.format_exc())
			if force:
				d = wx.MessageDialog(
					parent,
					_("There was an error while checking for updates.\nPlease try again later."),
					_("Update error"),
					wx.OK | wx.ICON_ERROR
				)
				d.ShowModal()

	delayedresult.startWorker(consume_updates, check_for_updates)


class MyUpdateDialog(UpdateDialog):
	def __init__(self, parent, preferences, updates):
		UpdateDialog.__init__(self, parent)
		self.preferences = preferences
		self.updates = updates
		self.updatePanels = set()
		for u in updates:
			up = MyUpdatePanel(self, preferences, u[0], u[1], u[2])
			self.updatePanels.add(up)
			self.updatesSizer.Add(up, 1, wx.EXPAND, 5 )
		self.SetSize((400, 400))
		
	def RemoveChild(self, child):
		self.updatesSizer.Layout()
		self.updatePanels.remove(child)
		if len(self.updatePanels) == 0:
			self.Show(False)
			self.Destroy()
			
	def OnDonate(self, evt):
		wx.LaunchDefaultBrowser(_("https://www.skeed.it/songpress#donate"))
		evt.Skip()

