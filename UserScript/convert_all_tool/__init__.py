# -*- coding: cp1252 -*-
# Modified: Kyle Brooks
# Created/Modified: 30/11/21

# An edited version of a script that converts the gabe format files into csv.
# The changes made, allow it to be used with python 3 as in the latest version of I-Simpa.

import uictrl as ui
import libsimpa
import csv
import os

def do_convert_all(elementId):
    # takes the gabe file and outputs it as a csv
    folder=ui.element(elementId)
    for el in folder.childs():
        if el[1] == ui.element_type.ELEMENT_TYPE_REPORT_FOLDER:
            do_convert_all(el[0])
        elif el[1] in [ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECP, ui.element_type.ELEMENT_TYPE_REPORT_GABE, ui.element_type.ELEMENT_TYPE_REPORT_GABE_GAP, ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECPS]:
            document = ui.e_file(el[0])
            gridparam=ui.application.getdataarray(document)
            path = document.buildfullpath().replace(".gabe",".csv")
            with open(path.encode('cp1252'), 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in gridparam:
                    writer.writerow(row)
class manager:
    def __init__(self):
        # register function for menu button
        self.OnConvertAllid=ui.application.register_event(self.OnConvertAll)
    def getmenu(self,elementType,elementId,menu):
        # create and link the menu button with its function
        el=ui.element(elementId)
        infos=el.getinfos()
        menu.insert(0,())
        menu.insert(0,(u"Convert all files in sub-directories to CSV",self.OnConvertAllid))
        return True
        
    def OnConvertAll(self,elementId):
        do_convert_all(elementId) # call conversion function
        ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER) # reload folders to make new files visible
        print("\nCSV Conversion: Complete") # prints to python console
# register new button in program and tell it where to make it available
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager())
