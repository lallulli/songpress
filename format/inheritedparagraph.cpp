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
