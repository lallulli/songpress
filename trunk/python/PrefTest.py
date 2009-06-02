###############################################################
# Name:			 PrefTest.py
# Purpose:	 Test preference management module
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-05-30
# Copyright: Luca Allulli (http://www.roma21.it/songpress)
# License:	 GNU GPL v2
##############################################################

from Pref import *

def EtaValidator(eta):
	if eta < 0:
		return True, 0
	elif eta < 120:
		return True, eta
	else:
		return False, 0

class Persona(Preferences):
	def __init__(self, parents = [], gui = None):
		Preferences.__init__(self, parents, gui)	
	
Persona.Register("nome", str)
Persona.Register("cognome", str, lambda: "Allulli")
Persona.Register("eta", int, None, EtaValidator)

Persona.Register("figlio", Persona)
	
a = Persona()
a.nome = 'Luca'
a.figlio = Persona([a, '..'])

x = XmlManager()
x.Serialize(a)
print x.dom.toprettyxml()



