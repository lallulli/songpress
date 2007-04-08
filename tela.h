/***************************************************************
 * Name:      tela.h
 * Purpose:   Scrolled component where song preview is drawed
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
#ifndef TELA_H
#define TELA_H

#include <wx/wxprec.h>

#ifdef __BORLANDC__
    #pragma hdrstop
#endif

#define EPSILON_DRAG (10)

//(*Headers(Tela)
//*)

class Tela: public wxScrolledWindow
{
	public:

		Tela(wxWindow* parent,wxWindowID id = -1);
		virtual ~Tela();

    void Disegna(wxDC& dc, bool metafile);
    void Ingrandisci() {SetVirtualSize(900, 900); }
    void Rimpicciolisci() {SetVirtualSize(50, 50); }

    //void LoadFile(const wxString& s) {fileName=s; Refresh();}
    void LoadSong(const wxString& s) {song = s; Refresh();}


		//(*Identifiers(Tela)
		//*)

	protected:

		//(*Handlers(Tela)
		//*)

		//(*Declarations(Tela)
		//*)
    DECLARE_EVENT_TABLE()
	private:
    virtual void OnDraw(wxDC& dc);
    void OnLeftButtonDown(wxMouseEvent& e);
    void OnLeftButtonUp(wxMouseEvent& e);
    void OnMouseMove(wxMouseEvent& e);
    void EndDragging();

    wxString fileName;
    wxString song;
    bool mouseMoving;
    bool mouseDragged;
    wxCoord yStart;
    wxCoord yStop;
};

#endif
