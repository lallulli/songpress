Required tools:
- cx_freeze (pip install cx_freeze)
- NSIS

Configure parameters in pynsis.py, such as:
 - path of NSIS executable
 - build path, depending on Python version (such as: src\build\exe.win32-3.9)

Then run:

python create_installer.py
