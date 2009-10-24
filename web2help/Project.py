###############################################################
# Name:			 Project.py
# Purpose:	 Project properties
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-08-24
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

from Globals import *

class Project(object):
	def __init__(self):
		object.__init__(self)
		self.template = glb.AddPath('template/template.html')
		self.css = glb.AddPath('template/template.css')
		self.name = ""
		self.extractTitle = """return html.body.find("div", {'id': "main"}).h1.string"""
		self.extractContent = """h1 = html.body.find("div", {'id': "main"}).h1
return "".join([str(x) for x in h1.fetchNextSiblings()])"""
		