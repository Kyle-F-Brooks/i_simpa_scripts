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