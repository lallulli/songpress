#ifndef INHERITEDPARAGRAPH_H_INCLUDED
#define INHERITEDPARAGRAPH_H_INCLUDED

#include "paragraph.h"


class InheritedParagraph : public Paragraph {
	public:

		void SetInheritedRightMargin(bool inherited);
		void SetInheritedLineSpacing(bool inherited);
		void SetInheritedParagraphSpacing(bool inherited);
		void SetInheritedShowNumber(bool inherited);
		void SetInheritedShowDecorations(bool inherited);
		void SetInheritedShowChords(bool inherited);
		void SetInheritedTransposeChords(bool inherited);

		bool GetInheritedRightMargin();
		bool GetInheritedLineSpacing();
		bool GetInheritedParagraphSpacing();
		bool GetInheritedShowNumber();
		bool GetInheritedShowDecorations();
		bool GetInheritedShowChords();
		bool GetInheritedTransposeChords();



	protected:

		bool inheritedRightMargin;
		bool inheritedLineSpacing;
		bool inheritedParagraphSpacing;
		bool inheritedShowNumber;
		bool inheritedShowDecorations;
		bool inheritedShowChords;
		bool inheritedTransposeChords;

};

#endif // INHERITEDPARAGRAPH_H_INCLUDED

/*
double RightMargin;rightMargin
double LineSpacing;lineSpacing
double ParagraphSpacing;paragraphSpacing
bool ShowNumber;showNumber
bool ShowDecorations;showDecorations
bool ShowChords;showChords
int TransposeChords;transposeChords

Match:
^\([^ ]*\) \([^;]*\);\([^ ]*\)$

Genera variabili inherited
\t\tbool inherited\2;

Genera dichiarazioni funzioni Get:
\t\t\1 Get\2();

Genera dichiarazioni funzioni Set:
\t\tvoid Set\2(\1 \3);

Genera dichiarazioni funzioni SetInherited:
\t\tvoid SetInherited\2(bool inherited);

Genera dichiarazioni funzioni GetInherited:
\t\tbool GetInherited\2();

Genera implementazione funzioni SetInherited:
void InheritedParagraph::SetInherited\2(bool inherited) {\n\tinherited\2 = inherited;\n}\n

Genera implementazione funzioni GetInherited:
bool InheritedParagraph::GetInherited\2() {\n\treturn inherited\2;\n}\n

*/
