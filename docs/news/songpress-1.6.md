# Songpress 1.6 released, fork it on GitHub!

Songpress 1.6 introduces the following features:

- **Windows 10 compatibility**
- **Different output** for different usage: chords are not always useful. For a large lead sheet, chords on every single verse are welcome, but for a small leaflet one could prefer to put chords only on the first verse and on the (first) chorus, in order to save space, or even to remove chords completely (for example for singers). Therefore Songpress introduces three levels of "chordeness":
    - complete, chords are typeset on every verse
    - minimal, only one verse for each type gets chords (Songpress will determine automatically the first occurrence of a verse with a new chord pattern)
    - chords off
    - **Chord normalization**: quickly clean up chords, so that a homogeneous notation is adopted

Furthermore, we moved our project from Google Code to [Github](https://github.com/lallulli/songpress), and prepared some scripts to automate builds. Hopefully new releases will take less time to be prepared, and will benefit from contributions from the community. Please contribute by forking our code!
