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
2. Open the I-Simpa folder usually located at C:\Program Files\I-SIMPA\
3. Paste the UserScript, SystemScript and libsimpa folders that were downloaded into C:\Program Files\I-SIMPA\ and choose to replace any other versions
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

## source_contributions
Used to get the specific source contribution for each microphone and output a file for each source with the spl reading at each receiver

## plot_xyz
Used to convert a grid of microphone data into a readable format for plotting libraries such as d-plot, can read the output of the source contributions and Transmission Loss

## stl_calc
Calculates the Transmission loss, based on having an excitation receiver.

## var_input
Takes the QFF and LF as inputs, saving them as gabe files. Makes the files accessible for stl_calc.

## material_link (WIP)
this function is currently not imported into I-simpa. It has an issue regarding the source code.

## power_balance (WIP)
calculates the power balance based on the area, the projected area and the source power.

## core_functions (WIP)
a collection of functions that are used repeatedly by other scrzipts.

### Possible Features
* STL Hologram
* Store and return to set camera positions
* Custom Material Import: CATT Acoustic/li8 Odeon
