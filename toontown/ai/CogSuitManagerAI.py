from toontown.coghq import CogDisguiseGlobals
from toontown.toonbase import ToontownGlobals

import random


class CogSuitManagerAI:
    def __init__(self, air):
        self.air = air

    def recoverPart(self, toon, factoryType, suitTrack, zoneId, toons):
        recoveredParts = [0, 0, 0, 0]
        parts = toon.getCogParts()
        suitIndex = ToontownGlobals.cogDept2index[suitTrack]

        if CogDisguiseGlobals.isSuitComplete(parts, suitIndex):
            return recoveredParts

        recoveredParts[suitTrack] = toon.giveGenericCogPart(factoryType, suitIndex)
        return recoveredParts

    def removeParts(self, toonId, suitDeptIndex):
        toon = self.air.doId2do.get(toonId)

        # Check if the toon is in our doId2do:
        if toon is not None:
            parts = toon.getCogParts()
            if CogDisguiseGlobals.isSuitComplete(parts, suitDeptIndex):
                toon.loseCogParts(suitDeptIndex)

        def dbCallback(dclass, fields, toonId=toonId, suitDeptIndex=suitDeptIndex):
            if dclass != self.air.dclassesByName['DistributedToonAI']:
                return

            parts = fields['setCogParts'][0]
            if CogDisguiseGlobals.isSuitComplete(parts, suitDeptIndex):
                # Code from DistributedToonAI.loseCogParts:
                loseCount = random.randrange(CogDisguiseGlobals.MinPartLoss,
                                             CogDisguiseGlobals.MaxPartLoss+1)

                partBitmask = parts[suitDeptIndex]
                partList = range(17)

                while loseCount > 0 and partList:
                    losePart = random.choice(partList)
                    partList.remove(losePart)

                    losePartBit = 1 << losePart
                    if partBitmask & losePartBit:
                        partBitmask &= ~losePartBit
                        loseCount -= 1

                parts[suitDeptIndex] = partBitmask

                # Update the cog parts in the db:
                self.air.dbInterface.updateObject(
                    self.air.dbId, toonId,
                    self.air.dclassesByName['DistributedToonAI'],
                    {'setCogParts': (parts,)}
                )

        # It doesn't look like the toon was in our doId2do. Lets query the db:
        self.air.dbInterface.queryObject(self.air.dbId, toonId, dbCallback)
