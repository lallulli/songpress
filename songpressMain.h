/***************************************************************
 * Name:      songpressMain.h
 * Purpose:   Defines Application Frame
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/

#ifndef SONGPRESSMAIN_H
#define SONGPRESSMAIN_H

#include "songpressApp.h"
#include "pannelloprincipale.h"
#include "inputpanel.h"
#include <wx/aui/aui.h>
#include <wx/filename.h>


//(*Headers(songpressFrame)
#include <wx/frame.h>
#include <wx/menu.h>
#include <wx/statusbr.h>
#include <wx/timer.h>
#include <wx/toolbar.h>
//*)

class songpressFrame: public wxFrame
{
	public:

		songpressFrame(wxWindow* parent,wxWindowID id = -1);
		virtual ~songpressFrame();
		
		void NotifySongModified();
		void NotifyLazySongModified();

	private:
	
    bool NewFile();          //Clears current file
    bool SaveAs();           //Ask for file name and save
    bool Save();             //Save file fileName
    bool OpenFileAsk();      //Ask for file name and open
    void OpenFile();         //Open file fileName
    void SetWindowTitle();   //Sets window title from fileName (or Untitled)
    bool EnforceFileSaved(); //If there are modifications, ask whether to save;
                             //Return false if user cancels operation

		//(*Handlers(songpressFrame)
		void OnQuit(wxCommandEvent& event);
		void OnAbout(wxCommandEvent& event);
		void OnTimerTrigger(wxTimerEvent& event);
		void OnMenuFileSaveSelected(wxCommandEvent& event);
		void OnMenuFileOpenSelected(wxCommandEvent& event);
		void OnMenuFileSaveAsSelected(wxCommandEvent& event);
		void OnMenuFileNewSelected(wxCommandEvent& event);
		//*)
		void OnClose(wxCloseEvent& event);

		//(*Identifiers(songpressFrame)
		static const long idMenuNew;
		static const long idMenuOpen;
		static const long idMenuSave;
		static const long idMenuSaveAs;
		static const long idMenuExit;
		static const long idMenuAbout;
		static const long ID_STATUSBAR1;
		static const long ID_TIMER;
		static const long ID_TOOLBAR1;
		static const long Open;
		//*)

		//(*Declarations(songpressFrame)
		wxMenu* Menu1;
		wxMenuItem* MenuFileNew;
		wxMenuItem* MenuFileOpen;
		wxMenuItem* MenuFileSave;
		wxMenuItem* MenuFileSaveAs;
		wxMenuItem* MenuExit;
		wxMenu* Menu2;
		wxMenuItem* MenuHelpAbout;
		wxStatusBar* StatusBar1;
		wxTimer Timer;
		wxToolBar* ToolBar1;
		wxToolBarToolBase* ToolBarItem1;
		//*)
		
		wxAuiManager* auiManager;
		PannelloPrincipale* outputPanel;
		InputPanel* inputPanel;
		wxFileName fileName;
		bool fileNameValid;
		bool fileModified;

		DECLARE_EVENT_TABLE()
};

#endif // SONGPRESSMAIN_H
