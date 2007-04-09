/***************************************************************
 * Name:      tela.cpp
 * Purpose:   Scrolled component where song preview is drawed
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
#include "tela.h"
#include "textpreferences.h"
#include "songdrawer.h"
#include "songparser.h"
#include <wx/strconv.h>

BEGIN_EVENT_TABLE(Tela, wxScrolledWindow)
  EVT_LEFT_DOWN(Tela::OnLeftButtonDown)
  EVT_LEFT_UP(Tela::OnLeftButtonUp)
  EVT_MOTION(Tela::OnMouseMove)
END_EVENT_TABLE()


Tela::Tela(wxWindow* parent,wxWindowID id):
  wxScrolledWindow(parent, id)	{
  SetVirtualSize(0, 0);
  SetScrollRate(10, 10);
  EnableScrolling(true, true);
  SetSize(200, 200);
  mouseMoving=false;
  mouseDragged=false;
}

Tela::~Tela()
{
}

void Tela::Disegna(wxDC& dc, bool metafile) {
  if(!song.IsEmpty()) {
    wxFont strofa (
      10,
      wxFONTFAMILY_MODERN,
      wxFONTSTYLE_NORMAL,
      wxFONTWEIGHT_NORMAL,
      false,
      _T("Comic Sans MS")
      //_T("Times New Roman")
    );
    wxFont accordi (
      9,
      wxFONTFAMILY_MODERN,
      wxFONTSTYLE_SLANT,
      wxFONTWEIGHT_NORMAL,
      false,
      _T("Comic Sans MS")
      //_T("Times New Roman")
    );
    wxFont commenti (
      10,
      wxFONTFAMILY_MODERN,
      wxFONTSTYLE_SLANT,
      wxFONTWEIGHT_NORMAL,
      false,
      _T("Comic Sans MS")
      //_T("Times New Roman")
    );
    wxFont ritornello(
      10,
      wxFONTFAMILY_MODERN,
      wxFONTSTYLE_NORMAL,
      wxFONTWEIGHT_BOLD,
      false,
      _T("Comic Sans MS")
      //_T("Times New Roman")
    );
    wxFont titolo(
      10,
      wxFONTFAMILY_MODERN,
      wxFONTSTYLE_SLANT,
      wxFONTWEIGHT_BOLD,
      true,
      _T("Comic Sans MS")
      //_T("Times New Roman")
    );

    TextPreferences t;
    t.SetChord(accordi);
    t.SetVerse(strofa);
    t.SetVerseHeader(strofa);
    t.SetChorus(ritornello);
    t.SetChorusHeader(ritornello);
    t.SetComment(commenti);
    t.SetTitle(titolo);
    t.SetVerseIndent(30);
    t.SetChorusIndent(42);
    t.SetBlockSeparator(30);
    t.SetVerseHeaderSeparator(10);
    t.SetChorusHeaderSeparator(10);
    t.SetTitleIndent(30);
    t.SetTitleBlockSeparator(10);
    t.SetChorusHeaderText(_T("Rit"));
    SongDrawer sd(dc, t);
    sd.SetActiveSelection(true);
    sd.SetYStartSelection(yStart);
    sd.SetYStopSelection(yStop);
    sd.SetActiveSelection(mouseDragged);
    sd.SetMetafileMode(metafile);
    SongParser sp(sd);
    sp.Parse(song);
    SetVirtualSize(sd.GetWidth(), sd.GetHeight());
    
    /*
    TiXmlDocument doc;
    TiXmlDeclaration* dec = new TiXmlDeclaration("1.0", "", "");
    doc.LinkEndChild(dec);
    TiXmlElement* el = new TiXmlElement("Preferences");
    doc.LinkEndChild(el);
    t.Serialize(el);
    doc.SaveFile("pippo.xml");    
    */
    
  }
}

//private:

void Tela::OnDraw(wxDC& dc) {
  Disegna(dc, false);
}

void Tela::OnLeftButtonDown(wxMouseEvent& e) {
  wxCoord x, y, xu, yu;
  GetViewStart(&x, &y);
  GetScrollPixelsPerUnit(&xu, &yu);
  yStart=e.GetY() + y*yu;
  mouseMoving=true;
  mouseDragged=true;
}

void Tela::OnLeftButtonUp(wxMouseEvent& e) {
  wxCoord x, y, xu, yu;
  GetViewStart(&x, &y);
  GetScrollPixelsPerUnit(&xu, &yu);
  yStop=e.GetY() + y*yu;
  mouseMoving=false;
  EndDragging();
  Refresh();
}

void Tela::OnMouseMove(wxMouseEvent& e) {
  if(mouseMoving) {
    if(e.LeftIsDown()) {
      wxCoord x, y, xu, yu;
      GetViewStart(&x, &y);
      GetScrollPixelsPerUnit(&xu, &yu);
      yStop=e.GetY() + y*yu;
    } else {
      mouseMoving=false;
      EndDragging();
    }
    Refresh();
  }
}

inline void Tela::EndDragging() {
  int diff=yStop-yStart;
  diff=(diff>0)? diff: -diff;
  mouseDragged=(diff >= EPSILON_DRAG);
}
