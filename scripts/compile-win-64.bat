SET SCRIPT_DIR=%~dp0
SET PYQTDEPLOY=venv\Scripts

@echo off
SET /p VERSION="Enter the release version: "

for %%a in ("%SCRIPT_DIR:~0,-1%") do set "PROJECT_DIR=%%~dpa"

CD /D %PROJECT_DIR%

COPY boatswain\main.py boatswain\main.py.bak

python scripts\update_version.py boatswain\main.py %VERSION%

%PYQTDEPLOY%\pyqtdeploy-build.exe pyqt-boatswain-win.pdy
CD build-win-64
%PROJECT_DIR%\sysroot-win-64\host\bin\qmake.exe
nmake

CD ..

@RD /S /Q release\win
MKDIR release\win\%VERSION%
MOVE build-win-64\release\Boatswain.exe release\win\%VERSION%\
COPY resources\* release\win\%VERSION%
DEL /s /q /f release\win\%VERSION%\*.sh
DEL /s /q /f release\win\%VERSION%\*.desktop

python scripts\zipping.py release\win\%VERSION% x64 %VERSION%

REM boatswain\main.py.bak main.py