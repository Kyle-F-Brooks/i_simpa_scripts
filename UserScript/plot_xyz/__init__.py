# Author: Kyle Brooks
# Created: 28/01/2022

from libsimpa import *
import uictrl as ui
import os
import math

# read through array of arrays structured in a frequency against receiver table
def getRecNames(receiverData):
    names=[]
    for rec in receiverData:
        names.append(rec[0])
    return names
# reads source contribution file names to get the specific source names
def GetSourceNames(elementId):
    files=ui.element(elementId)
    sources=[]
    for file in files.childs():
        if file[1]==ui.element_type.ELEMENT_TYPE_REPORT_GABE:
            sources.append(file[2][:-14])
    return sources

# read fusionSPL gabe file in
def readFusionGabe(elementId):
    # initialise variables
    folders=ui.element(elementId)
    receivers=[]
    exists=False
    freq=None
    # find the fusionSPL file in the Fused Receivers folder
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
# read the source contribution files in
def readContributionGabe(elementId):
    # initialise variables
    files=ui.element(elementId)
    sources=[]
    freq=None
    for file in files.childs():
        # check element type
        if file[1] == ui.element_type.ELEMENT_TYPE_REPORT_GABE:
            # open the report and read the data from it
            document=ui.e_file(file[0])
            dataFile=ui.application.getdataarray(document)
            # sort the data into frequency, extract each receiver line into list
            receivers=dataFile[1:]
            freq=dataFile[0]
            freq[0]='Frequency'
            # store each receivers in sources creating [[[Recevier 1],[Receiver 2]],[[Receiver 1],[Receiver 2]]]
            sources.append(receivers)
    return sources, freq
# read STL gabe file in
def readTransmissionGabe(elementId):
    # given element ID of Transmission Loss folder
    files=ui.element(elementId)
    freq=None
    receivers=[]
    for file in files.childs():
        # search for file name STL Data 
        if file[2]=='STL Data':
            document=ui.e_file(file[0])
            dataFile=ui.application.getdataarray(document)
            # split the frequency row from the receivers
            freq=dataFile[0]
            freq[0]='Frequency'
            receivers=dataFile[1:]
    return receivers, freq
# create a matrix describing the location of the receviers in the grid            
def createMatrix(xVals,yVals,recIds,first,last):
    # get list of receivers in the array
    firstIndex=recIds.index(first)
    lastIndex=recIds.index(last)
    receiverList=recIds[firstIndex:(lastIndex+1)]
    recMatrix=[]
    recCounter=0
    # create the matrix based on the user input x y values
    for x in range(xVals):
        recVals=[]
        for y in range(yVals):
            recVals.append(receiverList[recCounter])
            recCounter+=1
        recMatrix.append(recVals)
    return recMatrix
# search through the input data and if any values are NaN, make them equal to the lowest value in the array
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
# take the input matrix and the data to create the xyz plot
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
        self.transmissionMatrixId=ui.application.register_event(self.transmissionMatrix)
    def getmenu(self,elementType,elementId,menu):
        el=ui.element(elementId)
        infos=el.getinfos()
        if infos["name"]==u"Punctual receivers": # only display menu on Punctual receivers file
            menu.insert(0,(u"Plot as XYZ",self.receiverMatrixId))
            return True
        if infos["name"]=="Source Contributions":
            menu.insert(0,())
            menu.insert(0,(u"Plot as XYZ",self.contributionMatrixId))
            return True
        if infos["name"]=="Transmission Loss":
            menu.insert(0,())
            menu.insert(0,(u"Plot as XYZ",self.transmissionMatrixId))
            return True
        else:
            return False
    def transmissionMatrix(self, elementId):
        folder=ui.e_file(elementId)
        uiTitle="Plot XYZ"
        receivers,freq=readTransmissionGabe(elementId)
        freq.insert(1, "All Freq")
        recIds=getRecNames(receivers)
        userInput1=ui.application.getuserinput(uiTitle,"Please input the matrix dimensions", {"First Receiver":recIds,"Last Receiver":recIds,"X Dimension":"0","Y Dimension":"0","Frequency":freq[1:]})
        if userInput1[0]:
            try:
                freq.pop(1)
                MakeDir(elementId)
                recMatrix=createMatrix(int(userInput1[1]["X Dimension"]),int(userInput1[1]["Y Dimension"]),recIds,userInput1[1]["First Receiver"],userInput1[1]["Last Receiver"])
                if userInput1[1]["Frequency"] == "All Freq":
                    for f in freq[1:]:
                        xyz=createXYZ(recMatrix,receivers,freq,f)
                        SaveFile(zip(*xyz),folder.buildfullpath()+f"XYZ Plots\{f}_STL_XYZ.gabe")
                else:
                    xyz=createXYZ(recMatrix,receivers,freq,userInput1[1]["Frequency"])
                    targetFreq=userInput1[1]["Frequency"]
                    SaveFile(zip(*xyz),folder.buildfullpath()+f"XYZ Plots\{targetFreq}_STL_XYZ.gabe")
                ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)
                ui.application.saveproject()
            except:
                print("An Error Occured while building the plot for transmission loss")
            
    def contributionMatrix(self,elementId):
        folder=ui.e_file(elementId)
        uiTitle="Plot XYZ"
        sourceNames=GetSourceNames(elementId)
        sources,freq=readContributionGabe(elementId)
        freq.insert(1, "All Freq")
        recIds=getRecNames(sources[0])
        userInput1=ui.application.getuserinput(uiTitle,"Please input the matrix dimensions", {"First Receiver":recIds,"Last Receiver":recIds,"X Dimension":"0","Y Dimension":"0","Frequency":freq[1:]})
        if userInput1[0]:
            try:
                freq.pop(1)
                MakeDir(elementId)
                counter=0
                recMatrix=createMatrix(int(userInput1[1]["X Dimension"]),int(userInput1[1]["Y Dimension"]),recIds,userInput1[1]["First Receiver"],userInput1[1]["Last Receiver"])
                for source in sources:
                    if userInput1[1]["Frequency"] == "All Freq":
                        for f in freq[1:]:
                            xyz=createXYZ(recMatrix,source,freq,f)
                            SaveFile(zip(*xyz),folder.buildfullpath()+f"XYZ Plots\{sourceNames[counter]}_{f}_XYZ.gabe")
                    else:
                        xyz=createXYZ(recMatrix,source,freq,userInput1[1]["Frequency"])
                        targetFreq=userInput1[1]["Frequency"]
                        SaveFile(zip(*xyz),folder.buildfullpath()+f"XYZ Plots\{sourceNames[counter]}_{targetFreq}_XYZ.gabe")
                    counter+=1
                ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)
                ui.application.saveproject()
            except:
                print("An Error Occured while building the plot for the source contributions")

    def receiverMatrix(self,elementId):
        folder=ui.e_file(elementId)
        receivers,freq,exists=readFusionGabe(elementId)
        freq.insert(1, "All Freq")
        if not exists:
            print("Please Merge Recevier SPL")
        elif exists:
            uiTitle="Plot XYZ"
            recIds=getRecNames(receivers)
            userInput1=ui.application.getuserinput(uiTitle,"Please input the matrix dimensions", {"First Receiver":recIds,"Last Receiver":recIds,"X Dimension":"0","Y Dimension":"0","Frequency":freq[1:]})
            if userInput1[0]:
                try:
                    freq.pop(1)
                    MakeDir(elementId)
                    recMatrix=createMatrix(int(userInput1[1]["X Dimension"]),int(userInput1[1]["Y Dimension"]),recIds,userInput1[1]["First Receiver"],userInput1[1]["Last Receiver"])
                    if userInput1[1]["Frequency"] == "All Freq":
                        for f in freq[1:]:
                            xyz=createXYZ(recMatrix,receivers,freq,f)
                            SaveFile(zip(*xyz),folder.buildfullpath()+f"XYZ Plots\{f}_XYZ.gabe")
                    else:
                        xyz=createXYZ(recMatrix,receivers,freq,userInput1[1]["Frequency"])
                        targetFreq=userInput1[1]["Frequency"]
                        SaveFile(zip(*xyz),folder.buildfullpath()+f"XYZ Plots\{targetFreq}_XYZ.gabe")
                    ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)
                    ui.application.saveproject()
                except:
                    print("An Error Occured whilst building the plot for SPL")

ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location