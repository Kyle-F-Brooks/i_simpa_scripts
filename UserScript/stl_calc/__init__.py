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

# This function needs work
def getVals(folderwxid, recid):
    print("This should only show once")
    receivers=[]
    srcrec=None
    folder=ui.element(folderwxid)
    breakFree=False
    for el in folder.childs():
        if breakFree:
            break
        if el[1] == ui.element_type.ELEMENT_TYPE_REPORT_FOLDER:
            getVals(el[0],recid)
        elif el[1] in [ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECP, ui.element_type.ELEMENT_TYPE_REPORT_GABE, ui.element_type.ELEMENT_TYPE_REPORT_GABE_GAP, ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECPS]:
            document = ui.e_file(el[0])
            if document.getinfos()["name"]=="fusionSPL":
                gridparam=ui.application.getdataarray(document)
                for row in gridparam:
                    print(row[0])
                    if row[0]==recid:
                        print("source receiver")
                        breakFree=True
                        srcrec=row
                    if row[0]=='':
                        print("freq")
                        breakFree=True
                        pass
                    else:
                        print("rest")
                        breakFree=True
                        receivers.append(row)
    print("This is the thing: ") # this currently occurs 4 times and ends up clearing srcrec and receivers
    print(srcrec)
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
        # function creates a pop up menu where the user can select a source
        names=getNames(idel)
        uiTitle="STL Calculation WIP"
        userInput1=ui.application.getuserinput(uiTitle,(u"Pick a Reciever from the list"),{"Excitation Receiver": names})
        # getuserinput returns Tuple of (Bool, dict)
        # for receiver in receivers:
        if userInput1[0]:
            recid=userInput1[1]["Excitation Receiver"][-1]
            srcrec,receivers=getVals(idel, recid)
            # userInput2=ui.application.getuserinput(uiTitle,(u"Please Input the QFF data"),{"50Hz":"0","63":"0","80":"0","100":"0","125":"0","160":"0","200 Hz": "0", "250 Hz": "0", "315 Hz":"0", "400 Hz":"0","500 Hz":"0","630 Hz":"0","800 Hz":"0","1000 Hz":"0","1250 Hz":"0","1600 Hz":"0","2000 Hz":"0","2500 Hz":"0","3150 Hz":"0","4000 Hz":"0","5000 Hz":"0","6300 Hz":"0","8000 Hz":"0","10000 Hz":"0","12500":"0","16000":"0","20000":"0"})
            # if userInput2[0]:
            #     calcSTL(srcrec, receivers, userInput2[1])

ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location