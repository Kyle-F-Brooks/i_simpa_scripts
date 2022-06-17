# Author: Kyle Brooks
# Created: 30/05/2022
# Description: A group of scripts for dev purposes only

import uictrl as ui
from libsimpa import *
from core_functions import *

class manager:
    def __init__(self):
        self.showEl=ui.application.register_event(self.showId)
        self.showPaEl=ui.application.register_event(self.showParentId)
    def getmenu(self, elementType, elementId, menu):
        submenu=[("Show Info",self.showEl),("Show Parent Info",self.showPaEl)]
        menu.insert(0,("dev Tools",submenu))
        return True
    def showId(self,elementId):
        infos=ui.element(elementId).getinfos()
        print(infos)
    def showParentId(self,elementId):
        infos=ui.element(elementId).getinfos()
        print(ui.element(infos["parentid"]).getinfos())

# ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager())
# ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_ROOT,manager())
# ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_GROUPESURFACES,manager())
# ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_RECEPTEURSP,manager())
# ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX, manager())
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_DONNEES,manager())
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_PROJET,manager())
# ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE,manager())
# ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE,manager())
# ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE,manager())
