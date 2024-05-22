PYINSTALLER=pyinstaller
ICON=spr.ico
MAIN_SCRIPT=main.py
SPRSERVE_SCRIPT=sprserve.py

all: main_exe_w sprserve_exe_w main_exe_l sprserve_exe_l

# Windows目标
w: main_exe_w sprserve_exe_w

# Linux目标
l: main_exe_l sprserve_exe_l

main_exe_w:
	$(PYINSTALLER) -F -c -i $(ICON) $(MAIN_SCRIPT)

sprserve_exe_w:
	$(PYINSTALLER) -F -w -i $(ICON) $(SPRSERVE_SCRIPT)

main_exe_l:
	$(PYINSTALLER) -F -i $(ICON) $(MAIN_SCRIPT)

sprserve_exe_l:
	$(PYINSTALLER) -F -i $(ICON) $(SPRSERVE_SCRIPT)
