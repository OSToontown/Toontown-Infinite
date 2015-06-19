from toontown.ai.NewsManagerGlobals import DEFAULT_YEARLY_HOLIDAYS
from toontown.toonbase import ToontownGlobals

from otp.ai.MagicWordGlobal import *

from datetime import datetime

HOLIDAY_CHECK_INTERVAL = 21600


class HolidayManagerAI:

    def __init__(self, air):
        self.air = air
        self.currentHolidays = []
        self.magicWordHolidays = []
        self.xpMultiplier = 1
        self.setup()
        self.holidayTask()

    def setup(self):
        holidays = config.GetString('active-holidays', '')
        if holidays != '':
            for holiday in holidays.split(","):
                holiday = int(holiday)
                self.currentHolidays.append(holiday)
            simbase.air.newsManager.d_setHolidayIdList([self.currentHolidays])

    def isHolidayRunning(self, holidayId):
        if holidayId in self.currentHolidays:
            return True

    def isMoreXpHolidayRunning(self):
        if ToontownGlobals.MORE_XP_HOLIDAY in self.currentHolidays:
            self.xpMultiplier = 2
            return True
        return False

    def getXpMultiplier(self):
        return self.xpMultiplier

    def appendHoliday(self, holidayId):
        if holidayId not in self.currentHolidays:
            self.currentHolidays.append(holidayId)

        simbase.air.newsManager.d_setHolidayIdList([self.currentHolidays])

    def startHoliday(self, holidayId):
        if holidayId == ToontownGlobals.TRICK_OR_TREAT:
            for hood in self.air.hoods:
                hood.startupTrickOrTreat()

        elif holidayId == ToontownGlobals.WINTER_CAROLING:
            for hood in self.air.hoods:
                hood.startupWinterCaroling()

        elif holidayId == ToontownGlobals.FISH_BINGO_NIGHT:
            for hood in self.air.hoods:
                for fishingPond in hood.fishingPonds:
                    fishingPond.bingoMgr.b_enableBingo()

            for estate in self.air.estateManager.estate2toons.keys():
                if estate.pond:
                    estate.pond.bingoMgr.enableBingo()

    def removeHoliday(self, holidayId):
        if holidayId in self.currentHolidays:
            self.currentHolidays.remove(holidayId)

        simbase.air.newsManager.d_setHolidayIdList([self.currentHolidays])

    def endHoliday(self, holidayId):
        if holidayId == ToontownGlobals.TRICK_OR_TREAT:
            for hood in self.air.hoods:
                hood.endTrickOrTreat()

        elif holidayId == ToontownGlobals.WINTER_CAROLING:
            for hood in self.air.hoods:
                hood.endWinterCaroling()

        elif holidayId == ToontownGlobals.FISH_BINGO_NIGHT:
            for hood in self.air.hoods:
                for fishingPond in hood.fishingPonds:
                    fishingPond.bingoMgr.disableBingo()

            for estate in self.air.estateManager.estate2toons.keys():
                if estate.pond:
                    estate.pond.bingoMgr.disableBingo()

    def holidayTask(self, task=None):
        for holiday in DEFAULT_YEARLY_HOLIDAYS:
            holidayId = holiday[0]
            now = datetime.now()
            startDate = datetime(now.year, *holiday[1])
            endDate = datetime(now.year, *holiday[2])
            if holidayId in self.magicWordHolidays:
                return
            if startDate < now < endDate and holidayId not in self.currentHolidays:
                self.appendHoliday(holidayId)
                self.startHoliday(holidayId)
            elif endDate < now and holidayId in self.currentHolidays:
                self.removeHoliday(holidayId)
                self.endHoliday(holidayId)

        taskMgr.doMethodLater(HOLIDAY_CHECK_INTERVAL, self.holidayTask, 'holiday-Task')


@magicWord(category=CATEGORY_ADMINISTRATOR, types=[int])
def startHoliday(holidayId):
    if simbase.air.holidayManager.isHolidayRunning(holidayId):
        return 'That holiday is already running!'
    simbase.air.holidayManager.appendHoliday(holidayId)
    simbase.air.holidayManager.magicWordHolidays.append(holidayId)
    simbase.air.holidayManager.startHoliday(holidayId)
    return 'Successfully started holiday %d.' % holidayId


@magicWord(category=CATEGORY_ADMINISTRATOR, types=[int])
def stopHoliday(holidayId):
    if not simbase.air.holidayManager.isHolidayRunning(holidayId):
        return 'That holiday is\'nt running!'
    simbase.air.holidayManager.removeHoliday(holidayId)
    simbase.air.holidayManager.magicWordHolidays.remove(holidayId)
    simbase.air.holidayManager.endHoliday(holidayId)
    return 'Successfully stopped holiday %d.' % holidayId
