# Author: Kyle Brooks
# Created: 09/12/21

import uictrl as ui

class manager:
    def __init__(self):
        self.enable_reciever_namesid=ui.application.register_event(self.enable_reciever_names)
        self.disable_reciever_namesid=ui.application.register_event(self.disable_reciever_names)

    def getmenu(self,typeel,idel,menu):
        submenu=[]
        submenu.append((u"Enable Names", self.enable_reciever_namesid))
        submenu.append((u"Disable Names", self.disable_reciever_namesid))
        menu.insert(2,(u"Reciever Names", submenu))
        return True

    def enable_reciever_names(self, idgrp):
        self.set_reciever_activation(idgrp, True)

    def disable_reciever_names(self, idgrp):
        self.set_reciever_activation(idgrp, False)
    
    def set_reciever_activation(self,idgrp,newstate):
        grpsrc=ui.element(idgrp)
        all_property=grpsrc.getallelementbytype(ui.element_type.ELEMENT_TYPE_SCENE_RECEPTEURSP_RECEPTEUR_RENDU) 
        for prop in all_property:
            ui.element(prop).updateboolconfig("showlabel",newstate)

ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_RECEPTEURSP, manager())