# Author: Kyle Brooks
# Created: 18/01/22

import uictrl as ui
from libsimpa import *

# this function works
def getNames(folderwxid):
    # if using the fusion files, it may not be needed to get the receiver element dicts.
    receivers=[] # array of receiver element dicts
    names=[] # array of receiver names
    folder=ui.element(folderwxid) # set folder
    recplist=folder.getallelementbytype(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER) # get all folders in folder
    for idrecp in recplist: # for each folder get info
        recp=ui.element(idrecp)
        infos=recp.getinfos()
        if not infos["label"]=="Fused Receivers": # if receiver folder append to array receivers 
            receivers.append(infos)
    for receiver in receivers: # for each stored receiver append "label property to array names"
        names.append(receiver["label"])
    return names

# This function works
def getVals(folderwxid, recid):
    receivers=[]
    srcrec=None
    folders=ui.element(folderwxid)
    exists=False
    for folder in folders.childs():
        if folder[2]=="Fused Receivers": # speciically find the Fused Receivers folder
            files=ui.element(folder[0])
            for file in files.childs():
                if file[1]==ui.element_type.ELEMENT_TYPE_REPORT_GABE:
                    document = ui.e_file(file[0])
                    if document.getinfos()["name"]=="fusionSPL": # within the Fused Rec folder find the SPL list
                        exists=True
                        gridparam=ui.application.getdataarray(document)
                        for row in gridparam:
                            row=row[:-2]
                            if row[0]=='':
                                pass # do not add the frequency data to either srcrec or receivers
                            elif row[0]==recid:
                                srcrec=row # single out the srcrec line and store it
                            else:
                                receivers.append(row) # any row not handled by code above gets added to the receiever list
    return srcrec, receivers, exists

# this function works
def calcSTL(srcrecInput, recsInput, qffInput, lfInput): # srcrec-source receiver, recs list of other receivers, qff-list of qff vals, lf - list of lf correction vals 
    stl=[] # =srcrec-6-avgSPL+correction
    # create average of all receivers bar src rec
    qff=list(qffInput.values())
    lf=list(lfInput.values())
    recs=[]
    srcrec=list(srcrecInput[1:])
    for rec in recsInput:
        recs.append(rec[1:])
    # avg SPL calculation
    avgSPL=[]
    numSrc=len(recs)
    count=0
    for rec in recs:
        for k,v in enumerate(rec):
            if count==0:
                avgSPL.append(float(v))
            else:
                avgSPL[k]+=float(v)
        count+=1
    for k,v in enumerate(avgSPL):
        avgSPL[k] /= numSrc
    # correction factor
    correction=[]
    for val in qff:
        correction.append(float(val))
    for k,v in enumerate(lf):
        correction[k]+=float(v)
    # stl calculation
    for k,v in enumerate(srcrec):
        stl.append(str(float(v)-6-avgSPL[k]+correction[k]))
    freq=('','100 Hz','125 Hz','160 Hz','200 Hz','250 Hz','315 Hz','400 Hz','500 Hz','630 Hz','800 Hz','1000 Hz','1250 Hz','1600 Hz','2000 Hz','2500 Hz','3150 Hz','4000 Hz','5000 Hz','6300 Hz','8000 Hz','10000 Hz')
    stl.insert(0,'STL')
    save=[freq,stl]
    return save
    
def SaveFile(saveData,path):
    data=list(saveData)
    # Gabe_rw(), stringarray(), floatarray() called from libsimpa
    gabewriter=Gabe_rw(len(data)) # create writer with length equal to data array length
    labelcol=stringarray()  # label col is assigned as an array of strings
    for cell in data[0][1:]:
        labelcol.append(cell.encode('cp1252')) 
    for col in data[1:]:
        datacol=floatarray()
        for cell in col[1:]:
            datacol.append(float(cell))
        gabewriter.AppendFloatCol(datacol,str(col[0]))
    gabewriter.Save(path.encode('cp1252'))    

class manager:
    def __init__(self):
        self.stlCalculationid=ui.application.register_event(self.stlCalculation) # register receiver select function to i-simpa
    def getmenu(self,elementType,elementId,menu):
        el=ui.element(elementId)
        infos=el.getinfos()
        if infos["name"]==u"Punctual receivers": # only display menu on Punctual receivers file
            menu.insert(0,())
            menu.insert(0,(u"STL Calculation",self.stlCalculationid))
            return True
        else:
            return False

    def stlCalculation(self,elementId):
        names=getNames(elementId) 
        uiTitle="STL Calculation"
        grp=ui.e_file(elementId)
        userInput1=ui.application.getuserinput(uiTitle,(u"Pick a Reciever from the list"),{"Excitation Receiver": names})
        if userInput1[0]:
            recid=userInput1[1]["Excitation Receiver"][-1]
            srcrec,receivers,exists=getVals(elementId, recid)
            if not exists:
                print("Please Merge Punctual Receivers SPL")
            elif exists:
                freqRange={"a. 100 Hz":"0","b. 125 Hz":"0","c. 160 Hz":"0","d. 200 Hz": "0", "e. 250 Hz": "0", "f. 315 Hz":"0", "g. 400 Hz":"0","h. 500 Hz":"0","i. 630 Hz":"0","j. 800 Hz":"0","k. 1000 Hz":"0","l. 1250 Hz":"0","m. 1600 Hz":"0","n. 2000 Hz":"0","o. 2500 Hz":"0","p. 3150 Hz":"0","q. 4000 Hz":"0","r. 5000 Hz":"0","s. 6300 Hz":"0","t. 8000 Hz":"0","u. 10000 Hz":"0"}
                userInput2=ui.application.getuserinput(uiTitle,(u"Please Input the QFF data"),freqRange)
                if userInput2[0]:
                    userInput3=ui.application.getuserinput(uiTitle,(u"Please Input Low Frequency Correction"),freqRange)
                    if userInput3[0]:
                        saveData=calcSTL(srcrec, receivers, userInput2[1], userInput3[1])
                        SaveFile(zip(*saveData),grp.buildfullpath()+r"STL Calculation.gabe")
                        ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)

ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location