#ifndef INPUTPANEL_H
#define INPUTPANEL_H
/***************************************************************
 * Name:      inputpanel.h
 * Purpose:   Panel which hosts editing component
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
#include <wx/wxprec.h>

#ifdef __BORLANDC__
    #pragma hdrstop
#endif

//(*Headers(InputPanel)
#include <wx/panel.h>
#include <wx/sizer.h>
#include <wx/textctrl.h>
//*)

class songpressFrame;

class InputPanel: public wxPanel
{
	public:

		InputPanel(songpressFrame* parent,wxWindowID id = -1);
		virtual ~InputPanel();

		//(*Identifiers(InputPanel)
		static const long ID_TEXTCTRL1;
		//*)
		
		wxString GetSong();
		void SetSong(const wxString& song);

	protected:

		//(*Handlers(InputPanel)
		void OnSongTextModified(wxCommandEvent& event);
		void OnSongTextChar(wxKeyEvent& event);
		//*)

		//(*Declarations(InputPanel)
		wxBoxSizer* BoxSizer1;
		wxTextCtrl* SongText;
		//*)
		
		songpressFrame* parent;

	private:

		DECLARE_EVENT_TABLE()
};

#endif
