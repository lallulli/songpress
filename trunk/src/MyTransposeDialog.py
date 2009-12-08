###############################################################
# Name:			 MyTransposeDialog.py
# Purpose:	 Transposing services
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-12-02
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

from TransposeDialog import *

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
			
		
	def GetTransposed(text):
		return "pippo"
