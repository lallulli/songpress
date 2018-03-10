###############################################################
# Name:			 MyNotationDialog.py
# Purpose:	 Dialog to change notation
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-12-09
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:	 GNU GPL v2
##############################################################

from NotationDialog import *
from Transpose import *

class MyNotationDialog(NotationDialog):
	def __init__(self, parent, notations, text):
		NotationDialog.__init__(self, parent)
		self.notations = notations
		fn = autodetectNotation(text, notations)
		for n in self.notations:
			i = self.fromNotation.Append(n.desc)
			self.fromNotation.SetClientData(i, n)
			if n == fn:
				self.fromNotation.SetSelection(i)
			i = self.toNotation.Append(n.desc)
			self.toNotation.SetClientData(i, n)
		self.toNotation.SetSelection(0)
		self.OnFromNotation(None)
		self.text = text
			
	def OnFromNotation(self, event):
		i = self.fromNotation.GetSelection()
		if self.toNotation.GetSelection() == i:
			self.toNotation.SetSelection(1 if i == 0 else 0) 
		
	def ChangeChordNotation(self):
		return translateChordPro(
			self.text,
			self.fromNotation.GetClientData(self.fromNotation.GetSelection()),
			self.toNotation.GetClientData(self.toNotation.GetSelection())
		)
