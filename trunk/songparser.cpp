/***************************************************************
 * Name:      songparses.cpp
 * Purpose:   Parses a song, and drives a songdrawer
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/

#include "songparser.h"
#include "debmessage.h"

bool inSong=false;
bool inStrofa=false;
bool inChord=false;
bool inChorus=false;

void SongParser::ApriChord(wxString chord) {
  inChord=true;
  sd->AddChord(chord);
}

void SongParser::ChiudiChord() {
  /*
  if(inChord)
    printf("}");
  inChord=false;
  */
}

void SongParser::ApriStrofa() {
  if(!inStrofa)
    sd->BeginVerse();
  inStrofa=true;
}

void SongParser::ChiudiStrofa() {
  sd->CommitLine();
  ChiudiChord();
  /*
  if(inStrofa)
    sd->EndVerse();
  */
  inStrofa=false;
}

void SongParser::ApriChorus() {
  sd->CommitLine();
  ChiudiStrofa();
  if(!inChorus)
    sd->BeginChorus();
  inChorus=true;
}

void SongParser::ChiudiChorus() {
  ChiudiChord();
  /*
  if(inChorus)
    sd->EndChorus();
  */
  inChorus=false;
}

void SongParser::ApriSong(wxString title) {
  inSong=true;
  sd->SetTitle(title);
}

void SongParser::ChiudiSong() {
  ChiudiStrofa();
  ChiudiChorus();
  /*
  if(inSong)
    printf("\\end{song}\n");
  */
  inSong=false;
}

void SongParser::MangiaQuadra(FILE* f) {
  fscanf(f,"]");
}

void SongParser::MangiaGraffa(FILE* f) {
  fscanf(f,"}");
}

void SongParser::Parse(FILE* f) {
  char buffer[100000];
  bool esci=false;
  while(!esci) {
    int ris=fscanf(f,"%[^{[\n]", buffer);
    if(ris>=0) {
      if(ris==1) {
        if(!inChorus) ApriStrofa();
        sd->AddWords(wxString(buffer, wxConvLibc));
      }
      char c;
      fscanf(f,"%c", &c);
      if(c=='{') {
        fscanf(f,"%[^:}]", buffer);
        if(strcmp(buffer, "title")==0) {
          ChiudiSong();
          fscanf(f,":%[^}]", buffer);
          ApriSong(wxString(buffer, wxConvLibc));
        } else if(strcmp(buffer, "soc")==0) {
          ApriChorus();
        } else if(strcmp(buffer, "eoc")==0) {
          ChiudiChorus();
        } else if(strcmp(buffer, "c")==0) {
          ChiudiChord();
          if(!inChorus) ApriStrofa();
          fscanf(f,":%[^}]", buffer);
          sd->AddComment(wxString(buffer, wxConvLibc));
        } else if(strcmp(buffer, "verseNumber")==0) {
          fscanf(f, ":");
          int verseNumber;
          fscanf(f, "%d", &verseNumber);
          sd->SetVerseNumber(verseNumber);
        } else {
          fprintf(stderr, "Elemento '%s' non riconosciuto", buffer);
          return;
        }
        MangiaGraffa(f);
      } else if(c=='[') {
        if(!inChorus) ApriStrofa();
        ChiudiChord();
        fscanf(f,"%[^]]", buffer);
        ApriChord(wxString(buffer, wxConvLibc));
        MangiaQuadra(f);
      } else if(c=='\n') {
        ChiudiChord();
        int ris=fscanf(f,"%[\n]", buffer);
        if(ris>0)
          ChiudiStrofa();
        sd->CommitLine();
      } else {
        fprintf(stderr, "Carattere '%c' non riconosciuto", c);
        return;
      }
    } else
      esci=true;
  }
  ChiudiSong();
  sd->DrawBorder();
}

void SongParser::Parse(wxString s) {
  bool esci=false;
  wxString buffer;
  StringParser pars(s);
  while(!pars.NoMore()) {
    
    buffer = pars.FindAllBut(_T("[{\n"));
        
    if(buffer.Length()>0) {
      if(!inChorus) ApriStrofa();
      sd->AddWords(buffer);
    }
    else {
      wxChar c=pars.EatCurrent();
      if(c==_T('{')) {
        buffer = pars.FindAllBut(_T(":}"));
        if(buffer==_T("title")) {
          ChiudiSong();
          pars.EatCurrent();
          buffer=pars.FindAllBut(_T("}"));
          ApriSong(buffer);
        } else if(buffer==_T("soc")) {
          ApriChorus();
        } else if(buffer==_T("eoc")) {
          ChiudiChorus();
        } else if(buffer==_T("c")) {
          ChiudiChord();
          if(!inChorus) ApriStrofa();
          pars.EatCurrent();
          buffer = pars.FindAllBut(_T("}"));
          sd->AddComment(buffer);
        } else if(buffer==_T("verseNumber")) {
          pars.EatCurrent();
          long verseNumber;
          buffer = pars.FindAllBut(_T("}"));
          buffer.ToLong(&verseNumber);
          sd->SetVerseNumber((int) verseNumber);
        } else {
          fprintf(stderr, "Elemento non riconosciuto");
          return;
        }
        pars.EatCurrent();
      } else if(c==_T('[')) {
        if(!inChorus) ApriStrofa();
        ChiudiChord();
        buffer = pars.FindAllBut(_T("]"));
        ApriChord(buffer);
        pars.EatCurrent();
      } else if(c==_T('\n')) {
        ChiudiChord();
        if(pars.Current()==_T('\n')) {
          ChiudiStrofa();
          do {
            pars.EatCurrent();
          } while(pars.Current()==_T('\n'));
        }
        sd->CommitLine();
      } else {
        fprintf(stderr, "Carattere non riconosciuto");
        return;
      }
    }

  }
  ChiudiSong();
  sd->DrawBorder();
}


