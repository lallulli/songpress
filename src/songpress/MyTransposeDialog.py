###############################################################
# Name:             MyTransposeDialog.py
# Purpose:     Transposing dialog
# Author:         Luca Allulli (webmaster@roma21.it)
# Created:     2009-12-02
# Copyright: Luca Allulli (https://www.skeed.it/songpress)
# License:     GNU GPL v2
##############################################################

from .TransposeDialog import *
from .Transpose import *


class MyTransposeDialog(TransposeDialog):
    def __init__(self, parent, notations, text):
        TransposeDialog.__init__(self, parent)
        self.notations = notations
        self.text = text
        fn = autodetectNotation(text, notations)
        self.fk = autodetectKey(text, fn)
        for n in self.notations:
            i = self.notation.Append(n.desc)
            self.notation.SetClientData(i, n)
            if n == fn:
                self.notation.SetSelection(i)
        self.OnNotation()
            
    def OnNotation(self, event=None):
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
            if chord2pos(self.fk) == chord2pos(k):
                self.fromKey.SetSelection(i)
            i = self.toKey.Append(kn)
            self.toKey.SetClientData(i, k)
        self.UpdateToKey()
        if event is not None:
            event.Skip()
            
    def UpdateToKey(self):
        try:
            s = int(self.semitones.GetValue())
        except:
            return
        self.toKey.SetSelection((self.fromKey.GetSelection() + s) % 12)
        
    def GetTransposed(self):
        return transposeChordPro(
            self.fromKey.GetClientData(self.fromKey.GetSelection()),
            self.toKey.GetClientData(self.toKey.GetSelection()),
            self.text,
            self.notation.GetClientData(self.notation.GetSelection())
        )
        
    def OnSemitones(self, evt):
        self.UpdateToKey()
        evt.Skip()
        
    def OnFromKey(self, evt):
        self.UpdateToKey()
        evt.Skip()
        
    def OnToKey(self, evt):
        g = (self.toKey.GetSelection() - self.fromKey.GetSelection()) % 12
        if g > 7:
            g = -12 + g
        self.semitones.SetValue(g)
        evt.Skip()
