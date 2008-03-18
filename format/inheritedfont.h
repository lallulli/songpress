#ifndef INHERITEDFONT_H_INCLUDED
#define INHERITEDFONT_H_INCLUDED

#include "font.h"


class InheritedFont : public Font
{
	public:
		void SetInheritName(bool inherit);
		void SetInheritBold(bool inherit);
		void SetInheritItalic(bool inherit);
		void SetInheritUnderlined(bool inherit);
		void SetInheritSize(bool inherit);
		bool GetInheritName();
		bool GetInheritBold();
		bool GetInheritItalic();
		bool GetInheritUnderlined();
		bool GetInheritSize();
    virtual wxString GetName();
    virtual bool GetBold();
    virtual bool GetItalic();
    virtual bool GetUnderlined();
    virtual double GetSize();

	protected:
		bool inheritName;
		bool inheritBold;
		bool inheritItalic;
		bool inheritUnderlined;
		bool inheritSize;
};

#endif // INHERITEDFONT_H_INCLUDED
