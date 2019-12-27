SET SCRIPT_DIR=%~dp0
SET PYQTDEPLOY=venv\Scripts

for %%a in ("%SCRIPT_DIR%") do set "PROJECT_DIR=%%~dpa"

CD /D %PROJECT_DIR%

%PYQTDEPLOY%\pyqtdeploy-build.exe pyqt-boatswain-win.pdy
CD build-win-32
%PROJECT_DIR%\sysroot-win-32\host\bin\qmake.exe
nmake

CD ..

@RD /S /Q release\win
MKDIR release\win
MOVE build-win-32\release\Boatswain.exe release\win\
COPY resources\* release\win\