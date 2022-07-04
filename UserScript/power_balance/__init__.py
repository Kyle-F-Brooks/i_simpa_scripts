# Author: Kyle Brooks
# Created: 24/05/2022
# Description: Script to calculate the power balance

from ast import Pass
import uictrl as ui
from libsimpa import *
from core_functions import *
import math

print("In order to run the power balance calculation,\n each surface needs to be right clicked and copied.")
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
    matId=0 # ID of the "Materials" item in "Project" tree
    surfacesId=0 # ID of the "Surfaces" item in "Data" tree
    exists=False # check if elements exist
    for treeItem in ui.element(sceneId).childs(): # for each item in "Scene" Tree
        # Surface
        if treeItem[1]==ui.element_type.ELEMENT_TYPE_SCENE_DONNEES: # if element type Data
            exists=True
            for data in ui.element(treeItem[0]).childs(): # for each time in data tree
                if data[1]==ui.element_type.ELEMENT_TYPE_SCENE_GROUPESURFACES: # if element type is group of surfaces
                    surfacesId=data[0] # store the ID of surfaces item
        # Materials
        elif treeItem[1]==ui.element_type.ELEMENT_TYPE_SCENE_PROJET: # if element type project
            exists=True
            for project in ui.element(treeItem[0]).childs(): # for each item in project tree
                if project[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD: # if the item is element type bdd(project database)
                    for database in ui.element(project[0]).childs(): # for each item in project database
                        if database[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX: # if item is element "Materials"
                            matId=database[0] # store the ID of materials item
        elif not exists: # if elements do not exist, the wrong value has been input
            print("Incorrect Scene ID\nRight click on Project or Data in the Scene window")
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

def getMaterials(matsId):
    materials=[]
    materialNames=[]
    for materialsGroups in ui.element(matsId).childs():
        if materialsGroups[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_APP:
            for materialGroup in ui.element(materialsGroups[0]).childs():
                if materialGroup[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_APP_GROUP:
                    for material in ui.element(materialGroup[0]).childs():
                        matName=material[2] + " " + materialGroup[2]
                        materialNames.append(matName)
                        matAbsorp=[]
                        for property in ui.element(material[0]).childs():
                            if property[1]==ui.element_type.ELEMENT_TYPE_MATERIAU_APP:
                                for frequency in ui.element(property[0]).childs():
                                    matAbsorp.append(ui.element(frequency[0]).getdecimalconfig("absorb"))
                        matAbsorp.insert(0,matName)
                        materials.append(matAbsorp)
                elif materialGroup[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_APP_MATERIAU:
                    matName=materialGroup[2]+" "+materialsGroups[2]
                    materialNames.append(matName)
                    matAbsorp=[]
                    for property in ui.element(materialGroup[0]).childs():
                        if property[1]==ui.element_type.ELEMENT_TYPE_MATERIAU_APP:
                            for frequency in ui.element(property[0]).childs():
                                matAbsorp.append(ui.element(frequency[0]).getdecimalconfig("absorb"))
                    matAbsorp.insert(0, matName)
                    materials.append(matAbsorp)
        elif materialsGroups[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_USER:
            for materialGroup in ui.element(materialsGroups[0]).childs():
                if materialGroup[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_USER_GROUP:
                    for material in ui.element(materialGroup[0]).childs():
                        matName=material[2]+" "+materialGroup[2]
                        materialNames.append(matName)
                        matAbsorp=[]
                        for property in ui.element(materialGroup[0]).childs():
                            if property[1]==ui.element_type.ELEMENT_TYPE_MATERIAU_USER:
                                for frequency in ui.element(property[0]).childs():
                                    matAbsorp.append(ui.element(frequency[0]).getdecimalconfig("absorb"))
                        matAbsorp.insert(0,matName)
                        materials.append(matAbsorp)
                elif materialGroup[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_USER_MATERIAU:
                    matName=materialGroup[2]+" "+materialsGroups[2]
                    materialNames.append(matName)
                    matAbsorp=[]
                    for property in ui.element(materialGroup[0]).childs():
                        if property[1]==ui.element_type.ELEMENT_TYPE_MATERIAU_USER:
                            for frequency in ui.element(property[0]).childs():
                                matAbsorp.append(ui.element(frequency[0]).getdecimalconfig("absorb"))
                    matAbsorp.insert(0, matName)
                    materials.append(matAbsorp)

def createSurfMatDict(matNames, surfaces):
    # dict structure {"surface name": [materialNames], "surface name": [materialNames], "surface name": [materialNames]}
    linkingDict={}
    for surface in surfaces:
        linkingDict[surface]=matNames
    return linkingDict

def getRecData(recName, punctualId):
    recData=[] # empty array
    for folder in ui.element(punctualId).childs(): # for each folder in "punctual receivers"
        if folder[2]=="Fused Receivers": # if folder named "Fused Receivers"
            for file in ui.element(folder[0]).childs(): # for each file in "Fused Receivers" folder
                if file[1]==ui.element_type.ELEMENT_TYPE_REPORT_GABE: # if type is gabe report
                    document=ui.e_file(file[0]) # create readabel element from id numbers
                    if document.getinfos()["name"]=="fusionSPL": # check name is "fusionSPL"
                        for row in ui.application.getdataarray(document): # for each row in file "fusionSPL"
                            if row[0]==recName: # if the column is the name of the chosen rec
                                recData=row[1:-2] # set recData equal to row with global and average vals removed
    return recData # return the now filled array

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
        punctualId=ui.element(elementId).getinfos()["parentid"] # id of the punctual rec folder
        solveId=ui.element(punctualId).getinfos()["parentid"] # id of solve folder
        sppsId=ui.element(solveId).getinfos()["parentid"] # id of spps folder
        uiTitle="Power Balance Calculator" # ui titie
        names=getNames(punctualId) # call function to get names of recievers
        # display ui where the user picks the excitation reciever and inputs the ID number of the scene ID
        userInput1=ui.application.getuserinput(uiTitle, "Pick the excitation Receiver", {"Excitation": names, "Scene ID": 0})
        if userInput1[0]: # if the ui "OK" Button is pressed
            matId, surfacesId = getIds(userInput1[1]["Scene ID"]) # call function to get the ID of material folder and surfaces folder
            excRecName=userInput1[1]["Excitation"] # set chosen excitation mic
            excitationSPL=getRecData(excRecName,punctualId) # get data array of excitation reciever
            qff,lf=GetBothCorrection(sppsId,solveId) # get the correction data
            areas,surfaceNames=getAreas(surfacesId) # areas format [[][][][]] names = []
            projArea=0 # have projected area be input by the user
            '''
            this function needs to be fixed to append the name of the material group
            '''
            materials=getMaterials(matId) # materials format [[[],[],[],[],[]],[[],[],[],[],[]]]
            # Next ui, link surface name to material name
            choiceDict=createSurfMatDict(materials[2]) # Create dict item to display vals in next ui
            # display second ui menu that gives each surface and the user attaces the chosen material to link to the surface
            userInput2=ui.application.getuserinput(uiTitle, "Select Material\nfor each surface.", choiceDict)
            if userInput2[0]: # if the ui "OK" button is pressed
                # Results to save
                overallTransmissionLoss, overallTLLF, projIntensity, totalPowerdB, totalPowerW=calcPowerBalance(excitationSPL,areas,projArea,materials,lf,qff)
                # use the save function from "core_functions.py"


ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_DONNEES,manager()) # show on "Data" in scene
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_PROJET,manager()) # show on "Project" in scene