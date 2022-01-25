# Author: Kyle Brooks
# Created: 25/01/2022

from libsimpa import *
import uictrl as ui

# works as intended
def getAvg(rts):
    avgSPL=[]
    numSrc=len(rts)
    count=0
    for rt in rts:
        for k,v in enumerate(rt):
            if count==0:
                avgSPL.append(float(v))
            else:
                avgSPL[k]+=float(v)
        count+=1
    for k,v in enumerate(avgSPL):
        avgSPL[k] /= numSrc
    return avgSPL
# works as intended
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
# un-tested
def calcSabineAbs(vol,rt):
    sabine=[]
    for val in rt:
        sabine.append((0.161*vol)/(val/1000))
    return sabine
#un-tested
def calcPercentageAbs(area,sabine):
    percentage=[]
    for val in sabine:
        percentage.append((val/area)*100)
    return percentage

class manager:
    def __init__(self):
        self.calcAbsid=ui.application.register_event(self.calcAbs) # register calcAbs function to i-simpa
    def getmenu(self,elementType,elementId,menu):
        el=ui.element(elementId)
        infos=el.getinfos()
        if infos["name"]=="Punctual receivers": # only display menu on Punctual receivers file
            menu.insert(0,())
            menu.insert(0,("Absorption Calculation (WIP)",self.calcAbsid))
            return True
        else:
            return False
        
    def calcAbs(self,elementId):
        uiTitle="Absorption Calculation (WIP)"
        userInput1=ui.application.getuserinput(uiTitle,"Input Data Below",{"Room Volume": "0","Room Bare Area":"0","Area of Sample":"0"})
        if userInput1[0]:
            areaData=userInput1[1]
            rt,freq,exists=getEDT(elementId)
            if not exists:
                print("Please Merge Point Receivers for EDT")
            if exists:
                avgSPL=getAvg(rt)
                userInput2=ui.application.getuserinput(uiTitle,"Input Data Below",{"Data Type":["Bare", "Sample"]})
                if userInput2[0]:
                    if userInput2[1]["Data Type"] == "Bare":
                        pass
                        # calculate the sabine and abs
                    if userInput2[1]["Data Type"] == "Sample":
                        freqRange={"a. 100 Hz":"0","b. 125 Hz":"0","c. 160 Hz":"0","d. 200 Hz": "0", "e. 250 Hz": "0", "f. 315 Hz":"0", "g. 400 Hz":"0","h. 500 Hz":"0","i. 630 Hz":"0","j. 800 Hz":"0","k. 1000 Hz":"0","l. 1250 Hz":"0","m. 1600 Hz":"0","n. 2000 Hz":"0","o. 2500 Hz":"0","p. 3150 Hz":"0","q. 4000 Hz":"0","r. 5000 Hz":"0","s. 6300 Hz":"0","t. 8000 Hz":"0","u. 10000 Hz":"0"}
                        userInput3=ui.application.getuserinput(uiTitle, "input bare data", freqRange)
                        # new window to input bare data to allow calculation of abs Coefficient
                # input bare values will need to be copy pasted

ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location