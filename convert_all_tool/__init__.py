# -*- coding: cp1252 -*-
# Modified: Kyle Brooks
# Created/Modified: 30/11/21

import uictrl as ui
import libsimpa
import csv
import os

def do_convert_all(folderwxid):
    folder=ui.element(folderwxid)
    for el in folder.childs():
        # print(el)
        if el[1] == ui.element_type.ELEMENT_TYPE_REPORT_FOLDER:
            do_convert_all(el[0])
        elif el[1] in [ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECP, ui.element_type.ELEMENT_TYPE_REPORT_GABE, ui.element_type.ELEMENT_TYPE_REPORT_GABE_GAP, ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECPS]:
            document = ui.e_file(el[0])
            gridparam=ui.application.getdataarray(document)
            path = document.buildfullpath().replace(".gabe",".csv")
            with open(path.encode('cp1252'), 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in gridparam:
                    writer.writerow(row)
class manager:
    def __init__(self):
        self.OnConvertAllid=ui.application.register_event(self.OnConvertAll)
    def getmenu(self,typeel,idel,menu):
        el=ui.element(idel)
        infos=el.getinfos()
        menu.insert(0,())
        menu.insert(0,(u"Convert all files in sub-directories to CSV",self.OnConvertAllid))
        return True
        
    def OnConvertAll(self,idel):
        print("\nCSV Conversion: Processing")
        do_convert_all(idel)
        ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)
        print("\nCSV Conversion: Complete")
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager())
