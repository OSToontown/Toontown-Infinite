from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
from toontown.estate import GardenGlobals


class DistributedGardenPlotAI(DistributedLawnDecorAI):
    notify = directNotify.newCategory('DistributedGardenPlotAI')

    def __init__(self, air, ownerIndex):
        DistributedLawnDecorAI.__init__(self, air, ownerIndex)

        self.occupier = GardenGlobals.EmptyPlot

    def plantFlower(self, todo0, todo1):
        pass

    def plantGagTree(self, todo0, todo1):
        pass

    def plantStatuary(self, todo0):
        pass

    def plantToonStatuary(self, todo0, todo1):
        pass

    def plantNothing(self, todo0):
        pass

    def construct(self, gardenData):
        DistributedLawnDecorAI.construct(self, gardenData)

        self.occupier = gardenData.getUint8()

    def pack(self, gardenData):
        DistributedLawnDecorAI.pack(self, gardenData)

        gardenData.addUint8(self.occupier)
