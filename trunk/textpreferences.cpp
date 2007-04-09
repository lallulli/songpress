/***************************************************************
 * Name:      textpreferences.cpp
 * Purpose:   Contains preferences regarding font style
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
#include <wx/font.h>
#include <wx/dc.h>

#include "textpreferences.h"
#include "global.h"

TextPreferences::TextPreferences() {
  verseIndent=0;
  chorusIndent=0;
  blockSeparator=0;
  verseHeaderSeparator=0;
  chorusHeaderSeparator=0;
  titleIndent=0;
  titleBlockSeparator=0;
  printVerseHeaders=true;
  printChorusHeaders=true;
  useDecorations=true;
}


TextPreferences::~TextPreferences() {

}

void TextPreferences::SerializeFont(TiXmlElement* node, const wxString& name, const wxFont& font) {
  node->SetAttribute(name.mb_str(wxConvUTF8), font.GetNativeFontInfoDesc().mb_str(wxConvUTF8));
}


void TextPreferences::Serialize(TiXmlElement* node) {
  SerializeFont(node, _T("verse"), verse);
  SerializeFont(node, _T("chord"), chord);
  SerializeFont(node, _T("comment"), comment);
  SerializeFont(node, _T("chorus"), chorus);
  SerializeFont(node, _T("title"), title);
  SerializeFont(node, _T("verseHeader"), verseHeader);
  SerializeFont(node, _T("chorusHeader"), chorusHeader);
  node->SetAttribute("verseIndent", verseIndent);
  node->SetAttribute("chorusIndent", chorusIndent);
  node->SetAttribute("blockSeparator", blockSeparator);
  node->SetAttribute("verseHeaderSeparator", verseHeaderSeparator);
  node->SetAttribute("chorusHeaderSeparator", chorusHeaderSeparator);
  node->SetAttribute("titleIndent", titleIndent);
  node->SetAttribute("titleBlockSeparator", titleBlockSeparator);
  node->SetAttribute("printVerseHeader", printVerseHeaders);
  node->SetAttribute("printChorusHeader", printChorusHeaders);
  node->SetAttribute("useDecorations", useDecorations);
  node->SetAttribute("chorusHeaderText", chorusHeaderText.mb_str(wxConvUTF8));
}

