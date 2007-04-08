/***************************************************************
 * Name:      debmessage.h
 * Purpose:   Prints debug messages in a file
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
#ifndef DEBMESSAGE_H
#define DEBMESSAGE_H

#include <wx/wx.h>

void debMsg(char* msg);
void debMsg(wxString msg);


#endif // DEBMESSAGE_H
