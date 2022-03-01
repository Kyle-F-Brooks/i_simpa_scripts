# Author: Kyle Brooks
# Created: 28/01/2022

from libsimpa import *
import uictrl as ui
import os
import math

def getRecNames(receiverData):
    names=[]
    for rec in receiverData:
        names.append(rec[0])
    return names
def GetSourceNames(elementId):
    # read through the file 
    files=ui.element(elementId)
    sources=[]
    for file in files.childs():
        if file[1]==ui.element_type.ELEMENT_TYPE_REPORT_GABE:
            sources.append(file[2][:-14])
    return sources
def readFusionGabe(elementId):
    folders=ui.element(elementId)
    receivers=[]
    exists=False
    freq=None
    for folder in folders.childs():
        if folder[2]=="Fused Receivers":
            files=ui.element(folder[0])
            for file in files.childs():
                if file[1]==ui.element_type.ELEMENT_TYPE_REPORT_GABE:
                    document = ui.e_file(file[0])
                    if document.getinfos()["name"]=="fusionSPL":
                        exists=True
                        gridparam=ui.application.getdataarray(document)
                        for row in gridparam:
                            row=row[:-2]
                            if row[0]=='':
                                row[0]='Frequency'
                                freq=row
                            else:
                                receivers.append(row)
    return receivers, freq, exists
def readContributionGabe(elementId):
    files=ui.element(elementId)
    sources=[]
    freq=None
    for file in files.childs():
        if file[1] == ui.element_type.ELEMENT_TYPE_REPORT_GABE:
            document=ui.e_file(file[0])
            receivers=[]
            dataFile=ui.application.getdataarray(document)
            for dataRow in dataFile:
                if dataRow[0]=='':
                    dataRow[0]='Frequency'
                    freq=dataRow
                else:
                    receivers.append(dataRow)
            sources.append(receivers)
    return sources, freq
                
def createMatrix(xVals,yVals,recIds,first,last):
    # recIds is an array of all the receiver IDs
    recCounter=0
    recMatrix=[]
    startLogging=False
    for x in range(xVals):
        recVals=[]
        for y in range(yVals):
            if recIds[recCounter]==first:
                startLogging=True
            if startLogging:
                recVals.append(recIds[recCounter])
            if recIds[recCounter]==last:
                startLogging=False
            recCounter+=1
        recMatrix.append(recVals)
    return recMatrix

def removeNaN(receiver):
    lowestVal=500
    recId=receiver[0]
    receiver=receiver[1:]
    for val in receiver:
        if val<lowestVal:
            lowestVal=val
    for k,v in enumerate(receiver):
        if math.isnan(v):
            receiver[k]=lowestVal
    receiver.insert(0,recId)
    return receiver

def createXYZ(recMatrix,receivers,freq,selectedFreq):
    xyz=[['','X','Y','Z']]
    x=1
    freqIndex=freq.index(selectedFreq)
    for k1,yList in enumerate(recMatrix):
        y=1
        for k2,receiverId in enumerate(yList):
            for receiverNaN in receivers:
                receiver=removeNaN(receiverNaN)
                if receiver[0]==receiverId:
                    z= receiver[freqIndex]
            xyz.append([receiverId,x,y,z])
            y+=1
        x+=1
    return xyz

def SaveFile(saveData,path):
    data=list(saveData)
    # Gabe_rw(), stringarray(), floatarray() called from libsimpa
    gabewriter=Gabe_rw(len(data)) # create writer with length equal to data array length
    labelcol=stringarray()  # label col is assigned as an array of strings
    for cell in data[0][1:]:
        labelcol.append(cell.encode('cp1252'))
    gabewriter.AppendStrCol(labelcol,'')
    for col in data[1:]:
        datacol=floatarray()
        for cell in col[1:]:
            datacol.append(float(cell))
        gabewriter.AppendFloatCol(datacol,str(col[0]))
    gabewriter.Save(path.encode('cp1252'))
def MakeDir(elementId):
    grp=ui.e_file(elementId)
    targetPath=grp.buildfullpath()+ r"\XYZ Plots"
    if not os.path.exists(targetPath):
        os.mkdir(targetPath)

class manager:
    def __init__(self):
        self.receiverMatrixId=ui.application.register_event(self.receiverMatrix)
        self.contributionMatrixId=ui.application.register_event(self.contributionMatrix)
    def getmenu(self,elementType,elementId,menu):
        el=ui.element(elementId)
        infos=el.getinfos()
        if infos["name"]==u"Punctual receivers": # only display menu on Punctual receivers file
            menu.insert(0,(u"Plot as XYZ",self.receiverMatrixId))
            return True
        if infos["name"]=="Source Contributions":
            menu.insert(0,())
            menu.insert(0,(u"Plot as XYZ",self.contributionMatrixId))
        else:
            return False
    def contributionMatrix(self,elementId):
        folder=ui.e_file(elementId)
        uiTitle="Plot XYZ"
        sourceNames=GetSourceNames(elementId)
        sources,freq=readContributionGabe(elementId)
        recIds=getRecNames(sources[0])
        userInput1=ui.application.getuserinput(uiTitle,"Please input the matrix dimensions", {"First Receiver":recIds,"Last Receiver":recIds,"X Dimension":"0","Y Dimension":"0","Frequency":freq[1:]})
        if userInput1[0]:
            MakeDir(elementId)
            counter=0
            for source in sources:
                recMatrix=createMatrix(int(userInput1[1]["X Dimension"]),int(userInput1[1]["Y Dimension"]),recIds,userInput1[1]["First Receiver"],userInput1[1]["Last Receiver"])
                xyz=createXYZ(recMatrix,source,freq,userInput1[1]["Frequency"])
                targetFreq=userInput1[1]["Frequency"]
                SaveFile(zip(*xyz),folder.buildfullpath()+f"XYZ Plots\{sourceNames[counter]}_{targetFreq}_XYZ.gabe")
                counter+=1
            ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)
    def receiverMatrix(self,elementId):
        folder=ui.e_file(elementId)
        receivers,freq,exists=readFusionGabe(elementId)
        if not exists:
            print("Please Merge Recevier SPL")
        elif exists:
            uiTitle="Plot XYZ"
            recIds=getRecNames(receivers)
            userInput1=ui.application.getuserinput(uiTitle,"Please input the matrix dimensions", {"First Receiver":recIds,"Last Receiver":recIds,"X Dimension":"0","Y Dimension":"0","Frequency":freq[1:]})
            if userInput1[0]:
                recMatrix=createMatrix(int(userInput1[1]["X Dimension"]),int(userInput1[1]["Y Dimension"]),recIds,userInput1[1]["First Receiver"],userInput1[1]["Last Receiver"])
                xyz=createXYZ(recMatrix,receivers,freq,userInput1[1]["Frequency"])
                MakeDir(elementId)
                targetFreq=userInput1[1]["Frequency"]
                SaveFile(zip(*xyz),folder.buildfullpath()+f"XYZ Plots\{targetFreq}_XYZ.gabe")
                ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)

ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location