# Author: Kyle Brooks
# Created: 18/05/2022
# Description: Small function to be able to define and store the QFF and LF modifiers. Window popup, 
import os
from libsimpa import *
from core_functions import *


class manager:
    def __init__(self):
        self.storeLFId=ui.application.register_event(self.storeLF)
        self.storeQFFId=ui.application.register_event(self.storeQFF)
    def getmenu(self,elementType,elementId,menu):
        el=ui.element(elementId)
        infos=el.getinfos()
        if infos["name"]=="Punctual receivers":
            submenu=[("QFF",self.storeQFFId),("LF",self.storeLFId)]
            menu.insert(0,("Store Corrections", submenu))
            return True
        else:
            return False

    def storeQFF(self,elementId):
        # Store QFF in each solve folder, parent of element ID
        el=ui.element(elementId)
        infos=el.getinfos()
        currentPath = ui.e_file(infos["parentid"])
        uiTitle="Store QFF Correction"
        freqRange={"a. 100 Hz":"0","b. 125 Hz":"0","c. 160 Hz":"0","d. 200 Hz": "0", "e. 250 Hz": "0", "f. 315 Hz":"0", "g. 400 Hz":"0","h. 500 Hz":"0","i. 630 Hz":"0","j. 800 Hz":"0","k. 1000 Hz":"0","l. 1250 Hz":"0","m. 1600 Hz":"0","n. 2000 Hz":"0","o. 2500 Hz":"0","p. 3150 Hz":"0","q. 4000 Hz":"0","r. 5000 Hz":"0","s. 6300 Hz":"0","t. 8000 Hz":"0","u. 10000 Hz":"0"}
        userInput1=ui.application.getuserinput(uiTitle,("Input QFF Data"), freqRange)
        if userInput1[0]:
            freq=('','100 Hz','125 Hz','160 Hz','200 Hz','250 Hz','315 Hz','400 Hz','500 Hz','630 Hz','800 Hz','1000 Hz','1250 Hz','1600 Hz','2000 Hz','2500 Hz','3150 Hz','4000 Hz','5000 Hz','6300 Hz','8000 Hz','10000 Hz')
            qff=list(userInput1[1].values())
            qff.insert(0,'QFF')
            saveData=[freq, qff]
            path=currentPath.buildfullpath()+"QFF_Correction.gabe"
            SaveFile(saveData, path)
            ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)

    def storeLF(self, elementId):
        # Store the LF in the SPPS folder, parent of parent of element ID
        el=ui.element(elementId)
        infos=el.getinfos()
        el2=ui.element(infos["parentid"])
        infos2=el2.getinfos()
        sppsId=ui.e_file(infos2["parentid"])
        currentPath = ui.e_file(sppsId)
        uiTitle="Store LF Correction"
        freqRange={"a. 100 Hz":"0","b. 125 Hz":"0","c. 160 Hz":"0","d. 200 Hz": "0", "e. 250 Hz": "0", "f. 315 Hz":"0", "g. 400 Hz":"0","h. 500 Hz":"0","i. 630 Hz":"0","j. 800 Hz":"0","k. 1000 Hz":"0","l. 1250 Hz":"0","m. 1600 Hz":"0","n. 2000 Hz":"0","o. 2500 Hz":"0","p. 3150 Hz":"0","q. 4000 Hz":"0","r. 5000 Hz":"0","s. 6300 Hz":"0","t. 8000 Hz":"0","u. 10000 Hz":"0"}
        userInput1=ui.application.getuserinput(uiTitle,("Input LF Data"), freqRange)
        if userInput1[0]:
            freq=('','100 Hz','125 Hz','160 Hz','200 Hz','250 Hz','315 Hz','400 Hz','500 Hz','630 Hz','800 Hz','1000 Hz','1250 Hz','1600 Hz','2000 Hz','2500 Hz','3150 Hz','4000 Hz','5000 Hz','6300 Hz','8000 Hz','10000 Hz')
            lf=list(userInput1[1].values())
            lf.insert(0,'LF')
            saveData=[freq, list(userInput1[1].values())]
            path=currentPath.buildfullpath()+"LF_Correction.gabe"
            SaveFile(saveData, path)
            ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)

ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location