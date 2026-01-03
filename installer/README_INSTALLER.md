# How to build the Windows installer

In order to build the Windows installer you need to download:

- Windows x64 binaries of `uv`, e.g. [https://github.com/astral-sh/uv/releases/download/0.9.21/uv-x86_64-pc-windows-msvc.zip](https://github.com/astral-sh/uv/releases/download/0.9.21/uv-x86_64-pc-windows-msvc.zip)
- [icon-changer](https://github.com/stefanGaina/icon-changer/releases/download/v1.1.0/icon-changer-1.1.0.zip)
- The [NSIS compiler](https://nsis.sourceforge.io/Download)

Extract the content of the zip files of `uv` and `icon-changer` in this folder (`uv.exe` is sufficient). Then, launch the NSIS compiler and compile the `songpress.nsi` script.