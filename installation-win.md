# Boatswain installation for windows  
This instruction is applied for pyqtdeploy version 2.4 and Python version 3.7
## Preparation  
#### Installing MSVC 2017
+ Download Build Tools for Visual Studio 2017 (version 15.0) from https://visualstudio.microsoft.com/vs/older-downloads/ (You may have to join the Dev Essentials program, but don't worry, it's free and easy to apply)  
+ From the Installer UI, pick Visual C++ build tools  
+ Click install  
#### Installing Python  
You would need 3 versions of Python, including version 3.7 (32 + 64 bits) and version 2.7.   
The Python version 3.7 (32-bit) and 2.7 will be using for building the pyqt environment (sysroot).   
Python version 3.7 (64-bit) will be used for running the build.  
+ Download Python for Windows version 3.7.x.x (32-bit version only) from https://www.python.org/downloads/windows/  
+ Install Python   
  + Check the add Python to PATH checkbox  
  + After finished installation, check the Disable Path Length Limit  
+ Download Python 2.7 for Windows from https://www.python.org/ftp/python/2.7.15/python-2.7.15.amd64.msi  
+ Install Python  
  + Check Add python.exe to Path  
#### Installing Perl  
+ Download and install from http://strawberryperl.com  
#### Installing dependencies  
+ Start the Developer Command Prompt for VS 2017  
+ Go to the project's directory  
+ Create an environment for your project:   
```  
pip install virtualenv  
virtualenv venv  
venv\Scripts\activate.bat  
```  
+ Install project's dependencies: `pip install -r requirements.txt`  
+ Install pyqtdeploy: `pip install pyqtdeploy`  
+ Install Wget for window:   
  + Download from https://eternallybored.org/misc/wget/1.20.3/64/wget.exe  
  + Put wget.exe file into your Path  
  
#### Building sysroot environment  
You will use this sysroot for future building your application. This would take around haft hour to a few hours, depending on your hardware.  
```  
wget.exe -i download_list.txt --no-check-certificate  
pyqtdeploy-sysroot skeleton.json --verbose  
```  

#### Building sqlite3 lib 
In our project, we are using sqlite for storing our data. However, for Windows, the library that Python are using is kind of Dynamic Link Library (DLL), which is not really useful for us. So, we're going to build static link library for sqlite.

+ Navigate to https://www.sqlite.org/download.html and download latest amalgamation source version of SQLite.
+ Extract all the files into where ever you want in your hard drive.

+ Start the Developer Command Prompt for VS 2017
+ Go to the extracted folder
+ Run the following command to compile:
```
cl /c /EHsc sqlite3.c
lib sqlite3.obj
``` 
+ Copy the generated sqlite3.lib to your sysroot-win-32/lib folder
+ Copy the sqlite3.h to your sysroot-win-32/include folder
  
#### Fixing PyQt dynamic link library problem
There is one another problem with PyQt v5.13.0 for windows, It will try to
look for the Dynamic Link Library version of Qt5Core, whether or not we already have the static link library version of it. 
So, To fix this problem, open the sysroot-win-32/lib/python3.7/site-packages/PyQt5/\_\_init\_\_.py file, and comment out the `find_qt()` calling function

```
find_qt()
``` 
will become
```
#find_qt()
```
  
#### Build the application
  
#### Python versions problem  
In section Installing Python, I have mentioned that we have to install 3 versions of Python, and use the Python 3.7 64-bit for building. The reason for it is, for example:  
  
**If you missed the version 2.7,** then when you build the sysroot, it will throw an exception of:  
```  
Unable to find an installation of Python v2.7  
```  
_This happens because Python 2.7 is required for building PyQT for Windows._  
  **If you missed the version 3.7 32-bit**, then the exception would be:  
```  
Unable to find an installation of Python v3.7-32  
```  
Or, **if you missed the version 3.7 64-bit**, or not using python version 3.7 64-bit as running environment:
```  
Unable to find an installation of Python v2.7  
```
_This happens when you are trying to build a 32-bit application on a 64-bit machine. In pyqtdeploy/windows.py, it will try to search the installation path of Python from the Registry. However, if you try to run this script (by executing command pyqtdeploy-sysroot) using python 32-bit interpreter, then the system will try to look for the 32-bit Registry. And clearly, there will be nothing in there. That why you have to install and use Python 3.7 64-bit for building the sysroot._