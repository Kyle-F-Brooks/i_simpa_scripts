#core_functions.py>
from libsimpa import *
import os
import uictrl as ui

def SaveFile(saveData, path):
    data=list(saveData)
    gabewriter=Gabe_rw(len(data))
    labelcol=stringarray()
    for cell in data[0][1:]:
        labelcol.append(cell.encode('cp1252'))
    gabewriter.AppendStrCol(labelcol,'')
    for col in data[1:]:
        datacol=floatarray()
        for cell in col[1:]:
            datacol.append(float(cell))
        gabewriter.AppendFloatCol(datacol,str(col[0]))
    gabewriter.Save(path.encode('cp1252'))

def MakeDir(elementId, targetDir):
    currentPath=ui.e_file(elementId)
    targetPath = currentPath.buildfullpath()+ targetDir
    if not os.path.exists(targetPath):
        os.mkdir(targetPath)

def GetLFCorrection(sppsElementId):
    lf=[]
    sppsFolder=ui.element(sppsElementId)
    for files in sppsFolder.childs():
        if files[1]==ui.element_type.ELEMENT_TYPE_REPORT_GABE:
            lfDocument=ui.e_file(files[0])
            if lfDocument.getinfos()["name"]=="LF_Correction":
                gridparam=ui.application.getdataarray(lfDocument)
                for row in gridparam:
                    if row[0]=='':
                        pass
                    else:
                        lf.append(row[1])
    return lf

def GetQFFCorrection(solveElementId):
    qff=[]
    solveFolder=ui.element(solveElementId)
    for files in solveFolder.childs():
        if files[1]==ui.element_type.ELEMENT_TYPE_REPORT_GABE:
            qffDocument=ui.e_file(files[0])
            if qffDocument.getinfos()["name"]=="QFF_Correction":
                gridparam=ui.application.getdataarray(qffDocument)
                for row in gridparam:
                    if row[0]=='':
                        pass
                    else:
                        qff.append(row[1])
    return qff
    
def GetBothCorrection(sppsElementId,solveElementId):
    qff=[]
    lf=[]
    sppsFolder=ui.element(sppsElementId)
    for files in sppsFolder.childs():
        if files[1]==ui.element_type.ELEMENT_TYPE_REPORT_GABE:
            lfDocument=ui.e_file(files[0])
            if lfDocument.getinfos()["name"]=="LF_Correction":
                gridparam=ui.application.getdataarray(lfDocument)
                for row in gridparam:
                    if row[0]=='':
                        pass
                    else:
                        lf.append(row[1])
    solveFolder=ui.element(solveElementId)
    for files in solveFolder.childs():
        if files[1]==ui.element_type.ELEMENT_TYPE_REPORT_GABE:
            qffDocument=ui.e_file(files[0])
            if qffDocument.getinfos()["name"]=="QFF_Correction":
                gridparam=ui.application.getdataarray(qffDocument)
                for row in gridparam:
                    if row[0]=='':
                        pass
                    else:
                        qff.append(row[1])
    return qff,lf