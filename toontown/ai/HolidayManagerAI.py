from toontown.ai.NewsManagerGlobals import DEFAULT_YEARLY_HOLIDAYS
from toontown.toonbase import ToontownGlobals

from datetime import datetime

HOLIDAY_CHECK_INTERVAL = 21600


class HolidayManagerAI:

    def __init__(self, air):
        self.air = air
        self.currentHolidays = []
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

    def holidayTask(self, task=None):
        for holiday in DEFAULT_YEARLY_HOLIDAYS:
            holidayId = holiday[0]
            now = datetime.now()
            startDate = datetime(now.year, *holiday[1])
            endDate = datetime(now.year, *holiday[2])
            if startDate < now < endDate and holidayId not in self.currentHolidays:
                self.appendHoliday(holidayId)
                self.startHoliday(holidayId)
            elif endDate < now and holidayId in self.currentHolidays:
                self.removeHoliday(holidayId)
                self.endHoliday(holidayId)

        taskMgr.doMethodLater(HOLIDAY_CHECK_INTERVAL, self.holidayTask, 'holiday-Task')
