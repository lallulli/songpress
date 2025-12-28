###############################################################
# Name:             MyNormalizeDialog.py
# Purpose:     Dialog to change notation
# Author:         Luca Allulli (webmaster@roma21.it)
# Created:     2013-07-14
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:     GNU GPL v2
##############################################################

from .NormalizeDialog import *
from .Transpose import *


class MyNormalizeDialog(NormalizeDialog):
    def __init__(self, parent, notations, text):
        NormalizeDialog.__init__(self, parent)
        self.notations = notations
        fn = autodetectNotation(text, notations)
        for n in self.notations:
            i = self.fromNotation.Append(n.desc)
            self.fromNotation.SetClientData(i, n)
            if n == fn:
                self.fromNotation.SetSelection(i)
        self.OnFromNotation(None)
        self.text = text
            
    def OnFromNotation(self, event):
        i = self.fromNotation.GetSelection()
        
    def NormalizeChords(self):
        return translateChordPro(
            self.text,
            self.fromNotation.GetClientData(self.fromNotation.GetSelection()),
            self.fromNotation.GetClientData(self.fromNotation.GetSelection()),
        )
