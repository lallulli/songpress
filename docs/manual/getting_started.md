# Getting started

Songpress is an application that allows you to typeset songs, with chords an lyrics, easily.

With Songpress you cannot print your songs directly. Instead, once you have prepared your song, you have to "transfer" the song to an application that is able to print it; such as your favourite word processor (Microsoft Word, Openoffice.org, etc.), a desktop publishing application (for example Affinity), etc. Why? Because Songpress's business is to format beautiful songs - and it is skilled at it. But to prepare beautiful page layouts is the business of other good pieces of software, such as a Desktop Publishing application.

Thus, how do you prepare a song?

1. In Songpress, compose the song in the [ChordPro](chordpro.md) format. Essentially, just write the song and place the chords into square brackets: `[C]This is a [Am]beauty[Em]ful [G7]song`.
2. Check out the formatted song in the preview pane. If you like it, go ahead.
3. Copy the song into the Clipboard: select Edit -> Copy as Image
4. Open your favorite **publishing program** (e.g. Affinity) and paste your song: select Edit -> Paste

## Installation

Songpress officially runs on Windows and Linux. Installation via Linux instructions might also work on macOS, but it has not been tested on that platform.

### Windows Installation

To install Songpress on Windows, we provide a [network installer](https://github.com/lallulli/songpress/releases/download/1.9.0/songpress-net-setup.exe)
that downloads and installs the latest available version of Songpress.

Songpress is distributed through [PyPI](https://pypi.org/project/songpress/), the standard repository for Python packages. The network installer uses `uv` to:

1. Check whether a recent version of Python is already installed on your system. If not, the installer will download a local version of Python dedicated to Songpress.
2. Download and install Songpress along with all its dependencies (locally).

All installed files are contained in a single folder within your _Program Files_ directory, allowing Songpress to be cleanly uninstalled using its own uninstaller.

### Linux Installation

!!! Warning
    Songpress is written in [Python](https://python.org): be sure you have Python installed on your Linux system.

On Linux, you can install Songpress by using three alternative methods:

1. [Python virtual environment](https://docs.python.org/3/library/venv.html) and [pip](https://pypi.org/project/pip/)
2. [pipx](https://github.com/pypa/pipx)
3. [uv](https://github.com/astral-sh/uv)

The installation process may take several minutes, as the installer needs to download and compile [wxPython](https://wxpython.org/) and [wxWidgets](https://wxwidgets.org/) libraries.

!!! Warning
    Be sure your system has the [requirements to compile wxWidgets](https://docs.wxwidgets.org/3.2.10/page_introduction.html) and [wxPython](https://wiki.wxpython.org/How%20to%20install%20wxPython)


#### Install by using Python virtual environment and pip

Firstly, create a new virtual environment. Let's suppose the directory containing Python virtual environments is `~/.venv`:

```bash
python -m venv ~/.venv/songpress
```

then activate it:

```bash
source ~/.venv/songpress/bin/activate
```

then install Songpress via pip:

```bash
pip install songpress
```

#### Install by using pipx

If you installed [pipx](https://github.com/pypa/pipx) on your system:

```bash
pipx install songpress
```

#### Install by using uv

Alternatively, you can use [uv](https://github.com/astral-sh/uv):

```bash
uv tool install songpress
```

### Running Songpress

!!! note
    If you installed Songpress in a [virtual environment](#install-by-using-python-virtual-environment-and-pip), you have to activate it before running the application:

    ```bash
    source ~/.venv/songpress/bin/activate
    ```

You can run Songpress by typing:

```bash
songpress
```

You can create a start menu (application menu) shortcut by executing:

```bash
songpress --create-shortcuts
```

To upgrade Songpress on Linux, run:

```bash
pipx upgrade 

# if you use pip in a virtual environment:
#
# pip upgrade
#
```
