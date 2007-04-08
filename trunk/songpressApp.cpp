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
//*)

IMPLEMENT_APP(songpressApp);

bool songpressApp::OnInit()
{
	//(*AppInitialize
	bool wxsOK = true;
	wxInitAllImageHandlers();
	if ( wxsOK )
	{
	  songpressFrame* Frame = new songpressFrame(NULL);
	  Frame->Show();
	  SetTopWindow(Frame);
	}
	//*)
	return wxsOK;

}
