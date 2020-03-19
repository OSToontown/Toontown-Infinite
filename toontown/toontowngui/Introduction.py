from direct.gui.DirectGui import OnscreenImage, OnscreenText, DirectButton
from panda3d.core import TransparencyAttrib, Vec4, TextNode
from direct.interval.IntervalGlobal import Wait
from direct.interval.IntervalGlobal import Sequence, LerpColorScaleInterval
from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM
from toontown.toontowngui.ToontownUnlockTimer import ToontownUnlockTimer
from toontown.toonbase import TTLocalizer, ToontownGlobals

class Introduction(DirectObject, FSM):
    notify = directNotify.newCategory('Introduction')

    def __init__(self):
        DirectObject.__init__(self)
        FSM.__init__(self, self.__class__.__name__)
        font = ToontownGlobals.getMinnieFont()
        self.label = OnscreenText('', parent=hidden, font=font, fg=Vec4(1, 1, 1, 1), scale=0.06, align=TextNode.ACenter, wordwrap=35)
        self.label.setColorScale(Vec4(0, 0, 0, 0))
        gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui.bam')
        shuffleUp = gui.find('**/tt_t_gui_mat_shuffleUp')
        shuffleDown = gui.find('**/tt_t_gui_mat_shuffleDown')
        okUp = gui.find('**/tt_t_gui_mat_okUp')
        okDown = gui.find('**/tt_t_gui_mat_okDown')
        closeUp = gui.find('**/tt_t_gui_mat_closeUp')
        closeDown = gui.find('**/tt_t_gui_mat_closeDown')
        gui.removeNode()
        del gui
        self.exitButton = DirectButton(parent=hidden, relief=None, image=(shuffleUp, shuffleDown, shuffleUp), image_scale=(0.6, 0.6, 0.6), image1_scale=(0.63, 0.6, 0.6), image2_scale=(0.63, 0.6, 0.6), text=(TTLocalizer.IntroExitButton,
         TTLocalizer.IntroExitButton,
         TTLocalizer.IntroExitButton,
         ''), text_font=ToontownGlobals.getInterfaceFont(), text_scale=TTLocalizer.SBshuffleBtn, text_pos=(0, -0.02), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.yesButton = DirectButton(parent=hidden, relief=None, image=(okUp,
         okDown,
         okUp,
         okDown), image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7), image2_scale=(0.7, 0.7, 0.7), text=('', TTLocalizer.IntroYesButton, TTLocalizer.IntroYesButton), text_font=ToontownGlobals.getInterfaceFont(), text_scale=0.08, text_align=TextNode.ACenter, text_pos=(0, -0.175), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.noButton = DirectButton(parent=hidden, relief=None, image=(closeUp,
         closeDown,
         closeUp,
         closeDown), image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7), image2_scale=(0.7, 0.7, 0.7), text=('', TTLocalizer.IntroNoButton, TTLocalizer.IntroNoButton), text_font=ToontownGlobals.getInterfaceFont(), text_scale=0.08, text_align=TextNode.ACenter, text_pos=(0, -0.175), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.disclaimerTrack = None
        self.presentsTrack = None
        self.lock = None
        self.accept('lock-client', self.lockClient)
        return

    def lockClient(self, unlockTime, message):
        self.lock = ToontownUnlockTimer(unlockTime, message)

    def delete(self):
        if self.presentsTrack is not None:
            self.presentsTrack.finish()
            self.presentsTrack = None
        if self.disclaimerTrack is not None:
            self.disclaimerTrack.finish()
            self.disclaimerTrack = None
        if self.noButton is not None:
            self.noButton.destroy()
            self.noButton = None
        if self.yesButton is not None:
            self.yesButton.destroy()
            self.yesButton = None
        if self.exitButton is not None:
            self.exitButton.destroy()
            self.exitButton = None
        if self.label is not None:
            self.label.destroy()
            self.label = None
        return

    def calcLabelY(self):
        sy = self.label.getScale()[1]
        height = self.label.textNode.getHeight()
        return height * sy / 2.0

    def enterOff(self):
        pass

    def enterDisclaimer(self):
        self.label.setText(TTLocalizer.IntroDisclaimer)
        self.label.setPos(0, self.calcLabelY())
        self.label.reparentTo(aspect2d)
        if self.disclaimerTrack is not None:
            self.disclaimerTrack.finish()
            self.disclaimerTrack = None
        self.disclaimerTrack = Sequence(LerpColorScaleInterval(self.label, 2, Vec4(1, 1, 1, 1), Vec4(0, 0, 0, 0), blendType='easeIn'), Wait(3), LerpColorScaleInterval(self.label, 2, Vec4(0, 0, 0, 0), Vec4(1, 1, 1, 1), blendType='easeOut'))
        self.disclaimerTrack.start()
        return

    def exitDisclaimer(self):
        if self.disclaimerTrack is not None:
            self.disclaimerTrack.finish()
            self.disclaimerTrack = None
        self.label.reparentTo(hidden)
        self.label.setPos(0, 0)
        self.label.setText('')
        return

    def enterPresents(self):
        self.label.setText(TTLocalizer.IntroPresents)
        self.label.setPos(0, self.calcLabelY())
        self.label.reparentTo(aspect2d)
        if self.presentsTrack is not None:
            self.presentsTrack.finish()
            self.presentsTrack = None
        self.presentsTrack = Sequence(LerpColorScaleInterval(self.label, 2, Vec4(1, 1, 1, 1), Vec4(0, 0, 0, 0), blendType='easeIn'), Wait(3), LerpColorScaleInterval(self.label, 2, Vec4(0, 0, 0, 0), Vec4(1, 1, 1, 1), blendType='easeOut'))
        self.presentsTrack.start()
        return

    def exitPresents(self):
        if self.presentsTrack is not None:
            self.presentsTrack.finish()
            self.presentsTrack = None
        self.label.reparentTo(hidden)
        self.label.setPos(0, 0)
        self.label.setText('')
        return

    def enterLabel(self, text):
        self.label.setText(text)
        self.label.setPos(0, self.calcLabelY())
        self.label.reparentTo(aspect2d)
        self.label.setColorScale(Vec4(1, 1, 1, 1))

    def exitLabel(self):
        self.label.setColorScale(Vec4(0, 0, 0, 0))
        self.label.reparentTo(hidden)
        self.label.setPos(0, 0)
        self.label.setText('')

    def enterExitDialog(self, text, exitButtonCommand = None, exitButtonExtraArgs = []):
        self.label.setText(text)
        sy = self.label.getScale()[1]
        bottom = self.label.textNode.getBottom() * sy
        lineHeight = self.label.textNode.getLineHeight() * sy
        self.exitButton.setPos(0, 0, bottom - lineHeight * 2)
        self.exitButton['command'] = exitButtonCommand
        self.exitButton['extraArgs'] = exitButtonExtraArgs
        labelY = self.calcLabelY()
        self.label.setPos(0, labelY)
        self.exitButton.setZ(self.exitButton, labelY)
        self.exitButton.reparentTo(aspect2d)
        self.label.reparentTo(aspect2d)
        self.label.setColorScale(Vec4(1, 1, 1, 1))

    def exitExitDialog(self):
        self.label.setColorScale(Vec4(0, 0, 0, 0))
        self.label.reparentTo(hidden)
        self.exitButton.reparentTo(hidden)
        self.label.setPos(0, 0)
        self.label.setText('')
        self.exitButton['command'] = None
        self.exitButton['extraArgs'] = []
        self.exitButton.setPos(0, 0, 0)
        return

    def enterYesNoDialog(self, text, yesButtonCommand = None, yesButtonExtraArgs = [], noButtonCommand = None, noButtonExtraArgs = []):
        self.label.setText(text)
        sy = self.label.getScale()[1]
        bottom = self.label.textNode.getBottom() * sy
        lineHeight = self.label.textNode.getLineHeight() * sy
        self.yesButton.setPos(-0.1, 0, bottom - lineHeight * 2)
        self.yesButton['command'] = yesButtonCommand
        self.yesButton['extraArgs'] = yesButtonExtraArgs
        self.noButton.setPos(0.1, 0, bottom - lineHeight * 2)
        self.noButton['command'] = noButtonCommand
        self.noButton['extraArgs'] = noButtonExtraArgs
        labelY = self.calcLabelY()
        self.label.setPos(0, labelY)
        self.yesButton.setZ(self.yesButton, labelY)
        self.noButton.setZ(self.noButton, labelY)
        self.yesButton.reparentTo(aspect2d)
        self.noButton.reparentTo(aspect2d)
        self.label.reparentTo(aspect2d)
        self.label.setColorScale(Vec4(1, 1, 1, 1))

    def exitYesNoDialog(self):
        self.label.setColorScale(Vec4(0, 0, 0, 0))
        self.label.reparentTo(hidden)
        self.noButton.reparentTo(hidden)
        self.yesButton.reparentTo(hidden)
        self.label.setPos(0, 0)
        self.label.setText('')
        self.noButton['command'] = None
        self.noButton['extraArgs'] = []
        self.noButton.setPos(0, 0, 0)
        self.yesButton['command'] = None
        self.yesButton['extraArgs'] = []
        self.yesButton.setPos(0, 0, 0)
        return

    def enterClickToStart(self):
        if self.lock:
            self.lock.start()
            return
        base.cr.clickToStart.start()

    def exitClickToStart(self):
        base.cr.clickToStart.stop()
