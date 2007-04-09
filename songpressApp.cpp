/***************************************************************
 * Name:      songpressApp.cpp
 * Purpose:   Code for Application Class
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/

#ifdef WX_PRECOMP //
#include "wx_pch.h"
#endif

#ifdef __BORLANDC__
#pragma hdrstop
#endif //__BORLANDC__

#include "songpressApp.h"

//(*AppHeaders
#include "songpressMain.h"
#include <wx/image.h>
#include <wx/cmdline.h>
//*)

IMPLEMENT_APP(songpressApp);

bool songpressApp::OnInit()
{
	bool wxsOK = true;
	wxInitAllImageHandlers();
	if ( wxsOK )
	{
	  songpressFrame* Frame = new songpressFrame(NULL);
	  Frame->Show();
	  SetTopWindow(Frame);
	  wxCmdLineParser cmd(argc, argv);
	  cmd.AddParam(_("inputFile"), wxCMD_LINE_VAL_STRING, wxCMD_LINE_PARAM_OPTIONAL);
	  if(cmd.Parse()==0) {
      if(cmd.GetParamCount()==1) {
        Frame->OpenFile(cmd.GetParam(0));
      }
	  }
	}

	return wxsOK;

}
