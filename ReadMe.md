# sprDB

The sprDB is under development...

## Build Instructions
on Windows:
```bash
pyinstaller -F -c -i spr.ico main.py
pyinstaller -F -w -i spr.ico sprserve.py
```

on Linux:
```bash
pyinstaller -F -i spr.ico main.py
pyinstaller -F -i spr.ico sprserve.py
```

Then you will get a `dist` folder with an executable file that can be run by double-clicking or using the terminal command.
