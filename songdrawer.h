/***************************************************************
 * Name:      songdrawer.h
 * Purpose:   Prints a song to a device contest
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
 #ifndef SONGDRAWER_H
#define SONGDRAWER_H

#include "textpreferences.h"
#include "Skcoda.h"

class SongTextBox {
public:
  wxCoord x;
  wxString text;
  wxFont font;
  bool isChord;
};

class SongDrawer {
public:
  SongDrawer(wxDC& dc, TextPreferences& tpref);
  ~SongDrawer();

  void SetTitle(const wxString& title); //To be called first
  void BeginVerse();
  void BeginChorus();
  void CommitLine();
  void AddWords(const wxString& text);
  void AddChord(const wxString& chord);
  void AddComment(const wxString& comment);
  void SetVerseNumber(int n) {nVerse=n-1; }
  void DrawBorder();

  wxCoord GetWidth() {return xMax; }
  wxCoord GetHeight() {return yMax; }

  void SetYStartSelection(wxCoord y) {yStartSelection=y; SelectionMinMax();}
  void SetYStopSelection(wxCoord y) {yStopSelection=y; SelectionMinMax();}
  void SetActiveSelection(bool b) {activeSelection=b; }
  void SetMetafileMode(bool m) {metafileMode=m; }

private:
  void ResetLine();
  void DrawVerseHeader(int n, wxCoord xRight, wxCoord yBottom, const wxFont&);
  void DrawChorusHeader(wxCoord xRight, wxCoord yBottom, const wxFont&);
  bool VerifySelectionIntersection(wxCoord y, wxCoord h);
  void SelectionMinMax();

  wxDC* dc;
  TextPreferences* tpref;

  wxCoord yBase;
  wxCoord heightChord;
  wxCoord heightText;
  wxCoord xChord;
  wxCoord xVerse;
  wxCoord xMax;
  wxCoord yOffset;
  wxCoord yMax;

  int nVerse;
  bool isChorus;
  bool somethingInBlock;
  bool isFirstLine;

  wxCoord yStartSelection;
  wxCoord yStopSelection;

  bool activeSelection;
  bool metafileMode;

  skCoda<SongTextBox> queue;
};

#endif // SONGDRAWER_H
