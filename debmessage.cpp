/***************************************************************
 * Name:      debmessage.cpp
 * Purpose:   Prints debug messages in a file
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
#include "debmessage.h"
#include <stdio.h>

#define DEBMESSAGEFILENAME ("output.txt")

FILE* debMsgFile = NULL;

void debMsgInit() {
  debMsgFile = fopen(DEBMESSAGEFILENAME, "w");
}

void debMsg(char* msg) {
  if(debMsgFile==NULL)
    debMsgInit();
  fprintf(debMsgFile, msg);
  fflush(debMsgFile);
}

void debMsg(wxString msg) {
  if(debMsgFile==NULL)
    debMsgInit();
  fprintf(debMsgFile, msg.mb_str(wxConvUTF8));
  fflush(debMsgFile);
}
