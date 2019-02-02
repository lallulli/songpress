###############################################################
# Name:			 MyListDialog.py
# Purpose:	 Generic dialog box asking for an item in a list
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2019-02-02
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

import wx
from ListDialog import ListDialog


class MyListDialog(ListDialog):
	def __init__(self, parent, message, title, elements):
		"""
		Show a dialog box asking to select an item from a list

		:param message: message to be displayed
		:param title: dialog title
		:param elements: list of strings: items to be chosen from
		"""
		super().__init__(parent)
		self.SetTitle(title)
		self.label.SetLabel(message)
		self.elements_list = elements
		self.elements.InsertItems(elements, 0)

	def GetSelectedIndex(self):
		return self.elements.GetSelection()

	def GetSelectedString(self):
		return self.elements_list[self.elements.GetSelection()]

