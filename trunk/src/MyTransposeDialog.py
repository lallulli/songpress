###############################################################
# Name:			 MyTransposeDialog.py
# Purpose:	 Transposing dialog
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-12-02
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

from TransposeDialog import *
from Transpose import *

class MyTransposeDialog(TransposeDialog):
	def __init__(self, parent, notations, notation=None, key=None):
		TransposeDialog.__init__(self, parent)
		self.notations = notations
		self.key = key
		for n in self.notations:
			i = self.notation.Append(n.desc)
			self.notation.SetClientData(i, n)
			if n == notation:
				self.notation.SetSelection(i)
			
	def OnNotation(self, event):
		i = self.notation.GetSelection()
		n = self.notation.GetClientData(i)
		self.fromKey.Clear()
		self.toKey.Clear()
		for k in orderedKeys:
			kn = "%s / %s" % (
				translateChord(k, dNotation=n),
				translateChord(scales[k][1][5] + "m", dNotation=n),
			)
			i = self.fromKey.Append(kn)
			self.fromKey.SetClientData(i, k)
			i = self.toKey.Append(kn)
			self.toKey.SetClientData(i, k)
		event.Skip()
		
	def GetTransposed(self, text):
		return transposeChordPro(
			self.fromKey.GetClientData(self.fromKey.GetSelection()),
			self.toKey.GetClientData(self.toKey.GetSelection()),
			text,
			self.notation.GetClientData(self.notation.GetSelection())
		)
