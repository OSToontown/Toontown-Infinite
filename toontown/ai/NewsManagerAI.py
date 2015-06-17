from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.ai.NewsManagerGlobals import DEFAULT_WEEKLY_HOLIDAYS, DEFAULT_YEARLY_HOLIDAYS


class NewsManagerAI(DistributedObjectAI):
    notify = directNotify.newCategory('NewsManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.weeklyHolidays = DEFAULT_WEEKLY_HOLIDAYS
        self.yearlyHolidays = DEFAULT_YEARLY_HOLIDAYS
        self.OncelyHolidays = []

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        self.accept('avatarEntered', self.__handleAvatarEntered)

    def __handleAvatarEntered(self, avatar):
        if self.air.suitInvasionManager.getInvading():
            self.air.suitInvasionManager.notifyInvasionBulletin(avatar.getDoId())

    def setPopulation(self, todo0):
        pass

    def setBingoWin(self, todo0):
        pass

    def setBingoStart(self):
        pass

    def setBingoEnd(self):
        pass

    def setCircuitRaceStart(self):
        pass

    def setCircuitRaceEnd(self):
        pass

    def setTrolleyHolidayStart(self):
        pass

    def setTrolleyHolidayEnd(self):
        pass

    def setTrolleyWeekendStart(self):
        pass

    def setTrolleyWeekendEnd(self):
        pass

    def setRoamingTrialerWeekendStart(self):
        pass

    def setRoamingTrialerWeekendEnd(self):
        pass

    def setInvasionStatus(self, msgType, cogType, numRemaining, skeleton):
        self.sendUpdate('setInvasionStatus', args=[msgType, cogType, numRemaining, skeleton])

    def d_setHolidayIdList(self, holidays):
        self.sendUpdate('setHolidayIdList', holidays)

    def holidayNotify(self):
        pass

    def d_setWeeklyCalendarHolidays(self, weeklyHolidays):
        self.sendUpdate('setWeeklyCalendarHolidays', [weeklyHolidays])

    def getWeeklyCalendarHolidays(self):
        return self.weeklyHolidays

    def d_setYearlyCalendarHolidays(self, yearlyHolidays):
        self.sendUpdate('setYearlyCalendarHolidays', [yearlyHolidays])

    def getYearlyCalendarHolidays(self):
        return self.yearlyHolidays

    def setOncelyCalendarHolidays(self, todo0):
        pass

    def getOncelyCalendarHolidays(self):
        return []

    def setRelativelyCalendarHolidays(self, todo0):
        pass

    def getRelativelyCalendarHolidays(self):
        return []

    def setMultipleStartHolidays(self, todo0):
        pass

    def getMultipleStartHolidays(self):
        return []

    def sendSystemMessage(self, todo0, todo1):
        pass
