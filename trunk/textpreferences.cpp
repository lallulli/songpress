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

