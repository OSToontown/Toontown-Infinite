from toontown.toontowngui import TTDialog
from direct.gui.DirectGui import DirectButton, DirectLabel
from direct.fsm import ClassicFSM, State
from toontown.toonbase.ToontownGlobals import OptionsPageHotkey
    
class ControlRemap:

    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
    JUMP = 4
    ACTION_BUTTON = 5
    OPTIONS_PAGE_HOTKEY = 6
    CHAT_HOTKEY = 7
    
    
    def __init__(self):
        self.dialog = TTDialog.TTGlobalDialog(dialogName='ControlRemap', doneEvent = 'doneRemapping',
          style=TTDialog.TwoChoice, text='Choose the keys you wish to remap.', text_wordwrap=24,
          text_pos=(0, -0.7), suppressKeys = True, suppressMouse = True)
        scale = self.dialog.component('image0').getScale()
        scale.setX(scale[0] * 1.75)
        scale.setZ(scale[2] * 3)
        self.dialog.component('image0').setScale(scale)
        self.guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        textStartHeight = 0.65
        leftMargin = -0.7
        buttonbase_xcoord = -0.6
        buttonbase_ycoord = 0.6
        button_image_scale = (0.7, 1, 1)
        button_textpos = (0, -0.02)
        options_text_scale = 0.052
        self.upKey = DirectButton(
            parent=self.dialog,
            relief=None,
            image=(
                self.guiButton.find('**/QuitBtn_UP'),
                self.guiButton.find('**/QuitBtn_DN'),
                self.guiButton.find('**/QuitBtn_RLVR')),
            image_scale=button_image_scale,
            text=base.MOVE_UP,
            text_scale=options_text_scale,
            text_pos=button_textpos,
            pos=(
                buttonbase_xcoord,
                0.0,
                buttonbase_ycoord),
            command=self.enterWaitForKey, extraArgs=[self.UP])
        self.upLabel = DirectLabel(
            parent=self.dialog,
            relief=None,
            text='Move Up:',
            text_align=TextNode.ALeft,
            text_scale=options_text_scale,
            text_wordwrap=16,
            pos=(
                leftMargin,
                0,
                textStartHeight))
        self.leftKey = DirectButton(
            parent=self.dialog,
            relief=None,
            image=(
                self.guiButton.find('**/QuitBtn_UP'),
                self.guiButton.find('**/QuitBtn_DN'),
                self.guiButton.find('**/QuitBtn_RLVR')),
            image_scale=button_image_scale,
            text=base.MOVE_LEFT,
            text_scale=options_text_scale,
            text_pos=button_textpos,
            pos=(
                buttonbase_xcoord + 0.4,
                0.0,
                buttonbase_ycoord),
            command=self.enterWaitForKey, extraArgs=[self.LEFT])
        self.leftLabel = DirectLabel(
            parent=self.dialog,
            relief=None,
            text='Move Left:',
            text_align=TextNode.ALeft,
            text_scale=options_text_scale,
            text_wordwrap=16,
            pos=(
                leftMargin + 0.4,
                0,
                textStartHeight))
                
        self.downKey = DirectButton(
            parent=self.dialog,
            relief=None,
            image=(
                self.guiButton.find('**/QuitBtn_UP'),
                self.guiButton.find('**/QuitBtn_DN'),
                self.guiButton.find('**/QuitBtn_RLVR')),
            image_scale=button_image_scale,
            text=base.MOVE_DOWN,
            text_scale=options_text_scale,
            text_pos=button_textpos,
            pos=(
                buttonbase_xcoord + 0.8,
                0.0,
                buttonbase_ycoord),
            command=self.enterWaitForKey, extraArgs=[self.DOWN])
        self.downLabel = DirectLabel(
            parent=self.dialog,
            relief=None,
            text='Move Down:',
            text_align=TextNode.ALeft,
            text_scale=options_text_scale,
            text_wordwrap=16,
            pos=(
                leftMargin + 0.8,
                0,
                textStartHeight))

        self.rightKey = DirectButton(
            parent=self.dialog,
            relief=None,
            image=(
                self.guiButton.find('**/QuitBtn_UP'),
                self.guiButton.find('**/QuitBtn_DN'),
                self.guiButton.find('**/QuitBtn_RLVR')),
            image_scale=button_image_scale,
            text=base.MOVE_RIGHT,
            text_scale=options_text_scale,
            text_pos=button_textpos,
            pos=(
                buttonbase_xcoord + 1.2,
                0.0,
                buttonbase_ycoord),
            command=self.enterWaitForKey, extraArgs=[self.RIGHT])
        self.rightLabel = DirectLabel(
            parent=self.dialog,
            relief=None,
            text='Move Right:',
            text_align=TextNode.ALeft,
            text_scale=options_text_scale,
            text_wordwrap=16,
            pos=(
                leftMargin + 1.2,
                0,
                textStartHeight))                  
            
        self.jumpKey = DirectButton(
            parent=self.dialog,
            relief=None,
            image=(
                self.guiButton.find('**/QuitBtn_UP'),
                self.guiButton.find('**/QuitBtn_DN'),
                self.guiButton.find('**/QuitBtn_RLVR')),
            image_scale=button_image_scale,
            text=base.JUMP,
            text_scale=options_text_scale,
            text_pos=button_textpos,
            pos=(
                buttonbase_xcoord,
                0.0,
                buttonbase_ycoord - 0.3),
            command=self.enterWaitForKey, extraArgs=[self.JUMP])
        self.jumpLabel = DirectLabel(
            parent=self.dialog,
            relief=None,
            text='Jump:',
            text_align=TextNode.ALeft,
            text_scale=options_text_scale,
            text_wordwrap=16,
            pos=(
                leftMargin,
                0,
                textStartHeight - 0.3))
                
        self.actionKey = DirectButton(
            parent=self.dialog,
            relief=None,
            image=(
                self.guiButton.find('**/QuitBtn_UP'),
                self.guiButton.find('**/QuitBtn_DN'),
                self.guiButton.find('**/QuitBtn_RLVR')),
            image_scale=button_image_scale,
            text=base.ACTION_BUTTON,
            text_scale=options_text_scale,
            text_pos=button_textpos,
            pos=(
                buttonbase_xcoord + 0.4,
                0.0,
                buttonbase_ycoord - 0.3),
            command=self.enterWaitForKey, extraArgs=[self.ACTION_BUTTON])
        self.actionLabel = DirectLabel(
            parent=self.dialog,
            relief=None,
            text='Action Button:',
            text_align=TextNode.ALeft,
            text_scale=options_text_scale,
            text_wordwrap=16,
            pos=(
                leftMargin + 0.35,
                0,
                textStartHeight - 0.3))                
                
        self.optionsKey = DirectButton(
            parent=self.dialog,
            relief=None,
            image=(
                self.guiButton.find('**/QuitBtn_UP'),
                self.guiButton.find('**/QuitBtn_DN'),
                self.guiButton.find('**/QuitBtn_RLVR')),
            image_scale=button_image_scale,
            text=OptionsPageHotkey,
            text_scale=options_text_scale,
            text_pos=button_textpos,
            pos=(
                buttonbase_xcoord + 0.8,
                0.0,
                buttonbase_ycoord - 0.3),
            command=self.enterWaitForKey, extraArgs=[self.OPTIONS_PAGE_HOTKEY])
        self.optionsLabel = DirectLabel(
            parent=self.dialog,
            relief=None,
            text='Options Page Hotkey:',
            text_align=TextNode.ALeft,
            text_scale=options_text_scale * 0.9,
            text_wordwrap=16,
            pos=(
                leftMargin + 0.7,
                0,
                textStartHeight - 0.3))
        self.chatHotkey = DirectButton(
            parent=self.dialog,
            relief=None,
            image=(
                self.guiButton.find('**/QuitBtn_UP'),
                self.guiButton.find('**/QuitBtn_DN'),
                self.guiButton.find('**/QuitBtn_RLVR')),
            image_scale=button_image_scale,
            text=base.CHAT_HOTKEY,
            text_scale=options_text_scale,
            text_pos=button_textpos,
            pos=(
                buttonbase_xcoord + 1.25,
                0.0,
                buttonbase_ycoord - 0.3),
            command=self.enterWaitForKey, extraArgs=[self.CHAT_HOTKEY])
        self.chatHotkeyLabel = DirectLabel(
            parent=self.dialog,
            relief=None,
            text='Chatbox Hotkey:',
            text_align=TextNode.ALeft,
            text_scale=options_text_scale,
            text_wordwrap=16,
            pos=(
                leftMargin + 1.25,
                0,
                textStartHeight - 0.3))                 
                
        self.controlsToBeSaved = {
            self.UP: base.MOVE_UP,
            self.LEFT: base.MOVE_LEFT,
            self.DOWN: base.MOVE_DOWN,
            self.RIGHT: base.MOVE_RIGHT,
            self.JUMP: base.JUMP,
            self.ACTION_BUTTON: base.ACTION_BUTTON,
            self.OPTIONS_PAGE_HOTKEY: OptionsPageHotkey,
            self.CHAT_HOTKEY: base.CHAT_HOTKEY}
        
        self.popupDialog = None
        self.dialog.show()    

        self.fsm = ClassicFSM.ClassicFSM(
            'ControlRemapDialog',
            [
                State.State('off', self.enterShow, self.exitShow, ['waitForKey']),
                State.State('waitForKey', self.enterWaitForKey, self.exitWaitForKey, ['off']),               
            ], 'off', 'off')
        self.fsm.enterInitialState()
        self.dialog.accept('doneRemapping', self.exit)
        messenger.send('disable-hotkeys')
        base.localAvatar.chatMgr.disableBackgroundFocus()
        
    def enterShow(self):
        pass
        
    def exitShow(self):
        pass
        
    def enterWaitForKey(self, controlNum):
        base.transitions.fadeScreen(0.9)
        self.dialog.hide()
        if self.popupDialog:
            self.popupDialog.cleanup()
        self.popupDialog = TTDialog.TTDialog(style=TTDialog.NoButtons,
          text='Press the button you wish to remap this control to.', suppressMouse=True, suppressKeys=True)
        self.popupDialog.show()
        base.buttonThrowers[0].node().setButtonDownEvent('buttonPress-'+str(controlNum))
        self.dialog.accept('buttonPress-'+str(controlNum), self.registerKey, [controlNum])
        
    def registerKey(self, controlNum, keyName):
        self.popupDialog.cleanup()
        self.controlsToBeSaved[controlNum] = keyName
        if controlNum is self.UP:
            self.upKey['text'] = keyName
        elif controlNum is self.LEFT:
            self.leftKey['text'] = keyName
        elif controlNum is self.DOWN:
            self.downKey['text'] = keyName
        elif controlNum is self.RIGHT:
            self.rightKey['text'] = keyName
        elif controlNum is self.JUMP:
            self.jumpKey['text'] = keyName
        elif controlNum is self.ACTION_BUTTON:
            self.actionKey['text'] = keyName
        elif controlNum is self.OPTIONS_PAGE_HOTKEY:
            self.optionsKey['text'] = keyName
        elif controlNum is self.CHAT_HOTKEY:
            self.chatHotkey['text'] = keyName
        self.dialog.show()    
        self.exitWaitForKey(controlNum, keyName)
        
    def exitWaitForKey(self, controlNum, keyName):
        self.dialog.ignore('buttonPress-'+str(controlNum))
        
    def exit(self):
        if self.dialog.doneStatus == 'ok':
            self.enterSave()
        else:
            self.enterCancel()
        
    def enterSave(self):
        keymap = settings.get('keymap', {})
        keymap['MOVE_UP'] = self.controlsToBeSaved[self.UP]
        keymap['MOVE_LEFT'] = self.controlsToBeSaved[self.LEFT]
        keymap['MOVE_DOWN'] = self.controlsToBeSaved[self.DOWN]        
        keymap['MOVE_RIGHT'] = self.controlsToBeSaved[self.RIGHT]
        keymap['JUMP'] = self.controlsToBeSaved[self.JUMP]
        keymap['ACTION_BUTTON'] = self.controlsToBeSaved[self.ACTION_BUTTON]
        keymap['OPTIONS_PAGE_HOTKEY'] = self.controlsToBeSaved[self.OPTIONS_PAGE_HOTKEY]
        keymap['CHAT_HOTKEY'] = self.controlsToBeSaved[self.CHAT_HOTKEY]
        settings['keymap'] = keymap
        base.reloadControls()
        base.localAvatar.controlManager.reload()
        base.localAvatar.chatMgr.reloadWASD()
        self.unload()
        pass
        
    def exitSave(self):
        pass
        
    def enterCancel(self):
        self.unload()
        
    def exitCancel(self):
        pass
        
    def unload(self):
        self.upKey.destroy()
        del self.upKey
        self.upLabel.destroy()
        del self.upLabel
        self.leftKey.destroy()
        del self.leftKey
        self.leftLabel.destroy()
        del self.leftLabel
        self.downKey.destroy()
        del self.downKey
        self.downLabel.destroy()
        del self.downLabel
        self.rightKey.destroy()
        del self.rightKey
        self.rightLabel.destroy()
        del self.rightLabel
        self.jumpKey.destroy()
        del self.jumpKey
        self.jumpLabel.destroy()
        del self.jumpLabel
        self.actionKey.destroy()
        del self.actionKey
        self.actionLabel.destroy()
        del self.actionLabel
        self.optionsKey.destroy()
        del self.optionsKey
        self.optionsLabel.destroy()
        del self.optionsLabel
        self.chatHotkey.destroy()
        del self.chatHotkey
        self.chatHotkeyLabel.destroy()
        del self.chatHotkeyLabel
        if self.popupDialog:
            self.popupDialog.cleanup()
        del self.popupDialog
        self.dialog.cleanup()
        del self.dialog
        messenger.send('enable-hotkeys')