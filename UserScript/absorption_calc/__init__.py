# Author: Kyle Brooks
# Created: 25/01/2022

from libsimpa import *
import uictrl as ui

def getAvg(rts):
    avgSPL=[]
    numSrc=len(rts)
    count=0
    for rt in rts:
        for k,v in enumerate(rt):
            if count==0:
                avgSPL.append(float(v)*1000)
            else:
                avgSPL[k]+=(float(v)*1000)
        count+=1
    for k,v in enumerate(avgSPL):
        avgSPL[k] /= numSrc
    return avgSPL

def getEDT(folderwxid):
    folders=ui.element(folderwxid)
    receivers=[]
    exists=False
    freq=None
    for folder in folders.childs():
        if folder[2]=="Fused Receivers":
            files=ui.element(folder[0])
            for file in files.childs():
                if file[1]==ui.element_type.ELEMENT_TYPE_REPORT_GABE:
                    document = ui.e_file(file[0])
                    if document.getinfos()["name"]=="fusionEDT":
                        exists=True
                        gridparam=ui.application.getdataarray(document)
                        for row in gridparam:
                            row=row[:-2]
                            if row[0]=='':
                                freq=row[1:]
                            else:
                                receivers.append(row[1:])
    return receivers, freq, exists
    
def calcSabineAbs(vol,rt):
    sabine=[]
    for val in rt:
        sabine.append((0.161*vol)/(val/1000))
    return sabine
def calcPercentageAbs(area,sabine):
    percentage=[]
    for val in sabine:
        percentage.append((val/area)*100)
    return percentage
def calcAbsCoeff(bareSabine,sampleSabine,sampleArea):
    absCoeff=[]
    for k,v in enumerate(sampleSabine):
        absCoeff.append(((v-float(bareSabine[k]))/sampleArea)*100)
    return absCoeff
def calcSabineFinal(sampleSabine,bareSabine):
    sabineAbs=[]
    for k,v in enumerate(sampleSabine):
        sabineAbs.append(v-float(bareSabine[k]))
    return sabineAbs

# remember to zip(*saveData)
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

class manager:
    def __init__(self):
        self.calcAbsid=ui.application.register_event(self.calcAbs) # register calcAbs function to i-simpa
    def getmenu(self,elementType,elementId,menu):
        el=ui.element(elementId)
        infos=el.getinfos()
        if infos["name"]=="Punctual receivers": # only display menu on Punctual receivers file
            menu.insert(0,())
            menu.insert(0,("Absorption Calculation",self.calcAbsid))
            return True
        else:
            return False
    def calcAbs(self,elementId):
        uiTitle="Absorption Calculation"
        userInput1=ui.application.getuserinput(uiTitle,"Input Data Below",{"Cabin Volume": "0","Cabin Area":"0","Sample Area":"0"})
        grp=ui.e_file(elementId)
        if userInput1[0]:
            areaData=userInput1[1]
            rt,freq,exists=getEDT(elementId)
            freq.insert(0,'')
            if not exists:
                print("Please Merge Point Receivers for EDT")
            if exists:
                avgSPL=getAvg(rt)
                userInput2=ui.application.getuserinput(uiTitle,"Input Data Below",{"Data Type":["Bare", "Sample"]})
                if userInput2[0]:
                    if userInput2[1]["Data Type"] == "Bare":
                        try:
                            sampleData=calcSabineAbs(float(areaData["Cabin Volume"]),avgSPL)
                            absPercent=calcPercentageAbs(float(areaData["Cabin Area"]),sampleData)
                            sampleData.insert(0,"Sabine")
                            absPercent.insert(0,"Absorption %")
                            saveData=[freq,sampleData,absPercent]
                            SaveFile(zip(*saveData),grp.buildfullpath()+r"Bare Cabin Absorption.gabe")
                        except:
                            print("Error while calculating bare absorption")
                    elif userInput2[1]["Data Type"] == "Sample":
                        try:
                            freqRange={"a. 100 Hz":"0","b. 125 Hz":"0","c. 160 Hz":"0","d. 200 Hz": "0", "e. 250 Hz": "0", "f. 315 Hz":"0", "g. 400 Hz":"0","h. 500 Hz":"0","i. 630 Hz":"0","j. 800 Hz":"0","k. 1000 Hz":"0","l. 1250 Hz":"0","m. 1600 Hz":"0","n. 2000 Hz":"0","o. 2500 Hz":"0","p. 3150 Hz":"0","q. 4000 Hz":"0","r. 5000 Hz":"0","s. 6300 Hz":"0","t. 8000 Hz":"0","u. 10000 Hz":"0"}
                            userInput3=ui.application.getuserinput(uiTitle, "Input Bare Sabine Data", freqRange)
                            if userInput3[0]:
                                bareData=list(userInput3[1].values())
                                sampleData=calcSabineAbs(float(areaData["Cabin Volume"]),avgSPL)
                                absCoeff=calcAbsCoeff(bareData,sampleData,float(areaData["Sample Area"]))
                                sabineAbs=calcSabineFinal(sampleData,bareData)
                                absCoeff.insert(0,"Absorption Coefficient")
                                sabineAbs.insert(0,"Sabine")
                                saveData=[freq,absCoeff,sabineAbs]
                                SaveFile(zip(*saveData),grp.buildfullpath()+r"Cabin Sample Absorption.gabe")
                        except:
                            print("An error occured while calculating sample absorption")
                    ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)
                        # new window to input bare data to allow calculation of abs Coefficient
                # input bare values will need to be copy pasted

ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location