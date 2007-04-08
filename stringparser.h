/***************************************************************
 * Name:      stringparser.h
 * Purpose:   Facilitates generic parsing of strings
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
 #ifndef STRINGPARSER_H
#define STRINGPARSER_H

#include <wx/wx.h>

class StringParser {
  public:
    StringParser(wxString s): str(s), pos(0), len(s.Length()) {}
    
    bool NoMore();
    
    wxString FindAllBut(wxString forbidden);
    wxString AdvanceUntil(wxString target);
    wxChar Current();
    wxChar EatCurrent();
    
  protected:
    wxString str;
    int pos;
    int len;
  private:
};



#endif // STRINGPARSER_H
