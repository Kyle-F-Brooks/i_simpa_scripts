import uictrl as ui

class mdf(ui.element):
    """
    Diffusion model calculation core.
    """
    def __init__(self,idel):
        ui.element.__init__(self,idel)
        if not self.hasproperty("exeName"): #Test if this is a new project initialisation
            #If this is a new project then we add properties
            #Add tetgen parameters
            self.appendfilsbytype(ui.element_type.ELEMENT_TYPE_CORE_CORE_CONFMAILLAGE)
            #Add frequencies selection
            self.appendfilsbytype(ui.element_type.ELEMENT_TYPE_CORE_CORE_BFREQSELECTION)
            #Add configuration core
            coreconf=ui.element(self.appendfilsbytype(ui.element_type.ELEMENT_TYPE_CORE_CORE_CONFIG))
            #Append hidden config, used by I-SIMPA to find the core files and binaries
            ui.element(self.appendpropertytext("modelName","","mesh.cbin",True,True)).hide()
            ui.element(self.appendpropertytext("tetrameshFileName","","tetramesh.mbin",True,True)).hide()
            ui.element(self.appendpropertytext("exeName","","md.py")).hide()
            ui.element(self.appendpropertytext("corePath","","md\\")).hide()
            #User options
            coreconf.appendpropertylist("solver_mode","Calculation mode",[["Time","Static"],[0,1]],0,False,1,True)
            coreconf.appendpropertybool("with_direct_sound","Use direct sound",True,True)
            _("Calculation mode")
            _("Use direct sound")
            _("Time")
            _("Static")
        else:
            pass #Here in case of loading an existing project