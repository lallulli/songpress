###############################################################################
# Name: dev_tool.py                                                           #
# Purpose: Provides logging and error tracking utilities                      #
# Original author: Cody Precord <cprecord@editra.org>                         #
# Modified by Luca Allulli (just minor adaptations)                           #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

""" Editra Development Tools
Tools and Utilities for debugging and helping with development of Editra.
@summary: Utility function for debugging the editor

"""
__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id: dev_tool.py 61794 2009-08-31 04:03:04Z CJP $"
__revision__ = "$Revision: 61794 $"

#-----------------------------------------------------------------------------#
# Imports
import os
import sys
import re
import platform
import traceback
import time
import urllib2
import webbrowser
import codecs
import locale
import wx

# Editra Libraries
#import ed_glob
#import ed_msg
#import eclib
#from ebmlib import IsUnicode
import errdlg
from Globals import glb

#-----------------------------------------------------------------------------#
# Globals

class EdErrorDialog(errdlg.ErrorDialog):
    def __init__(self, msg):
        errdlg.ErrorDialog.__init__(self, None, title="Error Report", message=msg)

        # Setup
        self.SetDescriptionLabel("Error: Something unexpected happend\n"
                                   "Help improve %s by clicking on "
                                   "Report Error\nto send the Error "
                                   "Traceback shown below." % (glb.PROG_NAME,))

    def Abort(self):
        """Abort the application"""
        sys.exit(1)

    def GetProgramName(self):
        """Get the program name to display in error report"""
        return "%s Version: %s" % (glb.PROG_NAME, glb.VERSION)

    def Send(self):
        """Send the error report"""
        msg = "mailto:%s?subject=Error Report&body=%s"
        addr = glb.BUG_REPORT_ADDRESS
        if wx.Platform != '__WXMAC__':
            body = urllib2.quote(self.err_msg)
        else:
            body = self.err_msg
        msg = msg % (addr, body)
        msg = msg.replace("'", '')
        webbrowser.open(msg)

#-----------------------------------------------------------------------------#

def ExceptionHook(exctype, value, trace):
    """Handler for all unhandled exceptions
    @param exctype: Exception Type
    @param value: Error Value
    @param trace: Trace back info

    """
    # Format the traceback
    exc = traceback.format_exception(exctype, value, trace)
    exc.insert(0, u"*** %s ***%s" % (errdlg.TimeStamp(), os.linesep))
    ftrace = u"".join(exc)

    # Ensure that error gets raised to console as well
    print ftrace

    # If abort has been set and we get here again do a more forcefull shutdown
    if EdErrorDialog.ABORT:
        os._exit(1)

    # Prevent multiple reporter dialogs from opening at once
    if not EdErrorDialog.REPORTER_ACTIVE and not EdErrorDialog.ABORT:
        dlg = EdErrorDialog(ftrace)
        dlg.ShowModal()
        dlg.Destroy()

#-----------------------------------------------------------------------------#
