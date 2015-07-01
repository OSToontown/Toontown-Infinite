from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.ClockDelta import globalClockDelta

from toontown.chat.TTWhiteList import TTWhiteList


class ChatAgentUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("ChatAgentUD")

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        self.whiteList = TTWhiteList()

    def chatMessage(self, message):
        sender = self.air.getAvatarIdFromSender()
        if sender == 0:
            self.air.writeServerEvent('suspicious', self.air.getAccountIdFromSender(),
                                         'Account sent chat without an avatar', message)
            return

        modifications = []
        words = message.split(' ')
        offset = 0
        WantWhitelist = config.GetBool('want-whitelist', 1)
        for word in words:
            if word and not self.whiteList.isWord(word) and WantWhitelist:
                modifications.append((offset, offset+len(word)-1))
            offset += len(word) + 1

        cleanMessage = message
        for modStart, modStop in modifications:
            cleanMessage = cleanMessage[:modStart] + '*'*(modStop-modStart+1) + cleanMessage[modStop+1:]

        self.air.writeServerEvent('chat-said', sender, message, cleanMessage)

        dclass = self.air.dclassesByName['DistributedAvatarUD']
        dg = dclass.aiFormatUpdate(
            'setTalk', sender, sender, self.air.ourChannel,
            [0, 0, '', cleanMessage, modifications, 0,
             globalClockDelta.getRealNetworkTime(bits=16)])
        self.air.send(dg)
