###############################################################
# Name:			 MyProperties.py
# Purpose:	 Project properties dialog
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-08-24
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

from Properties import *
from Project import *

class MyProperties(Properties):
	def __init__(self, parent, project):
		Properties.__init__(self, parent)
		self.project = project
		self.template.SetPath(project.template)
		self.css.SetPath(project.css)
		self.title.SetValue(project.extractTitle)
		self.content.SetValue(project.extractContent)
		self.name.SetPath(project.name)
	
	def OnOk(self, evt):
		p = self.project
		p.template = self.template.GetPath()
		p.css = self.css.GetPath()
		p.extractTitle = self.title.GetValue()
		p.extractContent = self.content.GetValue()
		p.name = self.name.GetPath()
		evt.Skip()
		