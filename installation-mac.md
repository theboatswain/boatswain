# Boatswain installation for MacOS
This instruction is applied for pyqtdeploy version 2.4 and Python version 3.7
#### Preparation
Make sure you have the following libraries installed:
+ Python version 3.7.x
+ Command Line Developer Tools
#### Installing dependencies  
+ Go to the project's directory  
+ Create an environment for your project:   
```  
pip install virtualenv  
virtualenv venv  
source venv/bin/activate  
```  
+ Install project's dependencies: `pip install -r requirements.txt`  
+ Install pyqtdeploy: `pip install pyqtdeploy`  

#### Install sysroot
`wget -i download_list.txt`

After all dependency libraries are downloaded, run the following command to build sysroot:

`pyqtdeploy-sysroot skeleton.json --verbose > output.log` 

#### Build the application
```
chmod +x scripts/compile-macos-64.sh
./scripts/compile-macos-64.sh
```
After finishing the script, the application bundle will be located in the _release/macos_ folder