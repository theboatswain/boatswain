# Boatswain installation for linux
This instruction is applied for pyqtdeploy version 2.4 and Python version 3.7.

Tested on Ubuntu 18.04.3, Ubuntu 19.10, Elementary 5.0
#### Preparation
Make sure you have the following libraries installed:
+ Python version 3.7+
+ Package libssl-dev, libffi-dev, libfontconfig-dev, libsqlite3-dev, libxkbcommon-x11-dev installed
```bash
sudo apt install libssl-dev libffi-dev libfontconfig-dev libsqlite3-dev libxkbcommon-x11-dev
```
#### Installing dependencies  
+ Go to the project's directory  
+ Create an environment for your project:   
```  
pip3 install virtualenv  
virtualenv venv  
source venv/bin/activate  
```  
+ Install project's dependencies: `pip3 install -r requirements.txt`  
+ Install pyqtdeploy: `pip3 install pyqtdeploy`  

#### Install sysroot
Download all dependencies:
`wget -i download_list.txt`

After all dependency libraries are downloaded, run the following command to build sysroot:

`pyqtdeploy-sysroot skeleton.json --verbose > output.log` 

#### Optional packages
+ FPM - fpm is a tool to help us to build .deb and .rpm packages. Refer to https://fpm.readthedocs.io/en/latest/installing.html for installing instruction

+ RPM - rpm is a library for helping us to build rpm package `suto apt install rpm`

#### Build the application
```
chmod +x scripts/compile-linux-64.sh
./scripts/compile-linux-64.sh
```
After finishing the script, the application folder will be located in the _release/linux_ folder, along with .deb and .rpm packages