from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
from toontown.estate import GardenGlobals

class DistributedPlantBaseAI(DistributedLawnDecorAI):
    notify = directNotify.newCategory("DistributedPlantBaseAI")

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedLawnDecorAI.__init__(self, air, gardenManager, ownerIndex)

        self.typeIndex = None
        self.waterLevel = None
        self.growthLevel = None
        self.timestamp = None

    def d_setTypeIndex(self, index):
        self.sendUpdate('setTypeIndex', [index])

    def getTypeIndex(self):
        return self.typeIndex

    def d_setWaterLevel(self, waterLevel):
        self.sendUpdate('setWaterLevel', [waterLevel])

    def getWaterLevel(self):
        return self.waterLevel

    def d_setGrowthLevel(self, growthLevel):
        self.sendUpdate('setGrowthLevel', [growthLevel])

    def getGrowthLevel(self):
        return self.growthLevel

    def waterPlant(self):
        self.waterLevel += 1
        self.d_setWaterLevel(self.waterLevel)
        self.setMovie(GardenGlobals.MOVIE_WATER, self.air.getAvatarIdFromSender())

    def waterPlantDone(self):
        pass

    def construct(self, gardenData):
        DistributedLawnDecorAI.construct(self, gardenData)

        self.typeIndex = gardenData.getUint8()
        self.waterLevel = gardenData.getInt8()
        self.growthLevel = gardenData.getInt8()

        self.timestamp = gardenData.getUint32()

    def pack(self, gardenData):
        DistributedLawnDecorAI.pack(self, gardenData)

        gardenData.addUint8(self.typeIndex)
        gardenData.addInt8(self.waterLevel)
        gardenData.addInt8(self.growthLevel)
        gardenData.addUint32(self.timestamp)
