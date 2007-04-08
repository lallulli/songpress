/***************************************************************
 * Name:      pannelloprincipale.h
 * Purpose:   Panel which hosts song preview
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
 #ifndef PANNELLOPRINCIPALE_H
#define PANNELLOPRINCIPALE_H

#include <wx/wxprec.h>
#include "tela.h"

#ifdef __BORLANDC__
    #pragma hdrstop
#endif

//(*Headers(PannelloPrincipale)
#include <wx/button.h>
#include <wx/intl.h>
#include <wx/panel.h>
#include <wx/settings.h>
#include <wx/sizer.h>
//*)

class PannelloPrincipale: public wxPanel
{
	public:

		PannelloPrincipale(wxWindow* parent,wxWindowID id = -1);
		virtual ~PannelloPrincipale();

    void LoadSong(const wxString& s) {tela->LoadSong(s); }


		//(*Identifiers(PannelloPrincipale)
		enum Identifiers
		{
		  ID_BUTTON1 = 0x1000,
		  ID_CUSTOM1
		};
		//*)

	protected:

		//(*Handlers(PannelloPrincipale)
		void OnBottoneClick(wxCommandEvent& event);
		void OnRimpicciolisciClick(wxCommandEvent& event);
		void OnIngrandisciClick(wxCommandEvent& event);
		//*)

		//(*Declarations(PannelloPrincipale)
		wxBoxSizer* BoxSizer1;
		Tela* tela;
		wxBoxSizer* BoxSizer2;
		wxButton* Bottone;
		//*)

	private:

		DECLARE_EVENT_TABLE()
};

#endif
