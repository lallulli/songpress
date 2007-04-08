/***************************************************************
 * Name:      stringparser.cpp
 * Purpose:   Facilitates generic parsing of strings
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
 #include "stringparser.h"

bool StringParser::NoMore() {
  return pos==len;
}

wxString StringParser::FindAllBut(wxString forbidden) {
  int last = pos;
  int fl = forbidden.Length();
  bool out = false;
  while(!out && pos < len) {
    int i=0;
    while(i<fl && str[pos]!=forbidden[i])
      i++;
    out = (i < fl);
    if(!out) pos++;
  }
  return str.SubString(last, pos-1);
}

wxString StringParser::AdvanceUntil(wxString target) {
  int last = pos;
  int fl = target.Length();
  bool out = false;
  while(!out && pos < len) {
    int i=0;
    while(i<fl && str[pos]!=target[i])
      i++;
    out = (i == fl);
    if(!out) pos++;
  }
  return str.SubString(last, pos-1);
}

wxChar StringParser::Current() {
  return str[pos];
}

wxChar StringParser::EatCurrent() {
  return str[pos++];
}
