###############################################################
# Name:			 Project.py
# Purpose:	 Project properties
# Author:		 Luca Allulli (luca@skeed.it)
# Created:	 2009-08-24
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

from Globals import *
import xml.etree.ElementTree as ET


class Project(object):
	def __init__(self):
		object.__init__(self)
		self.template = glb.AddPath('template/template.html')
		self.css = glb.AddPath('template/template.css')
		self.name = ""
		self.extractTitle = """return html.body.find("div", {'id': "main"}).h1.string"""
		self.extractContent = """h1 = html.body.find("div", {'id': "main"}).h1
return h1.fetchNextSiblings()"""

	def Serialize(self):
		e = ET.Element('project')
		template = ET.SubElement(e, 'template')
		template.text = self.template
		css = ET.SubElement(e, 'css')
		css.text = self.css
		name = ET.SubElement(e, 'name')
		name.text = self.name
		extractTitle = ET.SubElement(e, 'extractTitle')
		extractTitle.text = self.extractTitle
		extractContent = ET.SubElement(e, 'extractContent')
		extractContent.text = self.extractContent
		return e
			
	def Unserialize(self, e):
		e = e.find('project')
		
		def get(name):
			v = e.find(name).text
			if v is None:
				return ""
			else:
				return v
	
		self.template = get('template')
		self.css = get('css')
		self.name = get('name')
		self.extractTitle = get('extractTitle')
		self.extractContent = get('extractContent')
