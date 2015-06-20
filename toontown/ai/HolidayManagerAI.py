from toontown.ai.NewsManagerGlobals import DEFAULT_YEARLY_HOLIDAYS, DEFAULT_WEEKLY_HOLIDAYS
from toontown.toonbase.HolidayGlobals import *

from otp.ai.MagicWordGlobal import *

from datetime import datetime, date

HOLIDAY_CHECK_INTERVAL = 21600
SILLY_SATURDAY_CYCLE = 7200


class HolidayManagerAI:

    def __init__(self, air):
        self.air = air
        self.currentHolidays = []
        self.magicWordHolidays = []
        self.currentSillySaturdayCycle = [None, None]
        self.xpMultiplier = 1
        self.setup()
        self.yearlyHolidayTask()
        self.weeklyHolidayTask()

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
        if MORE_XP_HOLIDAY in self.currentHolidays:
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
        if holidayId == TRICK_OR_TREAT:
            for hood in self.air.hoods:
                hood.startupTrickOrTreat()

        elif holidayId == WINTER_CAROLING:
            for hood in self.air.hoods:
                hood.startupWinterCaroling()

        elif holidayId in (FISH_BINGO_NIGHT, SILLY_SATURDAY_BINGO):
            for hood in self.air.hoods:
                for fishingPond in hood.fishingPonds:
                    fishingPond.bingoMgr.b_enableBingo()

            for estate in self.air.estateManager.estate2toons.keys():
                if estate.pond:
                    estate.pond.bingoMgr.enableBingo()

            self.air.newsManager.setBingoStart()

        elif holidayId in (TROLLEY_HOLIDAY, SILLY_SATURDAY_TROLLEY):
            self.air.newsManager.setTrolleyHolidayStart()

        if holidayId in (SILLY_SATURDAY_BINGO, SILLY_SATURDAY_TROLLEY):
            if self.currentSillySaturdayCycle[0] is None:
                self.currentSillySaturdayCycle = [
                    0 if holidayId == SILLY_SATURDAY_BINGO else 1, holidayId
                ]
            taskMgr.remove('Silly-Saturday')
            taskMgr.doMethodLater(SILLY_SATURDAY_CYCLE, self.sillySaturdayTask, 'Silly-Saturday')

    def removeHoliday(self, holidayId):
        if holidayId in self.currentHolidays:
            self.currentHolidays.remove(holidayId)

        simbase.air.newsManager.d_setHolidayIdList([self.currentHolidays])

    def endHoliday(self, holidayId):
        if holidayId == TRICK_OR_TREAT:
            for hood in self.air.hoods:
                hood.endTrickOrTreat()

        elif holidayId == WINTER_CAROLING:
            for hood in self.air.hoods:
                hood.endWinterCaroling()

        elif holidayId in (FISH_BINGO_NIGHT, SILLY_SATURDAY_BINGO):
            for hood in self.air.hoods:
                for fishingPond in hood.fishingPonds:
                    fishingPond.bingoMgr.disableBingo()

            for estate in self.air.estateManager.estate2toons.keys():
                if estate.pond:
                    estate.pond.bingoMgr.disableBingo()

            self.air.newsManager.setBingoEnd()

        elif holidayId in (TROLLEY_HOLIDAY, SILLY_SATURDAY_TROLLEY):
            self.air.newsManager.setTrolleyHolidayEnd()

    def yearlyHolidayTask(self, task=None):
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

        taskMgr.doMethodLater(HOLIDAY_CHECK_INTERVAL, self.yearlyHolidayTask, 'yearlyHolidayTask')

    def weeklyHolidayTask(self, task=None):
        for holiday in DEFAULT_WEEKLY_HOLIDAYS:
            holidayId = holiday[0]
            startDay = holiday[1]
            if holidayId in self.magicWordHolidays:
                return
            if startDay == date.today().weekday() and holidayId not in self.currentHolidays:
                self.appendHoliday(holidayId)
                self.startHoliday(holidayId)
            else:
                if startDay == 5:
                    holidayId = self.currentSillySaturdayCycle[1]

                if holidayId in self.currentHolidays:
                    self.removeHoliday(holidayId)
                    self.endHoliday(holidayId)

                if holidayId == self.currentSillySaturdayCycle[1]:
                    taskMgr.remove('Silly-Saturday')
                    self.currentSillySaturdayCycle = [None, None]

        taskMgr.doMethodLater(HOLIDAY_CHECK_INTERVAL, self.weeklyHolidayTask, 'weeklyHolidayTask')

    def sillySaturdayTask(self, task=None):
        if self.currentSillySaturdayCycle[0] is None:
            return

        self.endHoliday(self.currentSillySaturdayCycle[1])
        self.removeHoliday(self.currentSillySaturdayCycle[1])

        self.currentSillySaturdayCycle[0] ^= 1

        if self.currentSillySaturdayCycle[1] == SILLY_SATURDAY_TROLLEY:
            self.currentSillySaturdayCycle[1] = SILLY_SATURDAY_BINGO
        else:
            self.currentSillySaturdayCycle[1] = SILLY_SATURDAY_TROLLEY

        self.appendHoliday(self.currentSillySaturdayCycle[1])
        self.startHoliday(self.currentSillySaturdayCycle[1])

    def cleanup(self):
        taskMgr.remove('yearlyHolidayTask')
        taskMgr.remove('weeklyHolidayTask')
        taskMgr.remove('Silly-Saturday')

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
