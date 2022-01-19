import uictrl as ui
import libsimpa

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
    return names, receivers

def calcSTL(srcrec, recs, qff): # srcrec-source receiver, recs list of other receivers, qff-list of qff vals
    stl=[]
    #create average of all receivers bar src rec
    splex=0

    pass

def getVals(folderwxid, recid):
    receivers=[]
    folder=ui.element(folderwxid) # set folder
    recplist=folder.getallelementbytype(ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECP) # get all folders in folder
    for idrecp in recplist: # for each folder get info
        recp=ui.element(idrecp)
        infos=recp.getinfos()
        if infos["name"]=="fusedSPL": # if receiver folder append to array receivers 
            # store the row that relates to the excitation spl
            # add all others to array receivers
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
        names, receivers=getNames(idel)
        uiTitle="Function Currently Under Development"
        userInput1=ui.application.getuserinput(uiTitle,(u"Pick a Reciever from the list"),{"Excitation Receiver": names})
        # for receiver in receivers:
        #     if receiver["label"]==userInput1[1]["Please Pick a Receiver"]:
        #         print(receiver)
        if userInput1[0]:
            userInput2=ui.application.getuserinput(uiTitle,(u"Please Input the QFF data"),{"200 Hz": "0", "250 Hz": "0", "315 Hz":"0", "400 Hz":"0","500 Hz":"0","630 Hz":"0","800 Hz":"0","1000 Hz":"0","1250 Hz":"0","1600 Hz":"0","2000 Hz":"0","2500 Hz":"0","3150 Hz":"0","4000 Hz":"0","5000 Hz":"0","6300 Hz":"0","8000 Hz":"0","10000 Hz":"0"})

ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location