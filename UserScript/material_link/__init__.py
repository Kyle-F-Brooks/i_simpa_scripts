# Author: Kyle Brooks
# Created 02/02/2022

import libsimpa
import uictrl as ui

class manager:
    def __init__(self):
        self.linkMaterialsId=ui.application.register_event(self.linkMaterials)
    def getmenu(self,elementType,elementId,menu):
        el=ui.element(elementId)
        infos=el.getinfos()
        menu.insert(0,())
        menu.insert(0,(u"Link Materials (WIP)",self.linkMaterialsId))
        # if infos["name"]==u"Surfaces": # only display menu on Punctual receivers file
        #     menu.insert(0,())
        #     menu.insert(0,(u"Link Materials (WIP)",self.linkMaterialsId))
        #     return True
        # else:
        #     return False
        return True
    def linkMaterials(self):
        print("This Function is a WIP")
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_GROUPESURFACES, manager())