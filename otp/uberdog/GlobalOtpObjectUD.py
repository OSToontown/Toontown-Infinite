from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

MANAGER_CLASS = ''


class GlobalOtpObjectUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('GlobalOtpObjectUD')

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.senders2Mgrs = {}

    def __makeAvMsg(self, field, values, recipient):
        return self.air.dclassesByName['DistributedToonUD'].getFieldByName(field).aiFormatUpdate(
            recipient, recipient, simbase.air.ourChannel, values)

    def sendToAvatar(self, avId, field, values):
        dg = self.__makeAvMsg(field, values, avId)
        self.air.send(dg)

    def __makeAIMsg(self, field, values, recipient):
        return self.air.dclassesByName[MANAGER_CLASS].getFieldByName(field).aiFormatUpdate(
            recipient, recipient, simbase.air.ourChannel, values)

    def sendToAI(self, field, values, sender=None):
        if not MANAGER_CLASS:
            self.notify.warning('A AI manager class is not implemented!')
            return

        if not sender:
            sender = self.air.getAvatarIdFromSender()

        dg = self.__makeAIMsg(field, values, self.senders2Mgrs.get(sender, sender + 8))
        self.air.send(dg)

    def hello(self, channel):
        if not MANAGER_CLASS:
            self.notify.warning('A AI manager class is not implemented!')
            return

        self.senders2Mgrs[simbase.air.getAvatarIdFromSender()] = channel

        # Manager classes must implement their own response to hello's
        self.sendToAI('UDResponse', [])

        self.air.addPostRemove(self.__makeAIMsg('UDLost', [], channel))

    def heartbeat(self, channel):
        if simbase.air.getAvatarIdFromSender() not in self.senders2Mgrs:
            self.senders2Mgrs[simbase.air.getAvatarIdFromSender()] = channel
        self.sendUpdateToChannel(simbase.air.getAvatarIdFromSender(), 'heartbeatResponse', [])
