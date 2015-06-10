from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.task import Task

MANAGER_DOID = 0
HEARTBEAT_INTERVAL = 2.5


class GlobalOtpObjectAI(DistributedObjectGlobalAI):
    notify = directNotify.newCategory('GlobalOtpObjectAI')

    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)
        if not MANAGER_DOID:
            self.notify.warning('A manager DoId is not defined!')
            return

        self.uberdogUp = False
        self.sendUpdate('hello', [MANAGER_DOID])
        taskMgr.doMethodLater(HEARTBEAT_INTERVAL * 2, self.reportUdLost, self.uniqueName('noResponseTask'))

    def startHeartbeat(self):
        taskMgr.remove(self.uniqueName('noResponseTask'))
        self.uberdogUp = True
        taskMgr.doMethodLater(HEARTBEAT_INTERVAL, self.heartbeat, self.uniqueName('heartbeatTask'))

    def heartbeat(self, task):
        self.sendUpdate('heartbeat', [MANAGER_DOID])
        taskMgr.doMethodLater(HEARTBEAT_INTERVAL, self.reportUdLost, self.uniqueName('heartbeatLostTask'))
        return Task.again

    def heartbeatResponse(self):
        self.uberdogUp = True
        taskMgr.remove(self.uniqueName('heartbeatLostTask'))

    def reportUdLost(self, task):
        self.notify.warning('Connection to the Uberdog was lost!')
        self.uberdogUp = False
        if task.name == self.uniqueName('noResponseTask'):
            self.startHeartbeat()
            return Task.done
