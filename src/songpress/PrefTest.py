###############################################################
# Name:             PrefTest.py
# Purpose:     Test preference management module
# Author:         Luca Allulli (webmaster@roma21.it)
# Created:     2009-05-30
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:     GNU GPL v2
##############################################################

from xml.dom import minidom

from .Pref import *


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

x = XmlSerializer()
x.Serialize(a)

#Patch
def newwritexml(self, writer, indent= '', addindent= '', newl= ''):
    if len(self.childNodes)==1 and self.firstChild.nodeType==3:
        writer.write(indent)
        self.oldwritexml(writer) # cancel extra whitespace
        writer.write(newl)
    else:
        self.oldwritexml(writer, indent, addindent, newl)

if not ('oldwritexml' in minidom.Element.__dict__):
    minidom.Element.oldwritexml = minidom.Element.writexml
    minidom.Element.writexml = newwritexml
#End patch

#print x.dom.toprettyxml()

xml = """<?xml version="1.0" ?>
<pref id="1" ptype="Persona">
        <elem name="figlio">
                <pref id="2" ptype="Persona">
                        <parent id="1"/>
                        <elem name="cognome">
                                <str>Allulli</str>
                        </elem>
                </pref>
        </elem>
        <elem name="cognome">
                <str>Allulli</str>
        </elem>
        <elem name="nome">
                <str>Luca</str>
        </elem>
        <elem name="eta">
                <int>30</int>
        </elem>
</pref>
"""

xp = minidom.parseString(xml)

y = XmlDeserializer(xp, [Persona, Preferences])
k = y.Deserialize()
