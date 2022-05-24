# Author: Kyle Brooks
# Created: 18/01/22

import uictrl as ui
from libsimpa import *
from core_functions import *
import os

# this function works
def getNames(elementId):
    # if using the fusion files, it may not be needed to get the receiver element dicts.
    receivers=[] # array of receiver element dicts
    names=[] # array of receiver names
    folder=ui.element(elementId) # set folder
    recplist=folder.getallelementbytype(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER) # get all folders in folder
    for idrecp in recplist: # for each folder get info
        recp=ui.element(idrecp)
        infos=recp.getinfos()
        if infos["label"]!="Fused Receivers" and infos["label"]!="Source Contributions" and infos["label"]!="XYZ Plots" and infos["label"]!="Transmission Loss": # if receiver folder append to array receivers 
            receivers.append(infos)
    for receiver in receivers: # for each stored receiver append "label property to array names"
        names.append(receiver["label"])
    return names

# This function works
def getVals(elementId, recid):
    receivers=[]
    srcrec=None
    folders=ui.element(elementId)
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

def calcSTL(srcrecInput,recsInput,qff,lf):
    freq=('','100 Hz','125 Hz','160 Hz','200 Hz','250 Hz','315 Hz','400 Hz','500 Hz','630 Hz','800 Hz','1000 Hz','1250 Hz','1600 Hz','2000 Hz','2500 Hz','3150 Hz','4000 Hz','5000 Hz','6300 Hz','8000 Hz','10000 Hz')
    saveData=[freq]
    srcrec=list(srcrecInput)
    # Create correction factor
    correction=[]
    for k,v in enumerate(qff):
        correction.append((float(v)+float(lf[k])))
    # calculate transmission loss to each receiver
    for rec in recsInput:
        stl=[]
        for k,v in enumerate(srcrec):
            if k==0:
                stl.append(rec[k])
            else:
                stl.append(str(float(v)-6-float(rec[k])+correction[k-1]))
        saveData.append(stl)
    return saveData

# this function works
def calcAvgSTL(srcrecInput, recsInput, qff, lf): # srcrec-source receiver, recs list of other receivers, qff-list of qff vals, lf - list of lf correction vals 
    stl=[] # =srcrec-6-avgSPL+correction
    # create average of all receivers bar src rec
    recs=[]
    srcrec=list(srcrecInput[1:])
    for rec in recsInput:
        recs.append(rec[1:])
    # avg SPL calculation
    avgSPL=[]
    numRec=len(recs)
    count=0
    for rec in recs:
        for k,v in enumerate(rec):
            if count==0:
                avgSPL.append(float(v))
            else:
                avgSPL[k]+=float(v)
        count+=1
    for k,v in enumerate(avgSPL):
        avgSPL[k] /= numRec
    # correction factor
    correction=[]
    for k,v in enumerate(qff):
        correction.append((float(v)+float(lf[k])))
    # stl calculation
    for k,v in enumerate(srcrec):
        stl.append(str(float(v)-6-avgSPL[k]+correction[k]))
    freq=('','100 Hz','125 Hz','160 Hz','200 Hz','250 Hz','315 Hz','400 Hz','500 Hz','630 Hz','800 Hz','1000 Hz','1250 Hz','1600 Hz','2000 Hz','2500 Hz','3150 Hz','4000 Hz','5000 Hz','6300 Hz','8000 Hz','10000 Hz')
    stl.insert(0,'STL')
    save=[freq,stl]
    return save

def removeNaN(receivers):
    nanCount=0
    newRecs = []
    for receiver in receivers:
        recId=receiver[0]
        receiver=receiver[1:]
        for k,v in enumerate(receiver):
            if 'inf' in str(v): 
                receiver[k]=50
                nanCount+=1
        receiver.insert(0,recId)
        newRecs.append(receiver)
    return newRecs, nanCount

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
        userInput1=ui.application.getuserinput(uiTitle,(u"Pick the Excitation Receiver from the list"),{"Excitation Receiver": names})
        if userInput1[0]:
            try:
                recid=userInput1[1]["Excitation Receiver"]
                srcrec,receivers,exists=getVals(elementId, recid)
                if not exists:
                    print("Please Merge Punctual Receivers SPL")
                elif exists:
                    receivers,nanCount = removeNaN(receivers) 
                    print("%s inf values detected" % nanCount)
                    if nanCount > 10:
                        print("High Trasmission Loss Detected!\n")
                    userInput2=ui.application.getuserinput(uiTitle,"Use Correction Values?",{"QFF":["Yes","No"], "LF":["Yes","No"]})
                    if userInput2[0]:
                        el=ui.element(elementId)
                        infos=el.getinfos()
                        el2=ui.element(infos["parentid"])
                        solveId=infos["parentid"]
                        solvePath=ui.e_file(solveId)
                        infos2=el2.getinfos()
                        sppsId=infos2["parentid"]
                        sppsPath = ui.e_file(sppsId)
                        if userInput2[1]["QFF"]=="Yes" and userInput2[1]["LF"]=="Yes":
                            lfExists=os.path.exists(sppsPath.buildfullpath()+"LF_Correction.gabe")
                            qffExists=os.path.exists(solvePath.buildfullpath()+"QFF_Correction.gabe")
                            if lfExists and qffExists:
                                qff,lf=GetBothCorrection(sppsId,solveId)
                                saveAvgData=calcAvgSTL(srcrec,receivers,qff,lf)
                                saveData=calcSTL(srcrec, receivers,qff,lf)
                                targetDir= r"\Transmission Loss"
                                MakeDir(elementId, targetDir)
                                SaveFile(zip(*saveData),grp.buildfullpath()+r"Transmission Loss\STL Data.gabe")
                                SaveFile(zip(*saveAvgData),grp.buildfullpath()+r"Transmission Loss\Average STL Data.gabe")
                                ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)
                            elif lfExists and not qffExists:
                                print("Please create LF correcton file")
                            elif qffExists and not lfExists:
                                print("Please create LF correcton file")
                            else:
                                print("Please create both LF and QFF correction files")
                        elif userInput2[1]["QFF"]=="Yes" and userInput2[1]["LF"]=="No":
                            qffExists=os.path.exists(solvePath.buildfullpath()+"QFF_Correction.gabe")
                            if qffExists:
                                lf=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                                qff=GetQFFCorrection(solveId)
                                saveAvgData=calcAvgSTL(srcrec,receivers,qff,lf)
                                saveData=calcSTL(srcrec, receivers,qff,lf)
                                targetDir= r"\Transmission Loss"
                                MakeDir(elementId, targetDir)
                                SaveFile(zip(*saveData),grp.buildfullpath()+r"Transmission Loss\STL Data.gabe")
                                SaveFile(zip(*saveAvgData),grp.buildfullpath()+r"Transmission Loss\Average STL Data.gabe")
                                ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)
                            else:
                                print("Please create QFF correction file")
                        elif userInput2[1]["QFF"]=="No" and userInput2[1]["LF"]=="Yes":
                            lfExists=os.path.exists(sppsPath.buildfullpath()+"LF_Correction.gabe")
                            if lfExists:
                                qff=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                                lf=GetLFCorrection(sppsId)
                                saveAvgData=calcAvgSTL(srcrec,receivers,qff,lf)
                                saveData=calcSTL(srcrec, receivers,qff,lf)
                                targetDir= r"\Transmission Loss"
                                MakeDir(elementId, targetDir)
                                SaveFile(zip(*saveData),grp.buildfullpath()+r"Transmission Loss\STL Data.gabe")
                                SaveFile(zip(*saveAvgData),grp.buildfullpath()+r"Transmission Loss\Average STL Data.gabe")
                                ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)
                            else:
                                print("Please create LF correction file")
                        else:
                            qff=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                            lf=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                            saveAvgData=calcAvgSTL(srcrec,receivers,qff,lf)
                            saveData=calcSTL(srcrec, receivers,qff,lf)
                            targetDir= r"\Transmission Loss"
                            MakeDir(elementId, targetDir)
                            SaveFile(zip(*saveData),grp.buildfullpath()+r"Transmission Loss\STL Data.gabe")
                            SaveFile(zip(*saveAvgData),grp.buildfullpath()+r"Transmission Loss\Average STL Data.gabe")
                            ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)
            except:
                print("An Error Occured calculating the transmission loss")
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location