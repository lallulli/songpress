#ifndef FONT_H_INCLUDED
#define FONT_H_INCLUDED

#include <wx_pch.h>

class Font {
  public:
    virtual void SetName(wxString name);
    virtual void SetBold(bool bold);
    virtual void SetItalic(bool italic);
    virtual void SetUnderlined(bool underlined);
    virtual void SetSize(double size);
    virtual wxString GetName();
    virtual bool GetBold();
    virtual bool GetItalic();
    virtual bool GetUnderlined();
    virtual double GetSize();

    virtual void ToXml();
    virtual void FromXml();

  protected:
    wxString name;
    bool bold;
    bool italic;
    bool underlined;
    double size;
};

#endif // FONT_H_INCLUDED
