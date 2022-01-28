# Author: Kyle Brooks
# Created: 28/01/2022

from libsimpa import *
import uictrl as ui

def createMatrix(xVals,yVals,recIds):
  # recIds is an array of all the receiver IDs
  pass

class manager:
  def __init__(self):
    pass
  def getmenu(self,elementType,elementId,menu):
    el=ui.element(elementId)
    infos=el.getinfos()
    if infos["name"]==u"Punctual receivers": # only display menu on Punctual receivers file
        menu.insert(0,())
        menu.insert(0,(u"Plot as XYZ",self.stlCalculationid))
        return True
    else:
      return False