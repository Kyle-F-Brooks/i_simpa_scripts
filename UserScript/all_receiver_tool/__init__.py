# Author: Kyle Brooks
# Created: 09/12/21
# Modified:20/12/21

# This tool is used to enable and disable the name tags on each punctual reciever to make viewing of the model easier.
# Directivity Lines can now be hidden but not re-enabled.
import uictrl as ui

def set_direc_display(idgrp):
    # Sets the directivity bar to zero meaning it no longer shows. Cannot toggle it back on
    grpsrc=ui.element(idgrp)
    all_property=grpsrc.getallelementbytype(ui.element_type.ELEMENT_TYPE_SCENE_RECEPTEURSP_RECEPTEUR_PROPRIETES) 
    for prop in all_property:
        # edits "Direction X", "Direction Y" & "Direction Z"
        ui.element(prop).updatedecimalconfig("u",0) #X
        ui.element(prop).updatedecimalconfig("v",0) #Y
        ui.element(prop).updatedecimalconfig("w",0) #Z

def set_reciever_activation(idgrp,newstate):
    # depending on input, will show or hide the name label
    grpsrc=ui.element(idgrp)
    all_property=grpsrc.getallelementbytype(ui.element_type.ELEMENT_TYPE_SCENE_RECEPTEURSP_RECEPTEUR_RENDU) 
    for prop in all_property:
        ui.element(prop).updateboolconfig("showlabel",newstate)

class manager:
    def __init__(self):
        # register events for menu buttons 
        self.enable_reciever_namesid=ui.application.register_event(self.enable_reciever_names)
        self.disable_reciever_namesid=ui.application.register_event(self.disable_reciever_names)
        self.disable_direc_dispid=ui.application.register_event(self.disable_direc_disp)

    def getmenu(self,typeel,idel,menu):
        # create menu buttons and link them to their functions
        submenu=[]
        submenu.append((u"Enable Names", self.enable_reciever_namesid))
        submenu.append((u"Disable Names", self.disable_reciever_namesid))
        menu.insert(2,(u"Reciever Names", submenu))
        menu.insert(3,(u"Remove Directivity Lines", self.disable_direc_dispid))
        return True

    def enable_reciever_names(self, idgrp):
        set_reciever_activation(idgrp, True)

    def disable_reciever_names(self, idgrp):
        set_reciever_activation(idgrp, False)
        
    def disable_direc_disp(self, idgrp):
        set_direc_display(idgrp)

ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_RECEPTEURSP, manager())