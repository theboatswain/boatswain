SET SCRIPT_DIR=%~dp0
SET PYQTDEPLOY=venv\Scripts

@echo off

for %%a in ("%SCRIPT_DIR:~0,-1%") do set "PROJECT_DIR=%%~dpa"

CD /D %PROJECT_DIR%

FOR /F "delims=" %i IN ('python scripts\get_version.py boatswain\main.py') DO set VERSION=%i

%PYQTDEPLOY%\pyqtdeploy-build.exe pyqt-boatswain-win.pdy
CD build-win-32
%PROJECT_DIR%\sysroot-win-32\host\bin\qmake.exe
nmake

CD ..

@RD /S /Q release\win
MKDIR release\win\%VERSION%
MOVE build-win-32\release\Boatswain.exe release\win\%VERSION%\
COPY resources\* release\win\%VERSION%\
DEL /s /q /f release\win\%VERSION%\*.sh
DEL /s /q /f release\win\%VERSION%\*.desktop

python scripts\zipping.py release\win\%VERSION% x32 %VERSION%

