Songpress is a free, easy to use song typeset program for Windows and Linux, that generates high-quality songbooks.

Songpress is focused on song formatting. Once your song is ready, you can copy-paste it into your favorite program, to give your songbook the look you like the most.

### Windows Installation

To install Songpress on Windows, we provide a [network installer](https://github.com/lallulli/songpress/releases/download/1.9.0rc4/songpress-net-setup.exe)
that downloads and installs the latest available version of Songpress.

Songpress is distributed through [PyPI](https://pypi.org/project/songpress/), the standard repository for Python packages. The network installer uses `uv` to:

1. Check whether a recent version of Python is already installed on your system. If not, the installer will download a local version of Python dedicated to Songpress.
2. Download and install Songpress along with all its dependencies (locally).

All installed files are contained in a single folder within your _Program Files_ directory, allowing Songpress to be cleanly uninstalled using its own uninstaller.

### Linux Installation

On Linux, you can install Songpress using [pipx](https://github.com/pypa/pipx):

```bash
pipx install songpress
```

Alternatively, you can use [uv](https://github.com/astral-sh/uv):

```bash
uv tool install songpress
```

The installation process may take several minutes, as the installer needs to download and compile the wxPython and wxWidgets libraries. Once installed, you can run Songpress by typing:

```bash
songpress
```

You can create a start menu (application menu) shortcut by executing:

```bash
songpress --create-shortcuts
```

To upgrade Songpress on Linux, run:

```bash
pipx upgrade songpress
```

### Highlights

- Produce **high-quality guitar scores** (text and chords)
- **Easy** to learn, quick to use
- You can **paste formatted songs** into any Linux and Windows application, to layout your songbook with maximum flexibility (Affinity, Microsoft Word, LibreOffice, Microsoft Publisher, Inkscape etc.)
- **Export** formatted songs to PNG and HTML (web pages and snippets)
- **Chord transposition** with automatic key detection
- **Chord simplification** for beginner guitarists: determine the easiest key to play your song, and transpose it automatically
- Support several **chord notations**: American (C, D, E), Italian (Do, Re, Mi), French, German and Portuguese; notation conversion
- Support Chordpro and Tab (i.e. two-line) **chord formats**
- **Clean up** dirty songs with spurious blank lines (such as songs copied and pasted from web pages) and not homogeneous chord notations


Learn more at http://www.skeed.it/songpress
  
### Known Issues

__Linux: SVG export and display scaling__

When the system display scaling factor is not set to 1, the SVG output produced by Copy as Image may be incorrectly formatted. This is a known issue in the current wxPython release. The underlying problem [has already been fixed upstream in wxWidgets](https://github.com/wxWidgets/wxWidgets/issues/25707) and will be resolved automatically once the next version of wxPython becomes available.
