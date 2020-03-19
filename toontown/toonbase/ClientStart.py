#!/usr/bin/env python2
import gc


# Due to the newer Panda3D versions being less stable on the C++ side of things,
# we need to disable the garbage collector during startup or a thread related
# error will cause an AttributeError.
# ~ Chan
gc.disable()


import __builtin__


__builtin__.process = 'client'


from pandac.PandaModules import *
from panda3d.core import NodePath

for dtool in ('children', 'parent', 'name'):
    del NodePath.DtoolClassDict[dtool]


if __debug__:
    loadPrcFile('config/general.prc')
    loadPrcFile('config/distribution/dev.prc')


from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui import DirectGuiGlobals


notify = directNotify.newCategory('ClientStart')
notify.setInfo(True)


from otp.settings.Settings import Settings


preferencesFilename = ConfigVariableString(
    'preferences-filename', 'preferences.json').getValue()
notify.info('Reading %s...' % preferencesFilename)
__builtin__.settings = Settings(preferencesFilename)
if 'fullscreen' not in settings:
    settings['fullscreen'] = False
if 'music' not in settings:
    settings['music'] = True
if 'sfx' not in settings:
    settings['sfx'] = True
if 'musicVol' not in settings:
    settings['musicVol'] = 1.0
if 'sfxVol' not in settings:
    settings['sfxVol'] = 1.0
if 'loadDisplay' not in settings:
    settings['loadDisplay'] = 'pandagl'
if 'toonChatSounds' not in settings:
    settings['toonChatSounds'] = True
loadPrcFileData('Settings: res', 'win-size %d %d' % tuple(settings.get('res', (800, 600))))
loadPrcFileData('Settings: fullscreen', 'fullscreen %s' % settings['fullscreen'])
loadPrcFileData('Settings: music', 'audio-music-active %s' % settings['music'])
loadPrcFileData('Settings: sfx', 'audio-sfx-active %s' % settings['sfx'])
loadPrcFileData('Settings: musicVol', 'audio-master-music-volume %s' % settings['musicVol'])
loadPrcFileData('Settings: sfxVol', 'audio-master-sfx-volume %s' % settings['sfxVol'])
loadPrcFileData('Settings: loadDisplay', 'load-display %s' % settings['loadDisplay'])
loadPrcFileData('Settings: toonChatSounds', 'toon-chat-sounds %s' % settings['toonChatSounds'])


import os


import time
import sys
import random
import __builtin__
try:
    launcher
except:
    from toontown.launcher.TTILauncher import TTILauncher
    launcher = TTILauncher()
    __builtin__.launcher = launcher


notify.info('Starting the game...')
if launcher.isDummy():
    http = HTTPClient()
else:
    http = launcher.http
from direct.gui import DirectGuiGlobals
from toontown.toonbase import ToontownGlobals
DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)
launcher.setPandaErrorCode(7)
from toontown.toonbase import ToonBase
ToonBase.ToonBase()
if base.win is None:
    notify.error('Unable to open window; aborting.')
launcher.setPandaErrorCode(0)
launcher.setPandaWindowOpen()
try:
    import __builtin__
except:
    import builtins
    __builtin__ = builtins
#from toontown.distributed.DiscordRPC import DiscordRPC
#__builtin__.Discord = DiscordRPC()
#Discord.Launching()
from panda3d.core import Vec4
base.setBackgroundColor(Vec4(0, 0, 0, 0))
base.graphicsEngine.renderFrame()
DirectGuiGlobals.setDefaultRolloverSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui.bam'))
#from toontown.toon import Toon
#Toon.preload()
#from toontown.suit import Suit
#Suit.preload()
#Removed this.
#from toontown.login import AvatarChooser
#AvatarChooser.preload()
#from toontown.shtiker import ShtikerGUI
#ShtikerGUI.preload()
from toontown.toontowngui.Introduction import Introduction
introduction = Introduction()
from toontown.toontowngui.ClickToStart import ClickToStart
version = ConfigVariableString('server-version', 'n/a')
clickToStart = ClickToStart(version=version.getValue())
clickToStart.setColorScale(0, 0, 0, 0)
music = None
if base.musicManagerIsValid:
    themeList = ('phase_3/audio/bgm/tti_theme.ogg', 'phase_3/audio/bgm/tti_theme.ogg')
    music = base.loadMusic(random.choice(themeList))
    if music:
        music.setLoop(1)
        music.setVolume(0.9)
        music.play()
    notify.info('Loading the default GUI sounds...')
    DirectGuiGlobals.setDefaultRolloverSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
    DirectGuiGlobals.setDefaultClickSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
else:
    music = None
    #if ToontownGlobals.HALLOWEEN_PROPS in base.clientHolidayIdList:
    #    music = base.loadMusic('phase_3/audio/bgm/tti_theme_halloween.ogg')
    #if ToontownGlobals.WACKY_WINTER_DECORATIONS in base.clientHolidayIdList:
    #    music = base.loadMusic('phase_3/audio/bgm/tti_theme_christmas.ogg')
    #else:
    #    music = base.loadMusic('phase_3/audio/bgm/tti_theme.ogg')
    if music is not None:
        music.setLoop(1)
        music.setVolume(0.9)
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from otp.otpgui import OTPDialog

def syncLoginFSM(task = None):
    stateName = base.cr.loginFSM.getCurrentState().getName()
    if introduction.getCurrentOrNextState() != 'Label' and introduction.label.getText() != TTLocalizer.LoaderLabel:
            introduction.request('Label', TTLocalizer.LoaderLabel)
            taskMgr.doMethodLater(1, syncLoginFSM, 'syncLoginFSM-task')
    elif stateName in ('connect', 'login', 'waitForGameList', 'waitForShardList'):
        introduction.request('Label')
    elif stateName == 'failedToConnect':
        url = base.cr.serverList[0]
        if base.cr.bootedIndex in (1400, 1403, 1405):
            message = OTPLocalizer.CRNoConnectProxyNoPort % (url.getServer(), url.getPort(), url.getPort())
            style = OTPDialog.CancelOnly
        else:
            message = OTPLocalizer.CRNoConnectTryAgain % (url.getServer(), url.getPort())
            style = OTPDialog.TwoChoice
        if style == OTPDialog.CancelOnly:
            introduction.request('ExitDialog', message, base.cr.loginFSM.request, ['shutdown'])
        else:
            introduction.request('YesNoDialog', message, base.cr.loginFSM.request, ['connect', [base.cr.serverList]], base.cr.loginFSM.request, ['shutdown'])
    elif stateName == 'noConnection':
        if base.cr.bootedIndex is not None and base.cr.bootedIndex in OTPLocalizer.CRBootedReasons:
            message = OTPLocalizer.CRBootedReasons[base.cr.bootedIndex]
        elif base.cr.bootedIndex == 155:
            message = base.cr.bootedText
        elif base.cr.bootedText is not None:
            message = OTPLocalizer.CRBootedReasonUnknownCode % base.cr.bootedIndex
        else:
            message = OTPLocalizer.CRLostConnection
        if base.cr.bootedIndex == 152:
            message %= {'name': base.cr.bootedText}
        introduction.request('ExitDialog', message, base.cr.loginFSM.request, ['shutdown'])
    elif stateName == 'missingGameRootObject':
        introduction.request('YesNoDialog', OTPLocalizer.CRMissingGameRootObject, base.cr.loginFSM.request, ['waitForGameList'], base.cr.loginFSM.request, ['shutdown'])
    elif stateName == 'noShards':
        introduction.request('YesNoDialog', OTPLocalizer.CRNoDistrictsTryAgain, base.cr.loginFSM.request, ['noShardsWait'], base.cr.loginFSM.request, ['shutdown'])
    else:
        introduction.request('ClickToStart')
    if task is not None:
        return task.done
    else:
        return



from direct.interval.IntervalGlobal import Sequence, Func, Wait
presentsTrack = Sequence(Func(introduction.request, 'Presents'), Wait(7), Func(syncLoginFSM))
disclaimerTrack = Sequence(Func(introduction.request, 'Disclaimer'), Wait(7), Func(presentsTrack.start))
from toontown.distributed import ToontownClientRepository
base.cr = ToontownClientRepository.ToontownClientRepository(version.getValue(), launcher)
base.cr.music = music
base.cr.introduction = introduction
base.cr.clickToStart = clickToStart
base.initNametagGlobals()
from otp.distributed.OtpDoGlobals import OTP_DO_ID_FRIEND_MANAGER
base.cr.generateGlobalObject(OTP_DO_ID_FRIEND_MANAGER, 'FriendManager')
if not launcher.isDummy():
    base.startShow(launcher.getGameServer())
else:
    base.startShow()
__builtin__.loader = base.loader
disclaimerTrack.start()

def skip():
    if disclaimerTrack.isPlaying():
        disclaimerTrack.finish()
    elif presentsTrack.isPlaying():
        presentsTrack.finish()


#base.accept('mouse1', skip)
#gc.enable()
#gc.collect()
try:
    if config.GetBool('want-leak-graph-client', False):
        from toontown.debug import LeakGraph
        LeakGraph.outputLeaking()
    #Discord.StartTasks()
    base.run()
except SystemExit:
    pass
except Exception:
    import traceback
    traceback.print_exc()
