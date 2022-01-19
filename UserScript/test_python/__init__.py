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

def GetMixedLevel(folderwxid):#, target):
    # target refers to the measurement type desired for output
    cols=[]
    folder=ui.element(folderwxid)
    recplist=folder.getallelementbytype(ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECP)
    for idrecp in recplist: # for each punctual receiver in folder "Punctual receivers"
        recp=ui.element(idrecp)
        # once the spps is calculated a file named "Sound level" will be in the Project > Results tree
        if recp.getinfos()["name"]=="fusionSPL":
            # get the acoustics parameters file    
            pere=ui.element(recp.getinfos()["parentid"])
            nomrecp=pere.getinfos()["label"]
            params=ui.element(pere.getelementbylibelle('Acoustic parameters'))
            gridparam=ui.application.getdataarray(params)
            print(gridparam)
            if len(cols)==0: # with array cols empty 
            #     cols.append(next(zip(*gridparam))) # add frequency row
                idcol=gridparam[0].index("200") # set target column equal to the target title
            # cols.append([nomrecp]+list(list(zip(*gridparam))[idcol][1:])) # add data from reciever to new row
            print([nomrecp]+list(list(zip(*gridparam))[idcol][1:])) # add data from reciever to new row
    return cols

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
        GetMixedLevel(idel)
        # res=ui.application.getuserinput((u"This pop-up currently has no function"),(u"Pick a Reciever from the list"),{input1 : "0"})

        # open_as_csv(idel)
        # ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER) #refreshes folder in ui tree
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location