from direct.controls import ControlManager
from direct.showbase.InputStateGlobal import inputState

# This is the new class for Toontown's ControlManager


class ToontownControlManager(ControlManager.ControlManager):
    # Instead of checking config.prc, get wantWASD from ToonBase
    wantWASD = base.wantWASD

    def __init__(self, enable=True, passMessagesThrough=False):
        self.passMessagesThrough = passMessagesThrough
        self.inputStateTokens = []
        self.WASDTurnTokens = []
        self.controls = {}
        self.currentControls = None
        self.currentControlsName = None
        self.isEnabled = 0
        self.forceAvJumpToken = None
        self.inputToDisable = []
        self.forceTokens = None
        self.istWASD = []
        self.istNormal = []
        if enable:
            self.enable()

    def enable(self):
        if self.isEnabled:
            return

        self.isEnabled = 1

        # Keep track of what we do on the inputState so we can undo it later on
        ist = self.inputStateTokens
        ist.extend((
            inputState.watch('run', 'runningEvent', 'running-on', 'running-off'),
            inputState.watch('forward', 'force-forward', 'force-forward-stop'),
        ))

        if self.wantWASD:
            self.istWASD.extend((
                inputState.watch('turnLeft', 'mouse-look_left', 'mouse-look_left-done'),
                inputState.watch('turnLeft', 'force-turnLeft', 'force-turnLeft-stop'),
                inputState.watch('turnRight', 'mouse-look_right', 'mouse-look_right-done'),
                inputState.watch('turnRight', 'force-turnRight', 'force-turnRight-stop'),
                inputState.watchWithModifiers('forward', 'w', inputSource=inputState.WASD),
                inputState.watchWithModifiers('reverse', 's', inputSource=inputState.WASD),
                inputState.watchWithModifiers('jump', 'shift')
            ))

            self.setWASDTurn(True)

        else:
            self.istNormal.extend((
                inputState.watchWithModifiers('forward', 'arrow_up', inputSource=inputState.ArrowKeys),
                inputState.watchWithModifiers('reverse', 'arrow_down', inputSource=inputState.ArrowKeys),
                inputState.watchWithModifiers('turnLeft', 'arrow_left', inputSource=inputState.ArrowKeys),
                inputState.watchWithModifiers('turnRight', 'arrow_right', inputSource=inputState.ArrowKeys),
                inputState.watch('jump', 'control', 'control-up')
            ))
            
            self.istNormal.extend((
                inputState.watch('turnLeft', 'mouse-look_left', 'mouse-look_left-done'),
                inputState.watch('turnLeft', 'force-turnLeft', 'force-turnLeft-stop'),
                inputState.watch('turnRight', 'mouse-look_right', 'mouse-look_right-done'),
                inputState.watch('turnRight', 'force-turnRight', 'force-turnRight-stop')
            ))
            

        if self.currentControls:
            self.currentControls.enableAvatarControls()

    def disable(self):
        self.isEnabled = 0

        for token in self.istNormal:
            token.release()
        self.istNormal = []

        for token in self.inputStateTokens:
            token.release()
        self.inputStateTokens = []

        for token in self.istWASD:
            token.release()
        self.istWASD = []

        if self.currentControls:
            self.currentControls.disableAvatarControls()

        if self.passMessagesThrough:
            if self.wantWASD:
                print ':(ToontownControlManager) WASD support was enabled.'
                self.istWASD.append(inputState.watchWithModifiers('forward', 'w',
                                                                  inputSource=inputState.WASD))
                self.istWASD.append(inputState.watchWithModifiers('reverse', 's',
                                                                  inputSource=inputState.WASD))
                self.istWASD.append(inputState.watchWithModifiers('turnLeft', 'a',
                                                                  inputSource=inputState.WASD))
                self.istWASD.append(inputState.watchWithModifiers('turnRight', 'd',
                                                                  inputSource=inputState.WASD))
            else:
                print ':(ToontownControlManager) WASD support was disabled.'
                self.istNormal.append(
                    inputState.watchWithModifiers(
                        'forward',
                        'arrow_up',
                        inputSource=inputState.ArrowKeys))
                self.istNormal.append(
                    inputState.watchWithModifiers(
                        'reverse',
                        'arrow_down',
                        inputSource=inputState.ArrowKeys))
                self.istNormal.append(
                    inputState.watchWithModifiers(
                        'turnLeft',
                        'arrow_left',
                        inputSource=inputState.ArrowKeys))
                self.istNormal.append(
                    inputState.watchWithModifiers(
                        'turnRight',
                        'arrow_right',
                        inputSource=inputState.ArrowKeys))

    def disableWASD(self):
        # Disables WASD for when chat is open.
        # Forces all keys to return 0. This won't affect chat input.
        if self.wantWASD:
            self.forceTokens = [
                inputState.force('jump', 0, 'ToontownControlManager.disableWASD'),
                inputState.force('forward', 0, 'ToontownControlManager.disableWASD'),
                inputState.force('turnLeft', 0, 'ToontownControlManager.disableWASD'),
                inputState.force('slideLeft', 0, 'ToontownControlManager.disableWASD'),
                inputState.force('reverse', 0, 'ToontownControlManager.disableWASD'),
                inputState.force('turnRight', 0, 'ToontownControlManager.disableWASD'),
                inputState.force('slideRight', 0, 'ToontownControlManager.disableWASD')
            ]
            print 'disableWASD()'

    def enableWASD(self):
        # Enables WASD after chat is closed.
        # Releases all the forced keys we added earlier.
        if self.wantWASD:
            if self.forceTokens:
                for token in self.forceTokens:
                    token.release()
                self.forceTokens = []
                print 'enableWASD'

    def reload(self):
        # Called to reload the ControlManager ingame
        # Reload wantWASD
        self.wantWASD = base.wantWASD
        self.disable()
        self.enable()
