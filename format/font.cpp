#include "font.h"

void Font::SetName(wxString name) {
  this->name = name;
}

void Font::SetBold(bool bold) {
  this->bold = bold;
}

void Font::SetItalic(bool italic) {
  this->italic = italic;
}

void Font::SetUnderlined(bool underlined) {
  this->underlined = underlined;
}

void Font::SetSize(double size) {
  this->size = size;
}

wxString Font::GetName() {
  return name;
}

bool Font::GetBold() {
  return bold;
}

bool Font::GetItalic() {
  return italic;
}

bool Font::GetUnderlined() {
  return underlined;
}

double Font::GetSize() {
  return size;
}

void Font::ToXml() {}
void Font::FromXml() {}

