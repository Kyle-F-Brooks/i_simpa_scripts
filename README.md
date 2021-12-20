# I-Simpa Scripts
Author: Kyle Brooks

## Description
A repository of python scripts written to make using funtions in I-Simpa easier

## Installation
Each folder contains the required files to run the tools within I-Simpa 1.3.4 with the Python 3.8 Interperator. 
**Administrator controls are required to install any of these tools**

1. Download the desired tools
2. Open the I-Simpa folder usually located at C:\Program Files\I-Simpa\UserScript
3. Paste the tool folder into the user script folder
  * **Note:** recp_res_tool goes into the ..\I-Simpa\SystemScript folder and replaces the one already contained within.
4. Reboot any open instances of I-Simpa 

## all_reciever_tool
This tool is used to enable and disable the name tags on each punctual reciever to make viewing of the model easier.
### Planned Changes
* Removable Directivity Lines

## convert_all_tool
An edited version of a script that converts the gabe format files into csv. The changes made allow it to be used with python 3 as in the latest version of I-Simpa. 

## recp_res_tool
Combines each value of a chosen measurement into a single file to allow for easier processing of data. Each file gets saved in a folder called "Fused Recievers" and the file name is appended with the measurement that was chosen. 

## test_python 
currently under development.
### Possible Features
* STL Calculation
* STL Hologram
* Store and return to set camera positions
