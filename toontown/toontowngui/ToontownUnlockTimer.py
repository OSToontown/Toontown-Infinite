from pandac.PandaModules import NodePath, TextNode, TransparencyAttrib, Vec3
from direct.interval.IntervalGlobal import Sequence, LerpScaleInterval
from direct.gui.OnscreenImage import OnscreenImage
from toontown.toonbase import ToontownGlobals
import time

class ToontownUnlockTimer:

    def __init__(self, unlockTime, timerText):
        self.unlockTime = unlockTime
        self.timerText = timerText
        self.logo = None
        self.logoScaleSequence = None
        self.background = None
        self.timerParent = NodePath('timer-parent')
        self.message = None
        self.timer = None
        return

    def start(self):
        self.createTimer()
        taskMgr.add(self.__tick, 'timer-tick')

    def createTimer(self):
        self.timerParent.reparentTo(base.aspect2d)
        self.background = OnscreenImage(parent=base.render2d, image='phase_3.5/maps/blueprint.png', scale=(1, 1, 1), pos=(0, 0, 0))
        self.logo = OnscreenImage(parent=base.a2dTopCenter, image='phase_3/maps/toontown-logo.png', scale=(0.9, 1, 0.4), pos=(0, 0, -0.9))
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        self.logoScaleSequence = Sequence(LerpScaleInterval(self.logo, 2, Vec3(1, 1, 0.45), Vec3(0.9, 1, 0.4), blendType='easeInOut'), LerpScaleInterval(self.logo, 2, Vec3(0.9, 1, 0.4), Vec3(1, 1, 0.45), blendType='easeInOut'))
        self.logoScaleSequence.loop()
        tn = TextNode('timer-message')
        tn.setText(self.timerText)
        tn.setAlign(TextNode.ACenter)
        tn.setFont(ToontownGlobals.getInterfaceFont())
        self.message = self.timerParent.attachNewNode(tn)
        self.message.setScale(0.1)
        self.message.setPos(0, 0, -0.5)
        self.updateTimer()

    def updateTimer(self):
        currentTime = time.time()
        diff = self.unlockTime - currentTime
        if diff < 1:
            return True
        if self.timer:
            self.timer.removeNode()
        hours = int(diff / 60 / 60)
        minutes = int(diff / 60 % 60)
        seconds = int(diff % 60)
        if diff <= 60:
            timeText = '%d second%s' % (seconds, 's' if seconds != 1 else '')
        elif hours == 0:
            timeText = '%d minute%s and %d second%s' % (minutes,
             's' if minutes != 1 else '',
             seconds,
             's' if seconds != 1 else '')
        else:
            timeText = '%d hour%s, %d minute%s, and %d second%s' % (hours,
             's' if hours != 1 else '',
             minutes,
             's' if minutes != 1 else '',
             seconds,
             's' if seconds != 1 else '')
        tn = TextNode('time-left')
        tn.setText(timeText)
        tn.setAlign(TextNode.ACenter)
        tn.setFont(ToontownGlobals.getInterfaceFont())
        self.timer = self.timerParent.attachNewNode(tn)
        self.timer.setScale(0.15)
        self.timer.setPos(0, 0, -0.65)

    def __tick(self, task):
        done = self.updateTimer()
        if done:
            self.stop()
            return task.done
        task.setDelay(1)
        return task.again

    def stop(self):
        if self.timer:
            self.timer.removeNode()
        self.message.removeNode()
        tn = TextNode('timer-message')
        tn.setText('Toontown Infinite is now unlocked!')
        tn.setAlign(TextNode.ACenter)
        tn.setFont(ToontownGlobals.getInterfaceFont())
        self.message = self.timerParent.attachNewNode(tn)
        self.message.setScale(0.1)
        self.message.setPos(0, 0, -0.5)
        tn = TextNode('time-left')
        tn.setText('Please restart your game.')
        tn.setAlign(TextNode.ACenter)
        tn.setFont(ToontownGlobals.getInterfaceFont())
        self.timer = self.timerParent.attachNewNode(tn)
        self.timer.setScale(0.15)
        self.timer.setPos(0, 0, -0.65)
