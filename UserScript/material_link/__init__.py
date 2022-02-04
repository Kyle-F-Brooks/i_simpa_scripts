# Author: Kyle Brooks
# Created 02/02/2022

import libsimpa
import uictrl as ui

def getSurfaces(elementId):
    surfaceNames=[]
    surfaces=ui.element(elementId)
    for surface in surfaces.childs():
        surfaceNames.append(surface[2])
    return surfaceNames
def getUserMaterials(elementId):
    # need to find element ID of the materials Database. Won't be findable from the normal elementId
    materials=[]
    userMaterials=ui.element(elementId)
    for material in userMaterials.childs():
        materials.append(material)
        el=ui.element(material[0])
        infos=el.getinfos()
    return materials
def generateInputDict(surfaces, materials):
    inputDict={}
    materialId=[]
    for mat in materials:
        materialId.append(mat[2])
    for surface in surfaces:
        inputDict[surface]=materialId
    return inputDict

# elementId for surfaces is not consistent for all projects
class manager:
    def __init__(self):
        self.linkMaterialsId=ui.application.register_event(self.linkMaterials)
        self.getMatsId=ui.application.register_event(self.getMats)
    def getmenu(self,elementType,elementId,menu):
        el=ui.element(elementId)
        infos=el.getinfos()
        if infos['name']=="Surfaces":
            menu.insert(0,())
            menu.insert(0,(u"Link Materials (WIP)",self.linkMaterialsId))
            return True
        if infos["name"]=="User":
            menu.insert(0,())
            menu.insert(0,(u"Get Material Database ID(WIP)",self.getMatsId))
            return True
        else:
            return False
    def getMats(self,elementId,y):
        print(elementId)
    def linkMaterials(self,elementId,y):
        uiTitle="This function is a work in progress"
        userInput1=ui.application.getuserinput(uiTitle,"Input Material Element ID",{"Element ID":"0"})
        if userInput1[0]:
            surfaces=getSurfaces(elementId)
            materials=getUserMaterials(int(userInput1[1]["Element ID"]))
            print(surfaces)
            print(materials)
            inputDict=generateInputDict(surfaces,materials)
            print(inputDict)
            userInput2=ui.application.getuserinput(uiTitle,"Match Surface to Area",inputDict)
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_GROUPESURFACES, manager())
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_USER, manager())