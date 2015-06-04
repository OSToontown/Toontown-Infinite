from toontown.estate.DistributedPlantBaseAI import DistributedPlantBaseAI
from toontown.estate import GardenGlobals

class DistributedGagTreeAI(DistributedPlantBaseAI):
    notify = directNotify.newCategory("DistributedGagTreeAI")

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedPlantBaseAI.__init__(self, air, gardenManager, ownerIndex)
        self.occupier = GardenGlobals.TreePlot

        self.wilted = None
        self.gagTrack = None
        self.gagLevel = None

    def d_setWilted(self, wiltedState):
        self.sendUpdate('setWilted', [wiltedState])

    def getWilted(self):
        return self.wilted

    def requestHarvest(self):
        pass

    def construct(self, gardenData):
        DistributedPlantBaseAI.construct(self, gardenData)

        self.wilted = gardenData.getUint8()

        self.gagTrack, self.gagLevel = GardenGlobals.getTreeTrackAndLevel(self.typeIndex)

    def pack(self, gardenData):
        gardenData.addUint8(self.occupier)

        DistributedPlantBaseAI.pack(self, gardenData)

        gardenData.addUint8(self.wilted)

    def movieDone(self):
        self.setMovie(GardenGlobals.MOVIE_FINISHPLANTING, self.air.getAvatarIdFromSender())
