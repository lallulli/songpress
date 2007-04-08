/***************************************************************
 * Name:      songpressApp.h
 * Purpose:   Defines Application Class
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
#ifndef SONGPRESSAPP_H
#define SONGPRESSAPP_H

#include <wx/wxprec.h>

#ifdef __BORLANDC__
    #pragma hdrstop
#endif

#ifndef WX_PRECOMP
    #include <wx/wx.h>
#endif

class songpressApp : public wxApp
{
	public:
		virtual bool OnInit();
};

#endif // songpressAPP_H
