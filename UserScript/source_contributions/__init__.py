# Author: Kyle Brooks
# Created: 14/02/22

import libsimpa
import uictrl as ui

def getSources(folderwxid):
    # read through the file 
    folders=ui.element(folderwxid)
    sources=[]
    for folder in folders.childs():
        if folder[2]!="Fused Receivers" and folder[2]!="XYZ Plots":
            files=ui.element(folder[0])
            for file in files.childs():
                if len(sources)>0:
                    return sources
                if file[1]==ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECPS:
                    document = ui.e_file(file[0])
                    if document.getinfos()["name"]=="Sound level per source":
                        gridparam=ui.application.getdataarray(document)
                        for source in gridparam[0][1:-1]:
                            sources.append(source)
def getdata(folderwxid,selectedSrc):
    folders=ui.element(folderwxid)
    output=[]
    for folder in folders.childs():
        if folder[2]!="Fused Receivers" and folder[2]!="XYZ Plots":
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
class manager:
    def __init__(self):
        self.getSrcContId=ui.application.register_event(self.getSrcCont) # register calcAbs function to i-simpa
    def getmenu(self,elementType,elementId,menu):
        el=ui.element(elementId)
        infos=el.getinfos()
        if infos["name"]=="Punctual receivers": # only display menu on Punctual receivers file
            menu.insert(0,("Get Source Contributions (WIP)",self.getSrcContId))
            return True
        else:
            return False
    def getSrcCont(self, elementId):
        uiTitle="Source Contribution"
        srcList=getSources(elementId)
        pass

ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location