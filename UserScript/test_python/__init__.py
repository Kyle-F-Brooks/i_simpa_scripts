# -*- coding: cp1252 -*-
import uictrl as ui
import libsimpa
import csv
import os

# this document is currently a test workspace and does not have any real function

def transmision_loss_calc():
    # STL = SPLex - 6 - avgSPL + QFF
    print("Hello")

# def open_as_csv(folderwxid):
#     folder=ui.element(folderwxid)
#     for el in folder.childs():
#         # print(el)
#         if el[1] == ui.element_type.ELEMENT_TYPE_REPORT_FOLDER:
#             open_as_csv(el[0])
#         elif el[1] in [ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECP, ui.element_type.ELEMENT_TYPE_REPORT_GABE, ui.element_type.ELEMENT_TYPE_REPORT_GABE_GAP, ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECPS]:
#             document = ui.e_file(el[0])
#             gabedoc=ui.application.getdataarray(document)
            # for row in gabedoc:
                # print(row)
            # path = document.buildfullpath().replace(".gabe",".csv")
            # with open(path.encode('cp1252'), 'w') as csvfile:
            #     writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #     for row in gabedoc:
            #         writer.writerow(row)

class manager:
    def __init__(self):
        self.testFuncid=ui.application.register_event(self.testFunc)
    def getmenu(self,typeel,idel,menu):
        el=ui.element(idel)
        infos=el.getinfos()
        menu.insert(0,())
        menu.insert(0,(u"Test Code",self.testFuncid))
        return True
        
    def OnConvertAll(self,idel):
        transmision_loss_calc()
        input1=(u"First Input Data")
        input2=(u"Second Input Data")
        input3=(u"Third Input Data")

        res=ui.application.getuserinput((u"This pop-up currently has no function"),(u"Input random number values"),{ input1 : "0",input2 : "0",input3 : "0",})
        # open_as_csv(idel)
        ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER) #refreshes folder in ui tree
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location