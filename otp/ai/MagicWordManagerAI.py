from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.ai.MagicWordGlobal import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *


class MagicWordManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("MagicWordManagerAI")

    def sendMagicWord(self, word, targetId):
        invokerId = self.air.getAvatarIdFromSender()
        invoker = self.air.doId2do.get(invokerId)
        target = self.air.doId2do.get(targetId)
        targets = spellbook.getTargets(word)

        if targets:
            if target is not None and target.__class__.__name__ not in targets:
                self.sendUpdateToAvatarId(invokerId, 'sendMagicWordResponse',
                                          ['Target is a %s object! Expected: %s' % (target.__class__.__name__, targets)])
                return

        if not invoker:
            self.sendUpdateToAvatarId(invokerId, 'sendMagicWordResponse', ['Missing invoker!'])
            return

        if invoker.getAdminAccess() < MINIMUM_MAGICWORD_ACCESS:
            self.air.writeServerEvent('suspicious', invokerId, 'Attempted to issue magic word: %s' % word)
            dg = PyDatagram()
            dg.addServerHeader(self.GetPuppetConnectionChannel(invokerId), self.air.ourChannel, CLIENTAGENT_EJECT)
            dg.addUint16(126)
            dg.addString('Magic Words are reserved for administrators only!')
            self.air.send(dg)
            return

        if target is None:
            self.sendUpdateToAvatarId(invokerId, 'sendMagicWordResponse', ['Missing target!'])
            return

        response = spellbook.process(invoker, target, word)
        if response:
            self.sendUpdateToAvatarId(invokerId, 'sendMagicWordResponse', [response])

        self.air.writeServerEvent('magic-word',
                                  invokerId, invoker.getAdminAccess(),
                                  targetId, target.getAdminAccess(),
                                  word, response)


@magicWord(category=CATEGORY_COMMUNITY_MANAGER, types=[str])
def help(wordName=None):
    print 'help called with %s' % (wordName)    
    if not wordName:
        return "What were you interested getting help for?"
    word = spellbook.words.get(wordName.lower())   # look it up by its lower case value
    if not word:
        accessLevel = spellbook.getInvoker().getAdminAccess()
        wname = wordName.lower()
        for key in spellbook.words:
            if spellbook.words.get(key).access <= accessLevel:
                if wname in key:
                    return 'Did you mean %s' % spellbook.words.get(key).name
        return 'I have no clue what %s is referring to' % wordName
    return word.doc


@magicWord(category=CATEGORY_COMMUNITY_MANAGER, types=[])
def words():
    accessLevel = spellbook.getInvoker().getAdminAccess()
    wordString = None
    for key in spellbook.words:
        word = spellbook.words.get(key)
        if word.access <= accessLevel:
            if wordString is None:
                wordString = key
            else:
                wordString += ", "
                wordString += key
    if wordString is None:
        return "You are chopped liver"
    else:
        return wordString
