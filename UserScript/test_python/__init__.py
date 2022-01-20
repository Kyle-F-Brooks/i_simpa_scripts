# -*- coding: cp1252 -*-
import re
import uictrl as ui
import libsimpa
import csv
import os

# this document is currently a test workspace and does not have any real function

"""test a function to fetch the name of each reciever, out into a dict and display them to be selected in a pop up window"""

# def transmision_loss_calc():
    # STL = SPLex - 6 - avgSPL + QFF
    # print("Hello")

def testFunction(folderwxid):
    # target refers to the measurement type desired for output
    folder=ui.element(folderwxid)
    for el in folder.childs():
        if el[1] == ui.element_type.ELEMENT_TYPE_REPORT_FOLDER:
            testFunction(el[0])
        elif el[1] in [ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECP, ui.element_type.ELEMENT_TYPE_REPORT_GABE, ui.element_type.ELEMENT_TYPE_REPORT_GABE_GAP, ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECPS]:
            document = ui.e_file(el[0])
            if document.getinfos()["name"]=="fusionSPL":
                gridparam=ui.application.getdataarray(document)
                for row in gridparam:
                    print(row)

class manager:
    def __init__(self):
        self.testFuncid=ui.application.register_event(self.testFunc)
    def getmenu(self,typeel,idel,menu):
        el=ui.element(idel)
        infos=el.getinfos()
        if infos["name"]==u"Punctual receivers":
            menu.insert(0,())
            menu.insert(0,(u"Test Code",self.testFuncid))
            return True
        else:
            return False
        
    def testFunc(self,idel):
        # transmision_loss_calc()
        input1=u"Please Pick a Receiver"
        testFunction(idel)
        # res=ui.application.getuserinput((u"This pop-up currently has no function"),(u"Pick a Reciever from the list"),{input1 : "0"})

        # open_as_csv(idel)
        # ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER) #refreshes folder in ui tree
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location