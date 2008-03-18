/***************************************************************
 * Name:      textpreferences.h
 * Purpose:   Contains preferences regarding font style
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/

#ifndef TEXTPREFERENCES_H
#define TEXTPREFERENCES_H

#include <wx/font.h>
#include <wx/dc.h>
#include "tinyxml/tinyxml.h"

class TextPreferences {
public:
  TextPreferences();
  ~TextPreferences();

  void SetVerse(const wxFont& f) {verse=f; }
  void SetChord(const wxFont& f) {chord=f; }
  void SetComment(const wxFont& f) {comment=f; }
  void SetChorus(const wxFont& f) {chorus=f; }
  void SetTitle(const wxFont& f) {title=f; }
  void SetVerseHeader(const wxFont& f) {verseHeader=f; }
  void SetChorusHeader(const wxFont& f) {chorusHeader=f; }
  void SetVerseIndent(wxCoord x) {verseIndent=x; }
  void SetChorusIndent(wxCoord x) {chorusIndent=x; }
  void SetBlockSeparator(wxCoord h) {blockSeparator=h; }
  void SetVerseHeaderSeparator(wxCoord w) {verseHeaderSeparator=w; }
  void SetChorusHeaderSeparator(wxCoord w) {chorusHeaderSeparator=w; }
  void SetTitleIndent(wxCoord w) {titleIndent=w; }
  void SetTitleBlockSeparator(wxCoord w) {titleBlockSeparator=w; }
  void SetPrintVerseHeaders(bool b) {printVerseHeaders=b; }
  void SetPrintChorusHeaders(bool b) {printChorusHeaders=b; }
  void SetUseDecorations(bool b) {useDecorations=b; }
  void SetChorusHeaderText(const wxString& s) {chorusHeaderText=s; }

  wxFont GetVerse() {return verse; }
  wxFont GetChord() {return chord; }
  wxFont GetComment() {return comment; }
  wxFont GetChorus() {return chorus; }
  wxFont GetTitle() {return title; }
  wxFont GetVerseHeader() {return verseHeader; }
  wxFont GetChorusHeader() {return chorusHeader; }
  wxCoord GetVerseIndent() {return verseIndent; }
  wxCoord GetChorusIndent() {return chorusIndent; }
  wxCoord GetBlockSeparator() {return blockSeparator; }
  wxCoord GetVerseHeaderSeparator() {return verseHeaderSeparator; }
  wxCoord GetChorusHeaderSeparator() {return chorusHeaderSeparator; }
  wxCoord GetTitleIndent() {return titleIndent; }
  wxCoord GetTitleBlockSeparator() {return titleBlockSeparator; }
  bool GetPrintVerseHeaders() {return printVerseHeaders; }
  bool GetPrintChorusHeaders() {return printChorusHeaders; }
  bool GetUseDecorations() {return useDecorations; }
  wxString GetChorusHeaderText() {return chorusHeaderText; }

  void Serialize(TiXmlElement* node);

private:
  static void SerializeFont(TiXmlElement* node, const wxString& name, const wxFont& font);

  wxFont verse;
  wxFont chord;
  wxFont comment;
  wxFont chorus;
  wxFont title;
  wxFont verseHeader;
  wxFont chorusHeader;
  wxCoord verseIndent;
  wxCoord chorusIndent;
  wxCoord blockSeparator;
  wxCoord verseHeaderSeparator;
  wxCoord chorusHeaderSeparator;
  wxCoord titleIndent;
  wxCoord titleBlockSeparator;
  bool printVerseHeaders;
  bool printChorusHeaders;
  bool useDecorations;
  wxString chorusHeaderText;

};

#endif // TEXTPREFERENCES_H
