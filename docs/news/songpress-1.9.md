# Songpress 1.9.0 released

Happy Epiphany from the Songpress team!

Today, we are releasing a new version of Songpress: **1.9.0**. The main goals of this release are:

- **Code cleanup and modernization**. Simplify and modernize the codebase so that Songpress can be built against recent versions of its dependencies, in particular wxPython.
- **Installation system overhaul**. Songpress is now published on PyPI and can be installed on both Linux and Windows using standard tools such as pipx or uv. On Windows, a new network-based GUI installer bundles and uses uv to download and install all required dependencies in a standard, reliable way.
- **Feature parity on Linux**. Linux now reaches feature parity with Windows. The Copy as Image command is now available and copies the formatted output to the clipboard as an SVG image (with PNG as a fallback for applications that do not support SVG). For example, SVG-based copy and paste produces perfect results in Inkscape and in the unofficial Wine-based Affinity for Linux desktop publishing solution.
