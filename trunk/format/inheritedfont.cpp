#include "inheritedfont.h"

void InheritedFont::SetInheritName(bool inherit) {
	return inheritName;
}

void InheritedFont::SetInheritBold(bool inherit) {
	return inheritBold;
}

void InheritedFont::SetInheritItalic(bool inherit) {
	return inheritItalic;
}

void InheritedFont::SetInheritUnderlined(bool inherit) {
	return inheritUnderlined;
}

void InheritedFont::SetInheritSize(bool inherit) {
	return inheritSize;
}

bool InheritedFont::GetInheritName() {
	return inheritName;
}

bool InheritedFont::GetInheritBold() {
	return inheritBold;
}

bool InheritedFont::GetInheritItalic() {
	return inheritItalic;
}

bool InheritedFont::GetInheritUnderlined() {
	return inheritUnderlined;
}

bool InheritedFont::GetInheritSize() {
	return inheritSize;
}


wxString InheritedFont::GetName() {
  return inheritedName? parent->name: name;
}

bool InheritedFont::GetBold() {
  return inheritedBold? parent->bold: bold;
}

bool InheritedFont::GetItalic() {
  return inheritedItalic? parent->italic: italic;
}

bool InheritedFont::GetUnderlined() {
  return inheritedUnderlined? parent->underlined: underlined;
}

double InheritedFont::GetSize() {
  return inheritedSize? parent->size: size;
}


