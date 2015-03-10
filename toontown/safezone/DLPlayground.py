from toontown.classicchars import CCharPaths
from toontown.safezone import Playground
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals

base.camLens.setNearFar(ToontownGlobals.DreamlandCameraNear, ToontownGlobals.DreamlandCameraFar)

class DLPlayground(Playground.Playground):
    def showPaths(self):
        self.showPathPoints(CCharPaths.getPaths(TTLocalizer.Donald))
