from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram

from toontown.estate.DistributedGardenPlotAI import DistributedGardenPlotAI
from toontown.estate import GardenGlobals


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
            gardenData.addUint8(i)
            gardenData.addUint8(GardenGlobals.EmptyPlot)

        self.house.b_setGardenData(gardenData.getMessage())
        self.loadGarden()

    def createGardenFromData(self, gardenData):
        dg = PyDatagram(gardenData)
        gardenData = PyDatagramIterator(dg)

        plotCount = gardenData.getUint8()
        for _ in xrange(plotCount):
            plot = DistributedGardenPlotAI(self.air, self, self.house.housePos)
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
