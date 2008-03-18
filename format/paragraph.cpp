#include "paragraph.h"

void SetRightMargin(double rightMargin) {
	this->rightMargin = rightMargin;
}

void SetLineSpacing(double lineSpacing) {
	this->lineSpacing = lineSpacing;
}

void SetParagraphSpacing(double paragraphSpacing) {
	this->paragraphSpacing = paragraphSpacing;
}

void SetShowNumber(bool showNumber) {
	this->showNumber = showNumber;
}

void SetShowDecorations(bool showDecorations) {
	this->showDecorations = showDecorations;
}

void SetShowChords(bool showChords) {
	this->showChords = showChords;
}

void SetTransposeChords(int transposeChords) {
	this->transposeChords = transposeChords;
}

double GetRightMargin() {
	return rightMargin;
}

double GetLineSpacing() {
	return lineSpacing;
}

double GetParagraphSpacing() {
	return paragraphSpacing;
}

bool GetShowNumber() {
	return showNumber;
}

bool GetShowDecorations() {
	return showDecorations;
}

bool GetShowChords() {
	return showChords;
}

int GetTransposeChords() {
	return transposeChords;
}

