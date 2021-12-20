# -*- coding: cp1252 -*-
# Modified: Kyle Brooks
# Created/Modified: 09/12/21

import uictrl as ui
from libsimpa import *
import os


def GetMixedLevel(folderwxid, target):
    cols=[]
    folder=ui.element(folderwxid)
    recplist=folder.getallelementbytype(ui.element_type.ELEMENT_TYPE_REPORT_GABE_RECP)
    for idrecp in recplist:
        recp=ui.element(idrecp)
        if recp.getinfos()["name"]=="Sound level":
            if not recp.getinfos()["name"]=="Acoustic parameters":
                ui.application.sendevent(recp,ui.idevent.IDEVENT_RECP_COMPUTE_ACOUSTIC_PARAMETERS,{"TR":"15;30", "EDT":"", "D":""})
            pere=ui.element(recp.getinfos()["parentid"])
            nomrecp=pere.getinfos()["label"]
            params=ui.element(pere.getelementbylibelle('Acoustic parameters'))
            gridparam=ui.application.getdataarray(params)
            if len(cols)==0: 
                cols.append(next(zip(*gridparam)))
                idcol=gridparam[0].index(target) 
            cols.append([nomrecp]+list(list(zip(*gridparam))[idcol][1:]))
    return cols

def SaveLevel(tab,path):
    tab1= list(tab)
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
    ui.application.sendevent(ui.element(ui.element(ui.application.getrootreport()).childs()[0][0]),ui.idevent.IDEVENT_RELOAD_FOLDER)

class manager:
    def __init__(self):
        self.GetSPL=ui.application.register_event(self.OnSPL)
        self.GetSPLA=ui.application.register_event(self.OnSPLA)
        self.GetC50=ui.application.register_event(self.OnC50)
        self.GetC80=ui.application.register_event(self.OnC80)
        self.GetTs=ui.application.register_event(self.OnTS)
        self.GetRT15=ui.application.register_event(self.OnRT15)
        self.GetRT30=ui.application.register_event(self.onRT30)
        self.GetEDT=ui.application.register_event(self.OnEDT)
        self.GetST=ui.application.register_event(self.OnST)
        self.GetAll=ui.application.register_event(self.OnAll)
        
    def getmenu(self,typeel,idel,menu):
        el=ui.element(idel)
        infos=el.getinfos()
        if infos["name"]==u"Punctual receivers":
            submenu=[(u"Do All", self.GetAll), (u"Sound Level", self.GetSPL), (u"Sound Level (A)", self.GetSPLA), (u"C-50", self.GetC50), (u"C-80", self.GetC80), (u"Ts", self.GetTs), (u"RT-15", self.GetRT15), (u"RT-30", self.GetRT30), (u"EDT",self.GetEDT), (u"ST", self.GetST)]
            menu.insert(0,()) 
            menu.insert(0,(u"Merge Point Recievers",submenu))
            return True
        else:
            return False
    def MakeDir(self, idel):
        grp=ui.e_file(idel)
        pat=grp.buildfullpath()+ r"\Fused Recievers"
        if not os.path.exists(pat):
            os.mkdir(pat)
    def OnSPL(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Recievers\fusionSPL.gabe", "Sound level (dB)")
        print("Creating file fusionSPL.gabe")
    def OnSPLA(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Recievers\fusionSPLA.gabe", "Sound level (dBA)")
        print("Creating file fusionSPLA.gabe")
    def OnC50(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Recievers\fusionC50.gabe", "C-50 (dB)")
        print("Creating file fusionC50.gabe")
    def OnC80(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Recievers\fusionC80.gabe", "C-80 (dB)")
        print("Creating file fusionC80.gabe")
    def OnTS(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Recievers\fusionTs.gabe", "Ts (ms)")
        print("Creating file fusionTs.gabe")
    def OnRT15(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Recievers\fusionRT15.gabe", "RT-15 (s)")
        print("Creating file fusionRT15.gabe")
    def onRT30(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Recievers\fusionRT30.gabe", "RT-30 (s)")
        print("Creating file fusionRT30.gabe")
    def OnEDT(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Recievers\fusionEDT.gabe", "EDT (s)")
        print("Creating file fusionEDT.gabe")
    def OnST(self,idel):
        self.MakeDir(idel)
        grp=ui.e_file(idel)
        do_fusion(idel,grp.buildfullpath()+ r"Fused Recievers\fusionST.gabe", "ST (dB)")
        print("Creating file fusionST.gabe")
    def OnAll(self,idel):
        self.OnSPL(idel)
        self.OnSPLA(idel)
        self.OnC50(idel)
        self.OnC80(idel)
        self.OnTS(idel)
        self.OnRT15(idel)
        self.onRT30(idel)
        self.OnEDT(idel)
        self.OnST(idel)
ui.application.register_menu_manager(ui.element_type.ELEMENT_TYPE_REPORT_FOLDER, manager())