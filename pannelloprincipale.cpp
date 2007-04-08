/***************************************************************
 * Name:      pannelloprincipale.cpp
 * Purpose:   Panel which hosts song preview
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
#include "pannelloprincipale.h"
#include <wx/metafile.h>

BEGIN_EVENT_TABLE(PannelloPrincipale,wxPanel)
	//(*EventTable(PannelloPrincipale)
	EVT_BUTTON(ID_BUTTON1,PannelloPrincipale::OnBottoneClick)
	//*)
END_EVENT_TABLE()

PannelloPrincipale::PannelloPrincipale(wxWindow* parent,wxWindowID id)
{
	//(*Initialize(PannelloPrincipale)
	Create(parent,id,wxDefaultPosition,wxDefaultSize,wxTAB_TRAVERSAL);
	BoxSizer1 = new wxBoxSizer(wxVERTICAL);
	tela = new Tela(this,ID_CUSTOM1);
	BoxSizer2 = new wxBoxSizer(wxVERTICAL);
	Bottone = new wxButton(this,ID_BUTTON1,_("Copia negli Appunti"),wxDefaultPosition,wxDefaultSize,0);
	if (false) Bottone->SetDefault();
	BoxSizer2->Add(Bottone,1,wxALL|wxALIGN_CENTER,5);
	BoxSizer1->Add(tela,1,wxALL|wxALIGN_CENTER|wxEXPAND,5);
	BoxSizer1->Add(BoxSizer2,0,wxALL|wxALIGN_CENTER,5);
	this->SetSizer(BoxSizer1);
	BoxSizer1->Fit(this);
	BoxSizer1->SetSizeHints(this);
	//*)
}

PannelloPrincipale::~PannelloPrincipale()
{
}


void PannelloPrincipale::OnBottoneClick(wxCommandEvent& event) {
  wxMetafileDC dc;
  if (dc.Ok()) {
    tela->Disegna(dc, true);
    wxMetafile *mf = dc.Close();
    if(mf) {
      bool success = mf->SetClipboard((int)(dc.MaxX() + 10), (int)(dc.MaxY() + 10));
      delete mf;
    }
  }
}

void PannelloPrincipale::OnRimpicciolisciClick(wxCommandEvent& event)
{
  tela->Rimpicciolisci();
}

void PannelloPrincipale::OnIngrandisciClick(wxCommandEvent& event)
{
  tela->Ingrandisci();
}
