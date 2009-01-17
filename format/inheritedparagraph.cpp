#include "inheritedparagraph.h"

void InheritedParagraph::SetInheritedRightMargin(bool inherited) {
	inheritedRightMargin = inherited;
}

void InheritedParagraph::SetInheritedLineSpacing(bool inherited) {
	inheritedLineSpacing = inherited;
}

void InheritedParagraph::SetInheritedParagraphSpacing(bool inherited) {
	inheritedParagraphSpacing = inherited;
}

void InheritedParagraph::SetInheritedShowNumber(bool inherited) {
	inheritedShowNumber = inherited;
}

void InheritedParagraph::SetInheritedShowDecorations(bool inherited) {
	inheritedShowDecorations = inherited;
}

void InheritedParagraph::SetInheritedShowChords(bool inherited) {
	inheritedShowChords = inherited;
}

void InheritedParagraph::SetInheritedTransposeChords(bool inherited) {
	inheritedTransposeChords = inherited;
}


bool InheritedParagraph::GetInheritedRightMargin() {
	return inheritedRightMargin;
}

bool InheritedParagraph::GetInheritedLineSpacing() {
	return inheritedLineSpacing;
}

bool InheritedParagraph::GetInheritedParagraphSpacing() {
	return inheritedParagraphSpacing;
}

bool InheritedParagraph::GetInheritedShowNumber() {
	return inheritedShowNumber;
}

bool InheritedParagraph::GetInheritedShowDecorations() {
	return inheritedShowDecorations;
}

bool InheritedParagraph::GetInheritedShowChords() {
	return inheritedShowChords;
}

bool InheritedParagraph::GetInheritedTransposeChords() {
	return inheritedTransposeChords;
}

void InheritedParagraph::GetRightMargin() {
	return inheritedRightMargin? parent->rightMargin: rightMargin;
}

void InheritedParagraph::GetLineSpacing() {
	return inheritedLineSpacing? parent->lineSpacing: lineSpacing;
}

void InheritedParagraph::GetParagraphSpacing() {
	return inheritedParagraphSpacing? parent->paragraphSpacing: paragraphSpacing;
}

void InheritedParagraph::GetShowNumber() {
	return inheritedShowNumber? parent->showNumber: showNumber;
}

void InheritedParagraph::GetShowDecorations() {
	return inheritedShowDecorations? parent->showDecorations: showDecorations;
}

void InheritedParagraph::GetShowChords() {
	return inheritedShowChords? parent->showChords: showChords;
}

void InheritedParagraph::GetTransposeChords() {
	return inheritedTransposeChords? parent->transposeChords: transposeChords;
}
