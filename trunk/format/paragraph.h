#ifndef PARAGRAPH_H_INCLUDED
#define PARAGRAPH_H_INCLUDED


class Paragraph {
	public:

		virtual void SetRightMargin(double rightMargin);
		virtual void SetLineSpacing(double lineSpacing);
		virtual void SetParagraphSpacing(double paragraphSpacing);
		virtual void SetShowNumber(bool showNumber);
		virtual void SetShowDecorations(bool showDecorations);
		virtual void SetShowChords(bool showChords);
		virtual void SetTransposeChords(int transposeChords);
		virtual double GetRightMargin();
		virtual double GetLineSpacing();
		virtual double GetParagraphSpacing();
		virtual bool GetShowNumber();
		virtual bool GetShowDecorations();
		virtual bool GetShowChords();
		virtual int GetTransposeChords();

    virtual void ToXml();
    virtual void FromXml();

	protected:
		double rightMargin;
		double lineSpacing;
		double paragraphSpacing;
		bool showNumber;
		bool showDecorations;
		bool showChords;
		int transposeChords;
};

#endif // PARAGRAPH_H
