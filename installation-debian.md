# Boatswain installation for linux
This instruction is applied for pyqtdeploy version 2.4 and Python version 3.7
## Preparation
Make sure you have the following libraries installed:
+ Python version 3.7+
+ Package libssl-dev installed
+ Package libsqlite3-dev installed
+ Run the following command for building deps: `sudo apt-get build-dep qt5-default`
## Install sysroot
`wget -i download_list.txt`

After all dependency libraries are downloaded, run the following command to build sysroot:

`pyqtdeploy-sysroot skeleton.json` 
