/***************************************************************
 * Name:      songpressMain.cpp
 * Purpose:   Code for Application Frame
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/

#ifdef WX_PRECOMP
#include "wx_pch.h"
#endif

#ifdef __BORLANDC__
#pragma hdrstop
#endif //__BORLANDC__

#include <wx/filedlg.h>
#include <wx/sstream.h>
#include <wx/wfstream.h>
#include <wx/txtstrm.h>
#include <wx/event.h>

#include "songpressMain.h"


bool songpressFrameDropTarget::OnDropFiles(wxCoord x, wxCoord y, const wxArrayString& a) {
  return fp->OpenFile(a[0]);
}

//helper functions
enum wxbuildinfoformat {
    short_f, long_f };

wxString wxbuildinfo(wxbuildinfoformat format)
{
    wxString wxbuild(wxVERSION_STRING);

    if (format == long_f )
    {
#if defined(__WXMSW__)
        wxbuild << _T("-Windows");
#elif defined(__UNIX__)
        wxbuild << _T("-Linux");
#endif

#if wxUSE_UNICODE
        wxbuild << _T("-Unicode build");
#else
        wxbuild << _T("-ANSI build");
#endif // wxUSE_UNICODE
    }

    return wxbuild;
}

//(*InternalHeaders(songpressFrame)
#include <wx/bitmap.h>
#include <wx/intl.h>
#include <wx/image.h>
#include <wx/string.h>
//*)

//(*IdInit(songpressFrame)
const long songpressFrame::idMenuNew = wxNewId();
const long songpressFrame::idMenuOpen = wxNewId();
const long songpressFrame::idMenuSave = wxNewId();
const long songpressFrame::idMenuSaveAs = wxNewId();
const long songpressFrame::idMenuExit = wxNewId();
const long songpressFrame::idMenuAbout = wxNewId();
const long songpressFrame::ID_STATUSBAR1 = wxNewId();
const long songpressFrame::ID_TIMER = wxNewId();
const long songpressFrame::Open = wxNewId();
const long songpressFrame::ID_TOOLBAR1 = wxNewId();
//*)

BEGIN_EVENT_TABLE(songpressFrame,wxFrame)
	//(*EventTable(songpressFrame)
	//*)
	EVT_CLOSE(songpressFrame::OnClose)
END_EVENT_TABLE()

songpressFrame::songpressFrame(wxWindow* parent, wxWindowID id):
  fileNameValid(false),
  fileModified(false)
{
	//(*Initialize(songpressFrame)
	wxMenuBar* MenuBar1;

	Create(parent, id, _("The Song Press - Il Canzonatore"), wxDefaultPosition, wxDefaultSize, wxDEFAULT_FRAME_STYLE, _T("id"));
	MenuBar1 = new wxMenuBar();
	Menu1 = new wxMenu();
	MenuFileNew = new wxMenuItem(Menu1, idMenuNew, _("&New"), _("Create a new song"), wxITEM_NORMAL);
	Menu1->Append(MenuFileNew);
	MenuFileOpen = new wxMenuItem(Menu1, idMenuOpen, _("&Open..."), _("Open an existing song"), wxITEM_NORMAL);
	Menu1->Append(MenuFileOpen);
	MenuFileSave = new wxMenuItem(Menu1, idMenuSave, _("&Save..."), _("Save current song"), wxITEM_NORMAL);
	Menu1->Append(MenuFileSave);
	MenuFileSaveAs = new wxMenuItem(Menu1, idMenuSaveAs, _("Save &As..."), _("Save with a different name"), wxITEM_NORMAL);
	Menu1->Append(MenuFileSaveAs);
	MenuExit = new wxMenuItem(Menu1, idMenuExit, _("&Exit\tAlt-F4"), _("Quit the application"), wxITEM_NORMAL);
	Menu1->Append(MenuExit);
	MenuBar1->Append(Menu1, _("&File"));
	Menu2 = new wxMenu();
	MenuHelpAbout = new wxMenuItem(Menu2, idMenuAbout, _("About...\tF1"), _("Show info about this application"), wxITEM_NORMAL);
	Menu2->Append(MenuHelpAbout);
	MenuBar1->Append(Menu2, _("&Help"));
	SetMenuBar(MenuBar1);
	StatusBar1 = new wxStatusBar(this, ID_STATUSBAR1, 0, _T("ID_STATUSBAR1"));
	int __wxStatusBarWidths_1[1] = { -1 };
	int __wxStatusBarStyles_1[1] = { wxSB_NORMAL };
	StatusBar1->SetFieldsCount(1,__wxStatusBarWidths_1);
	StatusBar1->SetStatusStyles(1,__wxStatusBarStyles_1);
	SetStatusBar(StatusBar1);
	Timer.SetOwner(this, ID_TIMER);
	ToolBar1 = new wxToolBar(this, ID_TOOLBAR1, wxDefaultPosition, wxDefaultSize, wxTB_FLAT|wxTB_DOCKABLE|wxTB_HORIZONTAL|wxTB_NODIVIDER|wxNO_BORDER, _T("ID_TOOLBAR1"));
	ToolBarItem1 = ToolBar1->AddTool(Open, _("New item"), wxBitmap(wxImage(_T("C:\\Documents and Settings\\Luca\\Documenti\\cpp\\songpress\\open.png"))), wxNullBitmap, wxITEM_NORMAL, wxEmptyString, wxEmptyString);
	ToolBar1->Realize();
	SetToolBar(ToolBar1);

	Connect(idMenuNew,wxEVT_COMMAND_MENU_SELECTED,(wxObjectEventFunction)&songpressFrame::OnMenuFileNewSelected);
	Connect(idMenuOpen,wxEVT_COMMAND_MENU_SELECTED,(wxObjectEventFunction)&songpressFrame::OnMenuFileOpenSelected);
	Connect(idMenuSave,wxEVT_COMMAND_MENU_SELECTED,(wxObjectEventFunction)&songpressFrame::OnMenuFileSaveSelected);
	Connect(idMenuSaveAs,wxEVT_COMMAND_MENU_SELECTED,(wxObjectEventFunction)&songpressFrame::OnMenuFileSaveAsSelected);
	Connect(idMenuExit,wxEVT_COMMAND_MENU_SELECTED,(wxObjectEventFunction)&songpressFrame::OnQuit);
	Connect(idMenuAbout,wxEVT_COMMAND_MENU_SELECTED,(wxObjectEventFunction)&songpressFrame::OnAbout);
	Connect(ID_TIMER,wxEVT_TIMER,(wxObjectEventFunction)&songpressFrame::OnTimerTrigger);
	//*)
	dropTarget = new songpressFrameDropTarget(this);
	SetDropTarget(dropTarget);

	auiManager = new wxAuiManager(this);
	inputPanel = new InputPanel(this, -1);
  outputPanel = new PannelloPrincipale(this, -1);
  auiManager->AddPane(inputPanel, wxCENTER, wxT("CRD data"));
  auiManager->AddPane(outputPanel, wxRIGHT, wxT("Output"));
  /*auiManager->AddPane(
    ToolBar1,
    wxAuiPaneInfo().
    Name(wxT("tb1")).Caption(wxT("Big Toolbar")).
    ToolbarPane().Top().
    LeftDockable(false).RightDockable(false)
  );*/
  auiManager->Update();
  SetWindowTitle();

}

songpressFrame::~songpressFrame()
{
	//(*Destroy(songpressFrame)
	//*)
}

void songpressFrame::OnQuit(wxCommandEvent& event)
{
    Close();
}

void songpressFrame::OnAbout(wxCommandEvent& event)
{
    wxString msg = _("The Song Press - Il Canzonatore.\nCopyright (c) 2006-2007 Luca Allulli");
    wxMessageBox(msg, _("About The Song Press"));
}

void songpressFrame::NotifyLazySongModified() {
  fileModified = true;
  Timer.Start(1000, true);
}

void songpressFrame::NotifySongModified() {
  fileModified = true;
  Timer.Stop();
  outputPanel->LoadSong(inputPanel->GetSong());
}

void songpressFrame::OnTimerTrigger(wxTimerEvent& event) {
  outputPanel->LoadSong(inputPanel->GetSong());
}

void songpressFrame::OnMenuFileSaveSelected(wxCommandEvent& event) {
  Save();
  event.Skip();
}

bool songpressFrame::SaveAs() {
  bool leave = false;
  bool consensus = false;
  wxFileName fn;
  do {
      wxFileDialog dlg (
      this,
      _("Choose a name for the file"),
      _T(""),
      _T(""),
      _("CRD files (*.crd)|*.crd|All files (*.*)|*.*"),
      wxFD_SAVE
    );

    if(dlg.ShowModal()==wxID_OK) {

      fn = dlg.GetPath();
      if(fn.FileExists()) {
        wxString msg;
        msg.Printf(_("File \"%s\" already exists. Do you want to overwrite it?"), fn.GetName().GetData());
        wxMessageDialog d(
          this,
          msg,
          _("The Song Press"),
          wxYES_NO | wxCANCEL | wxICON_QUESTION
        );
        switch(d.ShowModal()) {
          case wxID_CANCEL:
            leave = true;
            consensus = false;
            break;
          case wxID_NO:
            leave = false;
            consensus = false;
            break;
          default: //wxID_YES
            leave = true;
            consensus = true;
        }
      } else {
        leave = true;
        consensus = true;
      }

    } else {
      leave = true;
      consensus = false;
    }

  } while(!leave);

  if(consensus) {
    fileName=fn;
    fileNameValid = true;
    SetWindowTitle();
    Save();
    return true;
  } else return false;

}

bool songpressFrame::Save() {
  if(!fileNameValid)
    return SaveAs();
  else {
    wxFileOutputStream f(fileName.GetFullPath());
    wxTextOutputStream out(f, wxEOL_NATIVE, wxConvISO8859_1);
// TODO (Luca#1#): Give also UTF8 converter
    out << inputPanel->GetSong();
    fileModified = false;
    return true;
  }
}

bool songpressFrame::OpenFileAsk() {
  if(EnforceFileSaved()) {
    wxFileDialog dlg (
      this,
      _("Open file"),
      _T(""),
      _T(""),
      _("CRD files (*.crd)|*.crd|All files (*.*)|*.*"),
      wxFD_OPEN
    );

    if(dlg.ShowModal()==wxID_OK) {
      wxFileName fn = dlg.GetPath();
      if(fn.FileExists()) {
        fileName = fn;
        fileNameValid = true;
        SetWindowTitle();
        OpenFile();
        return true;
      } else {
        wxString msg;
        msg.Printf(_("File \"%s\" does not exist."), fn.GetName().GetData());
        wxMessageDialog d(
          this,
          msg,
          _("The Song Press"),
          wxOK | wxICON_ERROR
        );
        d.ShowModal();
        return false;
      }
    } else return false;
  } else return false;
}

void songpressFrame::OpenFile() {
  wxString song;
  wxFileInputStream f(fileName.GetFullPath());
  wxTextInputStream in(f, _T("\t"), wxConvISO8859_1);
// TODO (Luca#1#): Give also UTF8 converter
  wxString s;
  while(!f.Eof()) {
    s = in.ReadLine();
    song += s;
    if(!f.Eof())
      song += _T("\n");
  }
  inputPanel->SetSong(song);
  fileModified = false;
}


void songpressFrame::SetWindowTitle() {
  if(!fileNameValid) {
    SetTitle(_("Untitled - The Song Press"));
  } else {
    SetTitle(fileName.GetName() + _(" - The Song Press"));
  }
}


void songpressFrame::OnMenuFileOpenSelected(wxCommandEvent& event) {
  OpenFileAsk();
  event.Skip();
}


void songpressFrame::OnMenuFileSaveAsSelected(wxCommandEvent& event) {
  SaveAs();
  event.Skip();
}


bool songpressFrame::EnforceFileSaved(bool canCancel) {
  if(fileModified) {

    wxMessageDialog d(
      this,
      _("Your song has been modified. Do you want to save it?"),
      _("The Song Press"),
      wxYES_NO | wxICON_QUESTION | (canCancel? wxCANCEL: 0)
    );
    switch(d.ShowModal()) {
      case wxID_CANCEL:
        return false;
      case wxID_NO:
        return true;
      default: //wxID_YES
        return Save();
    }
  }
  else
    return true;
}

void songpressFrame::OnMenuFileNewSelected(wxCommandEvent& event) {
  NewFile();
}

bool songpressFrame::NewFile() {
  if(EnforceFileSaved()) {
    inputPanel->Clear();
    fileNameValid = false;
    fileModified = false;
    outputPanel->LoadSong(_T(""));
    SetWindowTitle();
    return true;
  } else return false;
}

void songpressFrame::OnClose(wxCloseEvent& e) {
  if(EnforceFileSaved(e.CanVeto()))
    Destroy();
  else
    e.Veto();
  e.Skip();
}

bool songpressFrame::OpenFile(wxString filePath) {
  wxFileName fn = filePath;
  if(fn.FileExists()) {
    if(EnforceFileSaved()) {
      fileName = fn;
      fileNameValid = true;
      SetWindowTitle();
      OpenFile();
      return true;
    }
  }
  return false;
}
