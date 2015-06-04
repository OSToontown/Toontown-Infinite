from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram

from toontown.estate.DistributedGardenPlotAI import DistributedGardenPlotAI
from toontown.estate.DistributedGagTreeAI import DistributedGagTreeAI
from toontown.estate import GardenGlobals

from time import time

occupier2Class = {
    GardenGlobals.EmptyPlot: DistributedGardenPlotAI,
    GardenGlobals.TreePlot: DistributedGagTreeAI
}


class GardenManagerAI:
    notify = directNotify.newCategory('GardenManagerAI')

    def __init__(self, air, house):
        self.air = air
        self.house = house

        self.plots = []

    def loadGarden(self):
        if not self.house.hasGardenData():
            self.createBlankGarden()
            return

        self.createGardenFromData(self.house.getGardenData())

    def createBlankGarden(self):
        gardenData = PyDatagram()

        plots = GardenGlobals.getGardenPlots(self.house.housePos)

        gardenData.addUint8(len(plots))

        for i, plotData in enumerate(plots):
            gardenData.addUint8(GardenGlobals.EmptyPlot)
            gardenData.addUint8(i)

        self.house.b_setGardenData(gardenData.getMessage())
        self.loadGarden()

    def createGardenFromData(self, gardenData):
        dg = PyDatagram(gardenData)
        gardenData = PyDatagramIterator(dg)
        plotCount = gardenData.getUint8()
        for _ in xrange(plotCount):
            occupier = gardenData.getUint8()
            if occupier not in occupier2Class:
                continue
            plot = occupier2Class[occupier](self.air, self, self.house.housePos)
            plot.construct(gardenData)
            plot.generateWithRequired(self.house.zoneId)

            self.plots.append(plot)

    def updateGardenData(self):
        gardenData = PyDatagram()

        gardenData.addUint8(len(self.plots))
        for plot in self.plots:
            plot.pack(gardenData)

        self.house.b_setGardenData(gardenData.getMessage())

    def delete(self):
        for plot in self.plots:
            plot.requestDelete()

    def getTimestamp(self):
        return int(time())

    def constructTree(self, plotIndex, gagTrack, gagLevel):
        self.plots[plotIndex].setMovie(GardenGlobals.MOVIE_PLANT, self.air.getAvatarIdFromSender())
        dg = PyDatagram()
        dg.addUint8(plotIndex)
        dg.addUint8(GardenGlobals.getTreeTypeIndex(gagTrack, gagLevel))  # Type Index
        dg.addInt8(0)  # Water Level
        dg.addInt8(0)  # Growth Level
        dg.addUint32(self.getTimestamp())
        dg.addUint8(0)  # Wilted State (False)
        gardenData = PyDatagramIterator(dg)

        plot = occupier2Class[GardenGlobals.TreePlot](self.air, self, self.house.housePos)
        plot.construct(gardenData)
        self.plots[plotIndex] = plot

        self.updateGardenData()

    def treeFinished(self, plotIndex):
        tree = self.plots[plotIndex]
        tree.generateWithRequired(self.house.zoneId)
        tree.setMovie(GardenGlobals.MOVIE_FINISHPLANTING, self.air.getAvatarIdFromSender())