# Author: Kyle Brooks
# Created 02/02/2022

import libsimpa
import uictrl as ui

def getSurfaces(elementId):
    surfaceNames=[]
    surfaces=ui.element(elementId)
    for surface in surfaces.childs():
        surfaceNames.append(surface[2])
def getUserMaterials(elementId):
    # need to find element ID of the materials Database. Won't be  findable from the normal elementId
    materials=[]
    userMaterials=ui.element(elementId)
    for material in userMaterials:
        print(material)
    return materials
def generateInputDict(surfaces, materials):
    inputDict={}
    for surface in surfaces:
        inputDict.update({surface:materials})
    return inputDict

class manager:
    def __init__(self):
        self.linkMaterialsId=ui.application.register_event(self.linkMaterials)
    def getmenu(self,elementType,elementId,menu):
        el=ui.element(elementId)
        infos=el.getinfos()
        menu.insert(0,())
        menu.insert(0,(u"Link Materials (WIP)",self.linkMaterialsId))
        return True
    def linkMaterials(self,elementId,y):
        print("This Function is a WIP")
        getSurfaces(elementId)
        uiTitle="This function is a work in progress"
        userInput1=ui.application.getuserinput(uiTitle,"Match Surface to Area",{"List of Surfaces":"Array of Materials"})
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_GROUPESURFACES, manager())