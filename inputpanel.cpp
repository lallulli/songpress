/***************************************************************
 * Name:      inputpanel.cpp
 * Purpose:   Panel which hosts editing component
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
 #include "inputpanel.h"
#include "debmessage.h"

//(*InternalHeaders(InputPanel)
#include <wx/bitmap.h>
#include <wx/font.h>
#include <wx/fontenum.h>
#include <wx/fontmap.h>
#include <wx/image.h>
#include <wx/intl.h>
#include <wx/settings.h>
//*)

#include <wx/defs.h>

#include "songpressMain.h"

//(*IdInit(InputPanel)
const long InputPanel::ID_TEXTCTRL1 = wxNewId();
//*)

BEGIN_EVENT_TABLE(InputPanel,wxPanel)
	//(*EventTable(InputPanel)
	//*)
END_EVENT_TABLE()

InputPanel::InputPanel(songpressFrame* parent, wxWindowID id)
{
	//(*Initialize(InputPanel)
	Create(parent,id,wxDefaultPosition,wxDefaultSize,wxTAB_TRAVERSAL,_T("wxPanel"));
	BoxSizer1 = new wxBoxSizer(wxHORIZONTAL);
	SongText = new wxTextCtrl(this,ID_TEXTCTRL1,wxEmptyString,wxDefaultPosition,wxDefaultSize,wxTE_MULTILINE|wxTE_RICH2,wxDefaultValidator,_T("ID_TEXTCTRL1"));
	BoxSizer1->Add(SongText,1,wxALL|wxEXPAND|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL,0);
	SetSizer(BoxSizer1);
	BoxSizer1->Fit(this);
	BoxSizer1->SetSizeHints(this);
	Connect(ID_TEXTCTRL1,wxEVT_COMMAND_TEXT_UPDATED,(wxObjectEventFunction)&InputPanel::OnSongTextModified);
	SongText->Connect(ID_TEXTCTRL1,wxEVT_CHAR,(wxObjectEventFunction)&InputPanel::OnSongTextChar,NULL,this);
	//*)
	this->parent = parent;
}

InputPanel::~InputPanel()
{
	//(*Destroy(InputPanel)
	//*)
}


void InputPanel::OnSongTextModified(wxCommandEvent& event) {
  parent->NotifyLazySongModified();
  event.Skip();
}

wxString InputPanel::GetSong() {
  return SongText->GetValue();
}

void InputPanel::SetSong(const wxString& s) {
  SongText->SetValue(s);
  parent->NotifySongModified();
}

void InputPanel::OnSongTextChar(wxKeyEvent& event) {
  if(event.GetKeyCode() == WXK_RETURN) {
    parent->NotifySongModified();
  }
  event.Skip();
}

void InputPanel::Clear() {
  SongText->SetValue(_T(""));
}
