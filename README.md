# I-Simpa Scripts
Author: Kyle Brooks

Modified Scripts: convert_all_tool, recp_res_tool, source_tools, libsimpa

Custom Scripts: plot_xyz, stl_calc, absorption_calc

Please check my other repositories for the python 2 scripts

Test scripts have been moved to a seperate branch
## Description
A repository of python scripts written to make using funtions in I-Simpa easier

## Installation
Each folder contains the required files to run the tools within I-Simpa 1.3.4 with the Python 3.8 Interperator. 
**Administrator controls are required to install any of these tools**

1. Download the desired tools by pressing the "Code" button at the top of the screen and then "Download ZIP"
2. Open the I-Simpa folder usually located at C:\Program Files\I-SIMPA\UserScript
3. Paste the tool folder into the user script folder **Note:** recp_res_tool goes into the ..\I-SIMPA\SystemScript folder and replaces the one already contained within.
4. Reboot any open instances of I-Simpa 

## libsimpa
The libsimpa file has to be modified for Python 3 in order for the recp_res_tool to work. Paste the file into C:\Program Files\I-SIMPA\libsimpa. Handles the communication between python and c++.

## all_reciever_tool
This tool is used to enable and disable the name tags on each punctual reciever to make viewing of the model easier.
Directivity Lines can be removed but not re-enabled, this does not have an effect on the final result.

## convert_all_tool
An edited version of a script that converts the gabe format files into csv. The changes made, allow it to be used with python 3 as in the latest version of I-Simpa. 

## source_tools
Normally packaged with the software. Edited to remove all source names without disabling the sources

## recp_res_tool
Combines each value of a chosen measurement into a single file to allow for easier processing of data. Each file gets saved in a folder called "Fused Recievers" and the file name is appended with the measurement that was chosen. The alterations from python 2 -> 3 mean that this doesn't currently work on install alone. Replacement of the libsimpa file is required with the one available in the repository.

## absorption_calc
Calculates the Absorption Coefficient and the Sabine absorption, uses the early decay time(EDT)

## plot_xyz
Used to convert a grid of microphone data into a readable format for plotting libraries such as d-plot

## stl_calc
Calculates the Transmission loss, based on having an excitation receiver.

### Possible Features
* STL Hologram
* Store and return to set camera positions
* Custom Material Import: CATT Acoustic/li8 Odeon