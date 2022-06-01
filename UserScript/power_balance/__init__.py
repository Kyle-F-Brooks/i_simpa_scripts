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

def getMaterials(matsId):
    materials=[]
    return materials

def getAreas(surfacesId):
    areas=[]
    return areas

class manager:
    def __init__(self):
        self.calcPowerBalanceId=ui.application.register_event(self.runCalculation)
    def getmenu(self,elementType,elementId,menu):
        el=ui.element(elementId)
        infos=el.getinfos()
        if infos["name"]=="Transmission Loss":
            menu.insert(2,("Create Power Balance",self.calcPowerBalanceId))
            return True
        else:
            return False
    def runCalculation(self,elementId):
        el=ui.element(elementId)
        infos=el.getinfos()
        punctualId=infos["parentid"]
        solveId=ui.element(punctualId).getinfos()["parentid"]
        sppsId=ui.element(solveId).getinfos()["parentid"]
        uiTitle="Power Balance Calculator"
        names=getNames(punctualId)
        userInput1=ui.application.getuserinput(uiTitle, "Pick the excitation Receiver", {"Excitation": names})
        if userInput1[0]:
            excRecName=userInput1[1]["Excitation"]
            excitationSPL=[]
            qff,lf=GetBothCorrection(sppsId,solveId)
            areas=getAreas() # areas format [[][][][]]
            projArea=0 # have projected area be input by the user
            materials=getMaterials() # materials format [[][][][][][]]
            overallTransmissionLoss, overallTLLF, projIntensity, totalPowerdB, totalPowerW=calcPowerBalance(excitationSPL,areas,projArea,materials,lf,qff)


ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location