/***************************************************************
 * Name:      songdrawer.cpp
 * Purpose:   Prints a song to a device contest
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/

 #include "songdrawer.h"

//public:

SongDrawer::SongDrawer(wxDC& dc, TextPreferences& tpref): dc(&dc), tpref(&tpref) {
  ResetLine();
  yBase=0;
  nVerse=0;
  isChorus=false;
  somethingInBlock=false;
  isFirstLine=true;
  xMax=0;
  yOffset=-1;
  yMax=0;
  activeSelection=false;
  metafileMode=false;
}

SongDrawer::~SongDrawer() {
  //dtor
}

void SongDrawer::SetTitle(const wxString& title) {
  dc->SetFont(tpref->GetTitle());
  wxCoord w, h, indent;
  dc->GetTextExtent(title, &w, &h);
  indent = tpref->GetTitleIndent();
  yBase += h + tpref->GetTitleBlockSeparator();
  if(VerifySelectionIntersection(0, h)) {
    yOffset = 0;
    dc->DrawText(title, indent, 0);
    yMax = yMax > yBase? yMax: yBase;
    xMax = xMax > indent + h? xMax: indent + h;
  }
}

void SongDrawer::AddWords(const wxString& t) {
  SongTextBox b;
  b.x=xVerse;
  b.isChord=false;
  b.text=t;
  wxCoord w, h;
  if(isChorus)
    b.font=tpref->GetChorus();
  else
    b.font=tpref->GetVerse();
  dc->SetFont(b.font);
  dc->GetTextExtent(t, &w, &h);
  xVerse+=w;
  heightText = heightText > h? heightText: h;
  queue.InCoda(b);
  somethingInBlock=true;
}

void SongDrawer::AddComment(const wxString& t) {
  SongTextBox b;
  b.x=xVerse;
  b.isChord=false;
  b.text=_T("(")+t+_T(")");
  wxCoord w, h;
  b.font=tpref->GetComment();
  dc->SetFont(b.font);
  dc->GetTextExtent(b.text, &w, &h);
  xVerse+=w;
  heightText = heightText > h? heightText: h;
  queue.InCoda(b);
  somethingInBlock=true;
}

void SongDrawer::AddChord(const wxString& t) {
  SongTextBox b;
  xVerse=(xChord > xVerse? xChord: xVerse);
  xChord=xVerse;
  b.x=xVerse;
  b.isChord=true;
  b.text=t;
  wxCoord w, h;
  b.font=tpref->GetChord();
  dc->SetFont(b.font);
  dc->GetTextExtent(t, &w, &h);
  xChord+=w;
  heightChord = heightChord > h? heightChord: h;
  queue.InCoda(b);
  somethingInBlock=true;
}

void SongDrawer::CommitLine() {
  if(!queue.EstVuota()) {
    wxCoord xBase;
    if(isChorus)
      xBase=tpref->GetChorusIndent();
    else
      xBase=tpref->GetVerseIndent();
    wxCoord yVerse=yBase+heightChord-5; //-5 aggiunto!
    while(!queue.EstVuota()) {
      SongTextBox b=queue.OutCoda();
      dc->SetFont(b.font);
      if(VerifySelectionIntersection(yBase, heightChord-5+heightText)) {
        yOffset = yOffset > -1 ? yOffset: yBase;
        dc->DrawText(b.text, b.x+xBase, (b.isChord? yBase: yVerse)-yOffset);
      }
    }
    //wxCoord yBaseOld=yBase;
    yBase=yVerse+heightText;
    if(VerifySelectionIntersection(yBase, heightChord-5+heightText)) {
      yMax=yMax>yBase? yMax: yBase;
      wxCoord xNew=(xChord>xVerse? xChord: xVerse)+xBase;
      xMax=xNew>xMax? xNew: xMax;
    }
    if(isFirstLine) {
      if(isChorus)
        DrawChorusHeader(xBase, yBase, tpref->GetChorusHeader());
      else
        DrawVerseHeader(nVerse, xBase, yBase, tpref->GetVerseHeader());
      isFirstLine=false;
    }
    ResetLine();
  }
}

void SongDrawer::BeginVerse() {
  if(somethingInBlock)
    yBase+=tpref->GetBlockSeparator();
  nVerse++;
  isChorus=false;
  somethingInBlock=false;
  isFirstLine=true;
}

void SongDrawer::BeginChorus() {
  if(somethingInBlock)
    yBase+=tpref->GetBlockSeparator();
  isChorus=true;
  somethingInBlock=false;
  isFirstLine=true;
}

void SongDrawer::DrawBorder() {
  dc->SetPen(wxPen(*wxBLACK, 0, wxTRANSPARENT));
  dc->SetBrush(wxBrush(*wxBLACK, wxTRANSPARENT));
  dc->DrawRectangle(0, 0, xMax, yMax-yOffset);
  dc->SetBrush(wxBrush(*wxBLUE));
  if(activeSelection && !metafileMode)
    dc->DrawRectangle(0, yStartSelection, 10, yStopSelection-yStartSelection);
}

//private:
void SongDrawer::ResetLine() {
  xVerse=0;
  xChord=0;
  heightText=0;
  heightChord=0;
}

void SongDrawer::DrawVerseHeader(int n, wxCoord xRight, wxCoord yBottom, const wxFont& font) {
  if(tpref->GetPrintVerseHeaders()) {
    xRight-=tpref->GetVerseHeaderSeparator();
    dc->SetFont(font);
    wxCoord w, h;
    wxString s;
    s.Printf(_T("%d"), n);
    dc->GetTextExtent(s, &w, &h);
    if(VerifySelectionIntersection(yBottom-h, h)) {
      if(tpref->GetUseDecorations()) {
        dc->SetBrush(*wxLIGHT_GREY_BRUSH);
        wxPen pen(*wxBLACK, 1);
        dc->SetPen(pen);
        dc->DrawRectangle(xRight-w-2, yBottom-h-1-yOffset, w+4, h+2);
        yMax = yBottom+2 > yMax? yBottom+2: yMax;
      }
      dc->DrawText(s, xRight-w, yBottom-h-yOffset);
    }
  }
}

void SongDrawer::DrawChorusHeader(wxCoord xRight, wxCoord yBottom, const wxFont& font)  {
  if(tpref->GetPrintChorusHeaders()) {
    xRight-=tpref->GetChorusHeaderSeparator();
    dc->SetFont(font);
    wxCoord w, h;
    wxString s=tpref->GetChorusHeaderText();
    dc->GetTextExtent(s, &w, &h);
      if(VerifySelectionIntersection(yBottom-h, h)) {
      dc->SetBrush(*wxBLACK_BRUSH);
      if(tpref->GetUseDecorations()) {
        wxPen pen(*wxBLACK, 1);
        dc->SetPen(pen);
        dc->DrawRectangle(xRight-w-2, yBottom-h-1-yOffset, w+4, h+2);
        dc->SetTextForeground(*wxWHITE);
        yMax = yBottom+2 > yMax? yBottom+2: yMax;
      }
      dc->DrawText(s, xRight-w, yBottom-h-yOffset);
      dc->SetTextForeground(*wxBLACK);
    }
  }
}

inline bool SongDrawer::VerifySelectionIntersection(wxCoord y, wxCoord h) {
  return
    !metafileMode
    || !activeSelection
    || !((y+h < yStartSelection) || (yStopSelection < y));
}

void SongDrawer::SelectionMinMax() {
  wxCoord min=yStartSelection < yStopSelection? yStartSelection: yStopSelection;
  wxCoord max=yStartSelection > yStopSelection? yStartSelection: yStopSelection;
  yStartSelection=min;
  yStopSelection=max;
}
