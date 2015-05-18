from toontown.toonbase import ToontownGlobals
import SellbotLegFactorySpec
import SellbotLegFactoryCogs
import LawbotLegFactorySpec
import LawbotLegFactoryCogs
import FactoryMockupSpec
import FactoryMockupCogs


def getFactorySpecModule(factoryId):
    return FactorySpecModules[factoryId]


def getCogSpecModule(factoryId):
    return CogSpecModules[factoryId]


FactorySpecModules = {ToontownGlobals.SellbotFactoryInt: FactoryMockupSpec,
 ToontownGlobals.LawbotOfficeInt: LawbotLegFactorySpec}
CogSpecModules = {ToontownGlobals.SellbotFactoryInt: FactoryMockupCogs,
 ToontownGlobals.LawbotOfficeInt: LawbotLegFactoryCogs}
