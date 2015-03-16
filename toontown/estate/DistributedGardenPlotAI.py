from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
from toontown.estate import GardenGlobals


class DistributedGardenPlotAI(DistributedLawnDecorAI):
    notify = directNotify.newCategory('DistributedGardenPlotAI')

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedLawnDecorAI.__init__(self, air, gardenManager, ownerIndex)

        self.occupier = GardenGlobals.EmptyPlot

    def plantGagTree(self, gagTrack, gagLevel):
        pass

    def plantStatuary(self, species):
        pass

    def plantToonStatuary(self, species, dnaCode):
        pass

    def plantNothing(self, burntBeans):
        pass

    def construct(self, gardenData):
        DistributedLawnDecorAI.construct(self, gardenData)

        self.occupier = gardenData.getUint8()

    def pack(self, gardenData):
        DistributedLawnDecorAI.pack(self, gardenData)

        gardenData.addUint8(self.occupier)
