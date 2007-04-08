/***************************************************************
 * Name:      songparses.h
 * Purpose:   Parses a song, and drives a songdrawer
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
 #ifndef SONGPARSER_H
#define SONGPARSER_H

#include <wx/wx.h>

#include "songdrawer.h"
#include "stringparser.h"

class SongParser
{
public:
  SongParser(SongDrawer& d): sd(&d) {}
  void Parse(FILE* f);
  void Parse(wxString s);


private:
  void ApriChord(wxString chord);
  void ChiudiChord();
  void ApriStrofa();
  void ChiudiStrofa() ;
  void ApriChorus();
  void ChiudiChorus();
  void ApriSong(wxString title);
  void ChiudiSong();
  void MangiaQuadra(FILE* f);
  void MangiaGraffa(FILE* f);
  SongDrawer* sd;
};

#endif // SONGPARSER_H
