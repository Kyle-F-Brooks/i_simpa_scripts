import uictrl as ui
import libsimpa

def getNames(folderwxid):
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

class manager:
    def __init__(self):
        self.selectReceiverid=ui.application.register_event(self.selectReceiver) # register receiver select function to i-simpa
    def getmenu(self,typeel,idel,menu):
        el=ui.element(idel)
        infos=el.getinfos()
        if infos["name"]==u"Punctual receivers": # only display menu on Punctual receivers file
            menu.insert(0,())
            menu.insert(0,(u"Test Code",self.selectReceiverid))
            return True
        else:
            return False

    def selectReceiver(self,idel):
        # function creates a pop up menu where the user can select a source
        names, receivers=getNames(idel)
        input1=(u"Please Pick a Receiver")

        res=ui.application.getuserinput((u"Function Currently Under Development"),(u"Pick a Reciever from the list"),{input1 : names})

        for receiver in receivers:
            if receiver["label"]==res[1]["Please Pick a Receiver"]:
                print(receiver)



ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager()) # alter here based on menu location