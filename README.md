
  
<img src="https://raw.githubusercontent.com/theboatswain/boatswain/DevMaster/images/boatswain.png" width="500" />    
  
Boatswain is an open source, multiple platforms application that managing your docker containers in an easiest manner. The ultimate goal of this project is to help you to minimise the number of applications that you would need to install separately into your machine, instead, grouping all of them into one single place. And, in the same time, providing you a modern, easy to use User Interface, which allowing you to focus on the things that important to you.  
  
## Build status:  
  
[![Build Status](https://travis-ci.com/theboatswain/boatswain.svg?branch=master)](https://travis-ci.com/theboatswain/boatswain)  
  
## Introduction  
  
From the main UI of Boatswain, you can easily add or remove your docker containers, configure your port mapping, volume mapping, setting up your environment variables, overwrite your container's entrypoint, etc. You can also create and map a config shortcut to the main UI for easier configuration, or may be just for conventional visualisation.   
<img align="right" src="https://raw.githubusercontent.com/theboatswain/boatswain/DevMaster/images/main-app-cross.png" width="280" />    
  
Boatswain also allows you to group your containers together (i.e web stack, log stack, etc), or managing multiple workspaces (i.e home workspace or project X), switching between workspaces, checking container logs with our built-in log viewer, opening container's terminal, filtering your containers, etc. You can also expand your container/group when you need to change or check some informations, or collapse it once it's done.   

Boatswain is designed to make sure you can work with your containers as easily as possible. That why we introduce the preferences shortcut feature, which allows you to map your configurations into the main UI so then you can access it directly afterward. You also can import/export your preferences shortcut, or share it with us so then everyone can benefit from your work when they install the container. 
  
Boatswain is built from PyQT and applied pyqtdeploy technique for building release, so, the final release application are both lightweight and as fast as any native application. While maintaining the same user experiences between multiple platforms, including MacOS, Windows and Linux.  
  
Boatswain also comes with our open source, cross platform [Auto Updater](https://github.com/theboatswain/boatswain_updater)  to make sure your machine is always up to date with the newest version of Boatswain. If you want to integrate this feature into your project, don't hesitate to check it out at  https://github.com/theboatswain/boatswain_updater  
  
## Installation  
[Download the latest version](https://github.com/theboatswain/boatswain/releases) of Boatswain via the github release page.  
  
## Documentation  
Boatswain's documentation, user guide and other informations can be found at [https://github.com/theboatswain/boatswain/wiki](https://github.com/theboatswain/boatswain/wiki)  
  
## Building Boatswain  
Boatswain can be compiled and used on MacOS, Linux and Windows, both 32 bit and 64 bit systems. Details about how to compile from source can be found at [installation-mac.md](https://github.com/theboatswain/boatswain/blob/master/installation-mac.md) for MacOS,  [installation-debian.md](https://github.com/theboatswain/boatswain/blob/master/installation-debian.md) for Debian  and [installation-win.md](https://github.com/theboatswain/boatswain/blob/master/installation-win.md)  for Windows. Other Linux distributions can refer to [installation-debian.md](https://github.com/theboatswain/boatswain/blob/master/installation-debian.md) for generic instructions.  

## Preferences shortcut contributing  
Preferences shortcut is a feature to allow you to share your docker's configuration shortcut to everyone that are using Boatswain. By default, when you install any docker container with Boatswain, we will check if there is any preferences shortcut already there in our [default repo](https://github.com/theboatswain/preferences-shortcut). If yes then it will be installed automatically as well. So, if you want to share your's to us then please check [https://github.com/theboatswain/preferences-shortcut](https://github.com/theboatswain/preferences-shortcut) for how to contribute your preferences shortcut.

## Code contributions  
Note: by contributing code to the Boatswain project in any form, including sending a pull request via Github, a code fragment or patch via private email or public discussion groups, you agree to release your code under the terms of the GNU GPLv3 license that you can find in the [LICENSE](https://github.com/theboatswain/boatswain/blob/master/LICENSE)) file included in the Boatswain source distribution.  
  
Please see the [CONTRIBUTING.md](https://github.com/theboatswain/boatswain/blob/master/CONTRIBUTING.md) file in this source distribution for more information.  
  
## Copyright and License  
Code released under the [GNU GPL v3 license](https://github.com/theboatswain/boatswain/blob/master/LICENSE)