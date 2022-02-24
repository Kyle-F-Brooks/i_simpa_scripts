import uictrl as ui
rootcore=ui.element(ui.application.getrootcore())
#Check if our mod has been already inserted
if rootcore.getelementbylibelle("mdf")==-1: #Then append our mod
    rootcore.appenduserelement(ui.element_type.ELEMENT_TYPE_CORE_CORE,"mdf","mdf")