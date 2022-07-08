# Author: Kyle Brooks
# Created: 24/05/2022
# Description: Script to calculate the power balance

import uictrl as ui
from libsimpa import *
from core_functions import *
import math

print("\nIn order to run the power balance calculation,\neach surface needs to be right clicked and copied.\n\nRight click on 'Data' or 'Project' to get the scene ID")

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

def calcPowerBalance(excitationSPL, areas, projArea, materials, lf, qff):
    # materials is an array of array of material stl has to be same length as areas
    H=0.000000000001 # 1e -12
    # calculate excitation intensity in watts
    excitationIntensityW=[]
    excitationSTL=[]
    for freq in excitationSPL:
        intesnsityDb=float(freq)-6# correct math
        excitationSTL.append(intesnsityDb)
        excitationIntensityW.append((math.pow(10, (intesnsityDb/10))*H)) # correct math
    # calculate adjacent powers
    adjacentPowersW=[]
    adjacentPowersdB=[]
    totalArea=0
    for surface, area in areas.items():
        adjacentPowerW=[]
        adjacentPowerdB=[]
        for intens in excitationIntensityW:
            excInt=intens*float(area)
            adjacentPowerW.append(excInt)
            adjacentPowerdB.append((10*math.log10((excInt/H))))
        adjacentPowersW.append(adjacentPowerW)
        adjacentPowersdB.append(adjacentPowerdB)
        totalArea+=float(area)
    # Calculate total power in
    totalPowerIn=[]
    for freq in excitationIntensityW:
        totalPowerIn.append(freq*totalArea)
    # add the qff to the materials
    materialsQff=[]
    for surface, material in materials.items():
        materialQff=[]
        for k,v in enumerate(material):
            materialQff.append(v+qff[k])
        materialsQff.append(materialQff)
    # calc radiated power
    radiatedPowersdB=[]
    radiatedPowersW=[]
    for k1,v1 in enumerate(adjacentPowersdB):
        radiatedPowerdB=[]
        radiatedPowerW=[]
        for k2,v2 in enumerate(v1):
            rPdB=v2-materialsQff[k1][k2]
            rPw=(math.pow(10,(rPdB/10))*H)
            radiatedPowerdB.append(rPdB)
            radiatedPowerW.append(rPw)
        radiatedPowersdB.append(radiatedPowerdB)
        radiatedPowersW.append(radiatedPowerW)
    # calc total power out
    totalPowerW=[]
    totalPowerdB=[]
    for k1,v1 in enumerate(radiatedPowersW):
        if k1 == 0:
            totalPowerW=v1
        else:
            for k2, v2 in enumerate(v1):
                totalPowerW[k2]+=v2
    for watt in totalPowerW:
        totalPowerdB.append(10*math.log10(watt/H))
    # calc projected Intensity
    projIntensity=[]
    for watt in totalPowerW:
        projIntensity.append(10*math.log10((watt/projArea)/H))
    # calc overall Transmission loss
    overallTransmissionLoss=[]
    for k,v in enumerate(projIntensity):
        overallTransmissionLoss.append(excitationSTL[k]-v)
    overallTLLF=[]
    for k,v in enumerate(overallTransmissionLoss):
        overallTLLF.append(lf[k]+v)
    return overallTransmissionLoss, overallTLLF, projIntensity, totalPowerdB, totalPowerW, totalPowerIn

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
    areas={} # empty array to store surface areas
    surfaceNames=[] # empty array to store surface names
    for surface in ui.element(surfacesId).childs(): # for each surface
        if surface[1] == ui.element_type.ELEMENT_TYPE_SCENE_GROUPESURFACES_GROUPE: # if is group of surfaces
            area=ui.element(surface[0]).getdecimalconfig("aire") # declare area
            areas[surface[2]]=area # store area
            surfaceNames.append(surface[2]) # store surface name
    return areas, surfaceNames

# problem in this section
def getMaterials(matsId):
    materials=[] # empty array to store all material data
    materialNames=[] # empty array for all material names
    for materialsGroups in ui.element(matsId).childs(): # for each group in materials folder
        if materialsGroups[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_APP: # if group is generated by application
            for materialGroup in ui.element(materialsGroups[0]).childs(): # for element in group 
                if materialGroup[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_APP_GROUP: # if element is a group 
                    for material in ui.element(materialGroup[0]).childs(): # for each material in group 
                        if material[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_APP_GROUP:
                            for mat in ui.element(material[0]).childs():
                                if mat[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_APP_MATERIAU:
                                    matName=mat[2] + " " + material[2] # create mat name with group name appended to remove multiples of same mat
                                    materialNames.append(matName) # append name to list
                                    matAbsorp=[] # create empty array for absorption data
                                    for property in ui.element(mat[0]).childs(): # for each property of material
                                        if property[1]==ui.element_type.ELEMENT_TYPE_MATERIAU_APP: # if property is material spectrum
                                            for frequency in ui.element(property[0]).childs(): # for each frequency of material
                                                matAbsorp.append(round(ui.element(frequency[0]).getdecimalconfig("affaiblissement"),4)) # append the absorption value to array
                                    matAbsorp.insert(0,matName) # insert name of material to beginning of array for later sorting
                                    materials.append(matAbsorp) # append the material data to the materials array
                        elif material[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_APP_MATERIAU:
                            # same as above
                            matName=materialGroup[2]+" "+materialsGroups[2]
                            materialNames.append(matName)
                            matAbsorp=[]
                            for property in ui.element(materialGroup[0]).childs():
                                if property[1]==ui.element_type.ELEMENT_TYPE_MATERIAU_APP:
                                    for frequency in ui.element(property[0]).childs():
                                        matAbsorp.append(round(ui.element(frequency[0]).getdecimalconfig("affaiblissement"),4))
                            matAbsorp.insert(0, matName)
                            materials.append(matAbsorp)
                elif materialGroup[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_APP_MATERIAU: # if element is a material
                    # same as above
                    matName=materialGroup[2]+" "+materialsGroups[2]
                    materialNames.append(matName)
                    matAbsorp=[]
                    for property in ui.element(materialGroup[0]).childs():
                        if property[1]==ui.element_type.ELEMENT_TYPE_MATERIAU_APP:
                            for frequency in ui.element(property[0]).childs():
                                matAbsorp.append(round(ui.element(frequency[0]).getdecimalconfig("affaiblissement"),4))
                    matAbsorp.insert(0, matName)
                    materials.append(matAbsorp)
        elif materialsGroups[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_USER: # if group is generated by the user
            for materialGroup in ui.element(materialsGroups[0]).childs(): # for element in group
                if materialGroup[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_USER_GROUP: # if element is group
                    for material in ui.element(materialGroup[0]).childs(): # for each material in group
                        matName=material[2]+" "+materialGroup[2] # create mat name with group name appended to remove multiples of same mat
                        materialNames.append(matName) # append name to list 
                        matAbsorp=[] # create empty array for aborption data
                        for property in ui.element(material[0]).childs(): # for each property of material
                            if property[1]==ui.element_type.ELEMENT_TYPE_MATERIAU_USER: # if property is material spectrum
                                for frequency in ui.element(property[0]).childs(): # for each frequency of material
                                    matAbsorp.append(round(ui.element(frequency[0]).getdecimalconfig("affaiblissement"),4)) # append the absorption value to array
                        matAbsorp.insert(0,matName) # insert name of material o beginningg of array for later sorting
                        materials.append(matAbsorp) # append the material data to the materials array
                elif materialGroup[1]==ui.element_type.ELEMENT_TYPE_SCENE_BDD_MATERIAUX_USER_MATERIAU: # if element is a material
                    # same as above
                    matName=materialGroup[2]+" "+materialsGroups[2]
                    materialNames.append(matName)
                    matAbsorp=[]
                    for property in ui.element(material[0]).childs():
                        if property[1]==ui.element_type.ELEMENT_TYPE_MATERIAU_USER:
                            for frequency in ui.element(property[0]).childs():
                                matAbsorp.append(round(ui.element(frequency[0]).getdecimalconfig("affaiblissement"),4))
                    matAbsorp.insert(0, matName)
                    materials.append(matAbsorp)
    return materials, materialNames

def createSurfMatDict(matNames, surfaces):
    # dict structure {"surface name": [materialNames], "surface name": [materialNames], "surface name": [materialNames]}
    linkingDict={}
    for surface in surfaces:
        linkingDict[surface]=matNames
    return linkingDict

def selectMaterials(materials, choices):
    # take the materials list and choices list, look at the choices and return dict with Key: Surface Name, Value: Material spectrum
    dataDict={}
    for key in choices:
        # choice is the key
        chosenMat=choices[key]
        for material in materials:
            if material[0]==chosenMat:
                dataDict[key]=material[4:-3] # trim material name and set freq to 100Hz-10000Hz
        # Key: Surface Name
        # Value: Material Name
    return dataDict

def createSurfaceChoice(surfaceNames):
    dataDict={}
    for surfaceName in surfaceNames:
        dataDict[surfaceName]=["Yes", "No"]
    return dataDict

def selectSurfaces(surfaceDict, areas):
    selectedSurfaces=[]
    selectedAreas={}
    for surface, answer in surfaceDict.items():
        if answer=="Yes":
            selectedSurfaces.append(surface)
    for surface, area in areas.items():
        if surface in selectedSurfaces:
            selectedAreas[surface]=area
    return selectedSurfaces, selectedAreas

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
        userInput0=ui.application.getuserinput(uiTitle, "Pick the excitation Receiver", {"Excitation": names,"Scene ID":"0", "Projected Area":"0"})
        if userInput0[0]: # if the ui "OK" Button is pressed
            matId, surfacesId = getIds(int(userInput0[1]["Scene ID"])) # call function to get the ID of material folder and surfaces folder
            excRecName=userInput0[1]["Excitation"] # set chosen excitation mic
            excitationSPL=getRecData(excRecName,punctualId) # get data array of excitation reciever
            qff,lf=GetBothCorrection(sppsId,solveId) # get the correction data
            allAreas,surfaceNames=getAreas(surfacesId) # areas format [[][][][]] names = []
            projArea=float(userInput0[1]["Projected Area"]) # have projected area be input by the user
            surfaceChoice=createSurfaceChoice(surfaceNames)
            userInput1=ui.application.getuserinput(uiTitle,"Pick surfaces for model", surfaceChoice)
            if userInput1[0]:
                materials,materialsNames=getMaterials(matId) # materials format [[],[],[],[],[]]
                selectedSurfaces, selectedArea=selectSurfaces(userInput1[1], allAreas)
                choiceDict=createSurfMatDict(materialsNames,selectedSurfaces) # Create dict item to display vals in next ui
                # display second ui menu that gives each surface and the user attaces the chosen material to link to the surface
                userInput2=ui.application.getuserinput(uiTitle, "Select Material\nfor each surface.", choiceDict)
                if userInput2[0]: # if the ui "OK" button is pressed
                    # Results to save
                    chosenMaterials=selectMaterials(materials,userInput2[1])
                    overallTransmissionLoss, overallTLLF, projIntensity, totalPowerdB, totalPowerW=calcPowerBalance(excitationSPL,selectedArea,projArea,chosenMaterials,lf,qff)
                    # use the save function from "core_functions.py"


ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_DONNEES,manager()) # show on "Data" in scene
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_SCENE_PROJET,manager()) # show on "Project" in scene