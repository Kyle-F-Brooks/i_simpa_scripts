# Author: Kyle Brooks
# Created: 18/01/22

import uictrl as ui
import libsimpa

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
    for folder in folders.childs():
        if folder[2]=="Fused Receivers":
            files=ui.element(folder[0])
            for file in files.childs():
                if file[1]==ui.element_type.ELEMENT_TYPE_REPORT_GABE:
                    document = ui.e_file(file[0])
                    if document.getinfos()["name"]=="fusionSPL":
                        gridparam=ui.application.getdataarray(document)
                        for row in gridparam:
                            if row[0]=='':
                                pass
                            elif row[0]==recid:
                                srcrec=row
                            else:
                                receivers.append(row)
    return srcrec, receivers

def calcSTL(srcrec, recs, qffInput): # srcrec-source receiver, recs list of other receivers, qff-list of qff vals
    stl=[]
    # create average of all receivers bar src rec
    qffDict=qffInput.values()
    qff=list(qffDict)
    print(qff)
    print("\n")
    print(recs)
    print("\n")
    print(srcrec)
    pass

class manager:
    def __init__(self):
        self.selectReceiverid=ui.application.register_event(self.selectReceiver) # register receiver select function to i-simpa
    def getmenu(self,typeel,idel,menu):
        el=ui.element(idel)
        infos=el.getinfos()
        if infos["name"]==u"Punctual receivers": # only display menu on Punctual receivers file
            menu.insert(0,())
            menu.insert(0,(u"STL Calc(WIP)",self.selectReceiverid))
            return True
        else:
            return False

    def selectReceiver(self,idel):
        names=getNames(idel)
        uiTitle="STL Calculation WIP"
        userInput1=ui.application.getuserinput(uiTitle,(u"Pick a Reciever from the list"),{"Excitation Receiver": names})
        if userInput1[0]:
            recid=userInput1[1]["Excitation Receiver"][-1]
            srcrec,receivers=getVals(idel, recid)
            qffIn = {"50 Hz":"0","63 Hz":"0","80 Hz":"0","100 Hz":"0","125 Hz":"0","160 Hz":"0","200 Hz": "0", "250 Hz": "0", "315 Hz":"0", "400 Hz":"0","500 Hz":"0","630 Hz":"0","800 Hz":"0","1000 Hz":"0","1250 Hz":"0","1600 Hz":"0","2000 Hz":"0","2500 Hz":"0","3150 Hz":"0","4000 Hz":"0","5000 Hz":"0","6300 Hz":"0","8000 Hz":"0","10000 Hz":"0","12500 Hz":"0","16000 Hz":"0","20000 Hz":"0"}
            userInput2=ui.application.getuserinput(uiTitle,(u"Please Input the QFF data"),qffIn)
            if userInput2[0]:
                calcSTL(srcrec, receivers, userInput2[1])

ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location