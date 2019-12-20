# Boatswain installation for linux
## Preparation
Make sure you have the following libraries installed:
+ Python version 3.7+
+ Package libssl-dev installed
+ Package libsqlite3-dev installed
## Install sysroot
`wget -i download_list.txt`

After all dependency libraries are downloaded, run the following command to build sysroot:

`pyqtdeploy-sysroot skeleton.json` 
