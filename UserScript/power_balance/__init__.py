# Author: Kyle Brooks
# Created: 24/05/2022
# Description: Script to calculate the power balance

import uictrl as ui
from libsimpa import *
from core_functions import *




class manager:
    def __init__(self) -> None:
        self.calcPowerBalanceId=ui.application.register_event(self.calcPowerBalance)
    def getmenu(self,elementType,elementId,menu):
        el=ui.element(elementId)
        infos=el.getinfos()
        if infos["name"]=="Transmission Loss":
            menu.insert(0,("Create Power Balance",self.calcPowerBalanceId))
            return True
        else:
            return False
    def calcPowerBalance(self,elementId):
        pass