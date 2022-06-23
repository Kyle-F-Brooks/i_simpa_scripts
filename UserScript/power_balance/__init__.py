# Author: Kyle Brooks
# Created: 24/05/2022
# Description: Script to calculate the power balance

import uictrl as ui
from libsimpa import *
from core_functions import *
import math

def calcPowerBalance(excitationSPL, areas, projArea, materials, lf, qff):
    # materials is an array of array of material stl has to be same length as areas
    H=0.000000000001
    excitationIntensityW=[]
    for freq in excitationSPL:
        intesnsityDb=float(freq)-6
        excitationIntensityW.append((math.pow(10, (intesnsityDb/10))*H))
    adjacentPowersW=[]
    adjacentPowersdB=[]
    totalArea=0
    for area in areas:
        adjacentPowerW=[]
        adjacentPowerdB=[]
        for freq in excitationIntensityW:
            excInt=freq*float(area)
            adjacentPowerW.append(excInt)
            adjacentPowerdB.append((10*math.log10((excInt/H))))
        adjacentPowersW.append(adjacentPowerW)
        adjacentPowersdB.append(adjacentPowerdB)
        totalArea+=float(area)
    totalPower=[]
    for freq in excitationIntensityW:
        totalPower.append(freq*totalArea)
    materialsQff=[]
    for material in materials:
        materialQff=[]
        for k,v in enumerate(material):
            materialQff.append(v+qff[k])
        materialsQff.append(materialQff)
    radiatedPowersdB=[]
    radiatedPowersW=[]
    for k1,v1 in adjacentPowersdB:
        radiatedPowerdB=[]
        radiatedPowerW=[]
        for k2,v2 in enumerate(v1):
            rPdB=v2-materialsQff[k1][k2]
            rPw=(math.pow(10,(rPdB/10))*H)
            radiatedPowerdB.append(rPdB)
            radiatedPowerW.append(rPw)
        radiatedPowersdB.append(radiatedPowerdB)
        radiatedPowersW.append(radiatedPowerW)
    totalPowerW=[]
    totalPowerdB=[]
    for k1,v1 in enumerate(radiatedPowersW):
        for k2, v2 in enumerate(v1):
            totalPowerW[k2]+=v2
    for watt in totalPowerdB:
        totalPowerdB.append(10*math.log10(watt/H))
    projIntensity=[]
    for intensity in totalPowerdB:
        projIntensity.append(10*math.log10((intensity/projArea)/H))
    overallTransmissionLoss=[]
    for k,v in enumerate(projIntensity):
        overallTransmissionLoss.append(excitationSPL[k]-v)
    overallTLLF=[]
    for k,v in enumerate(overallTransmissionLoss):
        overallTLLF.append(lf[k]+v)
    return overallTransmissionLoss, overallTLLF, projIntensity, totalPowerdB, totalPowerW

def getIds(sceneId):
    matId=0 # needs both user and standard material data
    surfacesId=0
    for treeItem in ui.element(sceneId).childs():
        # Surface
        if treeItem[1]==ui.element_type.ELEMENT_TYPE_SCENE_DONNEES:
            for data in ui.element(treeItem[0]).childs():
                if data[1]==ui.element_type.ELEMENT_TYPE_SCENE_GROUPESURFACES:
                    surfacesId=data[0]
        # Materials
        elif treeItem[1]==ui.element_type.ELEMENT_TYPE_SCENE_PROJET:
            for project in ui.element(treeItem[0]).childs():
                if project[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD:
                    for database in ui.element(project[0]).childs():
                        if database[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX:
                            matId=database[0]
        else:
            print("Incorrect Scene ID")
    return matId, surfacesId

def getAreas(surfacesId):
    # need to copy the element in the tree, creates the value for aire
    # each boot up needs a fresh element copy
    areas=[]
    surfaceNames=[]
    for surface in ui.element(surfacesId).childs():
        if surface[1] == ui.element_type.ELEMENT_TYPE_SCENE_GROUP_SURFACES_GROUPE:
            area=ui.element(surface[0].getdecimalconfig("aire"))
            surfaceNames.append(surface[2])
            areas.append(area)
    return areas, surfaceNames

def getMaterials(matsId): # get the list of all materials related to the project
    # chose material from database for each surface
    # if element type is ELEMENT_TYPE_SCENE_BDD_MATERIAUX_APP, ELEMENT_TYPE_SCENE_BDD_MATERIAUX_USER
    userMats=[]
    appMats=[]
    for materials in ui.element(matsId).childs():
        if materials[1] == ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_APP:
            for materialGroup in ui.element(materials[0]).childs():
                for material in ui.element(materialGroup[0]).childs():
                    matName=material[2]
                    matAbsorp=[]
                    for attribute in ui.element(material[0]).childs():
                        if attribute[1]==ui.element_type.ELEMENT_TYPE_MATERIAU_APP:
                            for freq in ui.element(attribute[0]).childs():
                                matAbsorp.append(ui.element(freq[0]).getdecimalconfig("absorb"))
        elif materials[1] == ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_USER:
            for materialGroup in ui.element(materials[0]).childs():
                for material in ui.element(materialGroup[0]).childs():
                    matName=material[2]
                    matAbsorp=[]
                    for attribute in ui.element(material[0]).childs():
                        if attribute[1]==ui.element_type.ELEMENT_TYPE_MATERIAU_USER:
                            for freq in ui.element(attribute[0]).childs():
                                matAbsorp.append(ui.element(freq[0]).getdecimalconfig("absorb"))
                    matAbsorp.insert(0,matName)
                    userMats.append(matAbsorp)
    return userMats, appMats

class manager:
    def __init__(self):
        self.calcPowerBalanceId=ui.application.register_event(self.runCalculation)
        self.getSceneId=ui.application.register_event(self.getScene)
    def getmenu(self,elementType,elementId,menu):
        # create the menu items
        el=ui.element(elementId)
        infos=el.getinfos()
        if infos["name"]=="Transmission Loss":
            menu.insert(2,("Create Power Balance",self.calcPowerBalanceId))
            return True
        if infos["name"]=="Data" or infos["name"]=="Project":
            menu.insert(4,("Get Scene ID", self.getSceneId))
            menu.insert(4,())
            return True
        else:
            return False
    def getScene(self,elementId):
        # display the scene tab Id to allow it to be input to find the surface and material database
        sceneId=ui.element(elementId).getinfos()["parentid"]
        print("Scene ID: %s" % sceneId)
    def runCalculation(self,elementId):
        el=ui.element(elementId)
        infos=el.getinfos()
        punctualId=infos["parentid"]
        solveId=ui.element(punctualId).getinfos()["parentid"]
        sppsId=ui.element(solveId).getinfos()["parentid"]
        uiTitle="Power Balance Calculator"
        names=getNames(punctualId)
        userInput1=ui.application.getuserinput(uiTitle, "Pick the excitation Receiver", {"Excitation": names, "Scene ID": 0})
        if userInput1[0]:
            matId, surfacesId = getIds(userInput1[1]["Scene ID"])
            excRecName=userInput1[1]["Excitation"]
            excitationSPL=[]
            qff,lf=GetBothCorrection(sppsId,solveId)
            areas,surfaceNames=getAreas(surfacesId) # areas format [[][][][]]
            projArea=0 # have projected area be input by the user
            materials=getMaterials(matId) # materials format [[][][][][][]]
            overallTransmissionLoss, overallTLLF, projIntensity, totalPowerdB, totalPowerW=calcPowerBalance(excitationSPL,areas,projArea,materials,lf,qff)


ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_DONNEES,manager())
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_PROJET,manager())