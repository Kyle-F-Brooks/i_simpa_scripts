# Author: Kyle Brooks
# Created: 14/02/22

from libsimpa import *
import uictrl as ui
import os

def GetSources(elementId):
    # read through the file 
    folders=ui.element(elementId)
    sources=[]
    freq=[]
    for folder in folders.childs():
        if folder[2]!="Fused Receivers" and folder[2]!="XYZ Plots" and folder[2]!="Source Contributions" and folder[2]!="Transmission Loss":
            files=ui.element(folder[0])
            for file in files.childs():
                if len(sources)>0:
                    freq=freq[:-1]
                    return sources,freq
                if file[1]==ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECPS:
                    document = ui.e_file(file[0])
                    if document.getinfos()["name"]=="Sound level per source":
                        dataFile=ui.application.getdataarray(document)
                        if len(freq)==0:
                            for dataRow in dataFile:
                                freq.append(dataRow[0])
                        for dataRow in dataFile[0][1:-1]:
                            sources.append(dataRow)
    
def GetData(elementId,selectedSrc):
    folders=ui.element(elementId)
    output=[]
    for folder in folders.childs():
        if folder[2]!="Fused Receivers" and folder[2]!="XYZ Plots" and folder[2]!="Source Contributions":
            files=ui.element(folder[0])
            for file in files.childs():
                receiverData=[]
                dataIndex=0
                if file[1]==ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECPS:
                    document = ui.e_file(file[0])
                    if document.getinfos()["name"]=="Sound level per source":
                        dataFile=ui.application.getdataarray(document)
                        dataIndex=dataFile[0].index(selectedSrc)
                        for dataRow in dataFile:
                            receiverData.append(dataRow[dataIndex])
                        receiverData[0]=folder[2]
                        output.append(receiverData[:-1])
    return output
def MakeDir(elementId):
        currentPath=ui.e_file(elementId)
        dirPath=currentPath.buildfullpath()+ r"\Source Contributions"
        if not os.path.exists(dirPath):
            os.mkdir(dirPath)
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
def RunSaves(elementId):
    currentPath=ui.e_file(elementId)
    srcList,freq=GetSources(elementId)
    for source in srcList:
        saveData=GetData(elementId, source)
        saveData.insert(0,freq)
        SaveFile(zip(*saveData),currentPath.buildfullpath()+ f"\Source Contributions\{source} Contributions.gabe")
        print(f"Created: {source} Contributions.gabe")

class manager:
    def __init__(self):
        self.getSrcContId=ui.application.register_event(self.getSrcCont) # register calcAbs function to i-simpa
    def getmenu(self,elementType,elementId,menu):
        el=ui.element(elementId)
        infos=el.getinfos()
        if infos["name"]=="Punctual receivers": # only display menu on Punctual receivers file
            menu.insert(0,("Get Source Contributions",self.getSrcContId))
            return True
        else:
            return False
    def getSrcCont(self, elementId):
        try:
            MakeDir(elementId)
            RunSaves(elementId)
            ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)
        except:
            print("An Error occured extracting the source contributions")
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location