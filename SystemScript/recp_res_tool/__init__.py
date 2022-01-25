# -*- coding: cp1252 -*-
# Modified: Kyle Brooks
# Created/Modified: 09/12/21

# Combines each value of a chosen measurement into a single file to allow for easier processing of data. Each file 
# gets saved in a folder called "Fused Receivers" and the file name is appended with the measurement that was chosen.

import uictrl as ui
from libsimpa import *
import os


def GetMixedLevel(folderwxid, target):
    # target refers to the measurement type desired for output
    cols=[]
    folder=ui.element(folderwxid)
    recplist=folder.getallelementbytype(ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECP)
    for idrecp in recplist: # for each punctual receiver in folder "Punctual receivers"
        recp=ui.element(idrecp)
        # once the spps is calculated a file named "Sound level" will be in the Project > Results tree
        if recp.getinfos()["name"]=="Sound level":
            if not recp.getinfos()["name"]=="Acoustic parameters": # if the acoustic parameters have not yet been calculated then calculate them
                ui.application.sendevent(recp,ui.idevent.IDEVENT_RECP_COMPUTE_ACOUSTIC_PARAMETERS,{"TR":"15;30", "EDT":"", "D":""})
            # get the acoustics parameters file
            pere=ui.element(recp.getinfos()["parentid"])
            nomrecp=pere.getinfos()["label"]
            params=ui.element(pere.getelementbylibelle('Acoustic parameters'))
            gridparam=ui.application.getdataarray(params)
            if len(cols)==0: # with array cols empty 
                cols.append(next(zip(*gridparam))) # add frequency row
                idcol=gridparam[0].index(target) # set target column equal to the target title
            cols.append([nomrecp]+list(list(zip(*gridparam))[idcol][1:])) # add data from reciever to new row
    return cols

def SaveLevel(tab,path):
    tab1=list(tab)
    # Gabe_rw(), stringarray(), floatarray() called from libsimpa
    gabewriter=Gabe_rw(len(tab1))
    labelcol=stringarray()
    for cell in tab1[0][1:]:
        labelcol.append(cell.encode('cp1252')) 
    for col in tab1[1:]:
        datacol=floatarray()
        for cell in col[1:]:
            datacol.append(float(cell))
        gabewriter.AppendFloatCol(datacol,str(col[0]))
    gabewriter.Save(path.encode('cp1252')) 
    
def do_fusion(folderwxid, path, target):
    arraydata=GetMixedLevel(folderwxid, target)
    SaveLevel(zip(*arraydata),path)
    # reload folder to show newly created files
    ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)

class manager:
    def __init__(self):
        # add functions as an event in I-SIMPA
        self.GetSPL=ui.application.register_event(self.OnSPL)
        self.GetSPLA=ui.application.register_event(self.OnSPLA)
        self.GetC50=ui.application.register_event(self.OnC50)
        self.GetC80=ui.application.register_event(self.OnC80)
        self.GetTs=ui.application.register_event(self.OnTS)
        self.GetRT15=ui.application.register_event(self.OnRT15)
        self.GetRT30=ui.application.register_event(self.OnRT30)
        self.GetEDT=ui.application.register_event(self.OnEDT)
        self.GetST=ui.application.register_event(self.OnST)
        self.GetAll=ui.application.register_event(self.OnAll)
        
    def getmenu(self,typeel,idel,menu):
        # Create the additional menu buttons and link the function they initiate
        el=ui.element(idel)
        infos=el.getinfos()
        if infos["name"]==u"Punctual receivers":
            submenu=[(u"Do All", self.GetAll), (u"Sound Level", self.GetSPL), (u"Sound Level (A)", self.GetSPLA), (u"C-50", self.GetC50), (u"C-80", self.GetC80), (u"Ts", self.GetTs), (u"RT-15", self.GetRT15), (u"RT-30", self.GetRT30), (u"EDT",self.GetEDT), (u"ST", self.GetST)]
            menu.insert(0,()) 
            menu.insert(0,(u"Merge Point Receivers",submenu))
            return True
        else:
            return False

    # creates the Fused Receivers folder if it does not yet exist
    def MakeDir(self, idel):
        grp=ui.e_file(idel)
        pat=grp.buildfullpath()+ r"\Fused Receivers"
        if not os.path.exists(pat):
            os.mkdir(pat)
    # button commands, create file name and prints process to the pyhton console
    def OnSPL(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Receivers\fusionSPL.gabe", "Sound level (dB)")
        print("Created file fusionSPL.gabe")
    def OnSPLA(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Receivers\fusionSPLA.gabe", "Sound level (dBA)")
        print("Created file fusionSPLA.gabe")
    def OnC50(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Receivers\fusionC50.gabe", "C-50 (dB)")
        print("Created file fusionC50.gabe")
    def OnC80(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Receivers\fusionC80.gabe", "C-80 (dB)")
        print("Created file fusionC80.gabe")
    def OnTS(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Receivers\fusionTs.gabe", "Ts (ms)")
        print("Created file fusionTs.gabe")
    def OnRT15(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Receivers\fusionRT15.gabe", "RT-15 (s)")
        print("Created file fusionRT15.gabe")
    def OnRT30(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Receivers\fusionRT30.gabe", "RT-30 (s)")
        print("Created file fusionRT30.gabe")
    def OnEDT(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Receivers\fusionEDT.gabe", "EDT (s)")
        print("Created file fusionEDT.gabe")
    def OnST(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Receivers\fusionST.gabe", "ST (dB)")
        print("Created file fusionST.gabe")
    def OnAll(self,idel):
        self.OnSPL(idel)
        self.OnSPLA(idel)
        self.OnC50(idel)
        self.OnC80(idel)
        self.OnTS(idel)
        self.OnRT15(idel)
        self.OnRT30(idel)
        self.OnEDT(idel)
        self.OnST(idel)

# register tool and let the application know which menu to put the tool buttons into
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager())