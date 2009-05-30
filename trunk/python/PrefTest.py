###############################################################
# Name:			 PrefTest.py
# Purpose:	 Test preference management module
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-05-30
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

from Pref import *


class Persona(Preferences):
	def __init__(self, parents = [], gui = None):
		Preferences.__init__(self, parents, gui)	
	
Persona.Register("nome", str)
#Register("figlio", Persona)
"""	
a = Persona()
a.nome = 'Luca'
a.figlio = Persona(['..'])
b = Persona(a)
"""

