---
hide: toc
---

# The Chordpro Format

Songpress supports a subset of the original ChordPro format. The following table displays ChordPro directives supported by Songpress.

| Directive | Short Directive | Description | Example |
| :---------| --------------- | ----------- | ------- |
| {title:Song title}| {t:Song title} | The directive **title** produces the song title | {title:Greensleves} |
| {subtitle:Song subtitle} | {st:Song subtitle} | The directive **subtitle** produces the song subtitle | {subtitle:Traditional English song} |
| {start_of_chorus}...{end_of_chorus} | {soc}...{eoc} | The directive **chorus** produces a chorus verse with lyrics and chords inside the directives | {soc} [C]Greensleeves was [G]all my [Em]joy...{eoc} |
| {soc:Label}...{eoc} | | **Chorus with label** produces a chorus verse with lyrics and chords inside the directives, with the specified label instead of "Chorus". Label can be completely omitted by using _{soc:}...{eoc}_. ==**Note**: This is a Songpress non-standard directive== | {soc:Final} [C]Greensleeves was [G]all my [Em]joy... {eoc} |
| (blank line) | | Begins a new verse | |
| {verse:Label} | | **Verse with label** begins a new verse with the specified label instead of the verse number. Verse counter is not increased. Label can be completely omitted by using _{verse:}_. ==**Note**: This is a Songpress non-standard directive== | {verse:Instrum.}[C] [F] [G] |
| [Chord] | | **Chord** directive produces a chord just above the current position in lyrics | [C]Greensleeves was [G]all my [Em]joy |
| {comment:a comment} | {c:a comment} | The directive **comment** produces a comment | {c:repeat twice} |
| # Source comment | | Comment in the source chordpro file: it doesn't produce anything | # TODO: add other verses |
| {textfont:a font face} | | Set the **font face** starting from the position of the directive. When the parameter is omitted, default value is restored: `{textfont}` | {textfont:Arial} |
| {textsize:a size} | | Set the **font size** starting from the position of the directive. When the parameter is omitted, default value is restored: `{textsize}` | {textsize:12} |
| {textcolour:a colour} | | Set the **font color** starting from the position of the directive. Text color is expressed in a web-compatible format, such as `#RRGGBB`. When the parameter is omitted, default value is restored: `{textcolour}` | {textcolour:#FF0000} |
| {chordfont:a font face} | | Same as `{textfont}`, working on chords. | {chordfont:Courier New} |
| {chordsize:a size} | | Same as `{textsize}`, working on chords. | {chordsize:12} |
| {chordcolour:a colour} | | Same as `{textcolour}`, working on chords. | {chordcolour:blue} |
