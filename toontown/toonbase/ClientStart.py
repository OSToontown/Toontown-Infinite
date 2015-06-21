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


if __debug__:
    loadPrcFile('config/general.prc')
    loadPrcFile('config/distribution/dev.prc')


from direct.directnotify.DirectNotifyGlobal import directNotify


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
loadPrcFileData('Settings: fullscreen', 'fullscreen %s' % settings['fullscreen'])
loadPrcFileData('Settings: music', 'audio-music-active %s' % settings['music'])
loadPrcFileData('Settings: sfx', 'audio-sfx-active %s' % settings['sfx'])
loadPrcFileData('Settings: musicVol', 'audio-master-music-volume %s' % settings['musicVol'])
loadPrcFileData('Settings: sfxVol', 'audio-master-sfx-volume %s' % settings['sfxVol'])
loadPrcFileData('Settings: loadDisplay', 'load-display %s' % settings['loadDisplay'])
loadPrcFileData('Settings: toonChatSounds', 'toon-chat-sounds %s' % settings['toonChatSounds'])  

import os

from toontown.toonbase.ContentPacksManager import ContentPackError
from toontown.toonbase.ContentPacksManager import ContentPacksManager


contentPacksFilepath = ConfigVariableString(
    'content-packs-filepath', 'contentpacks/').getValue()
contentPacksSortFilename = ConfigVariableString(
    'content-packs-sort-filename', 'sort.yaml').getValue()
if not os.path.exists(contentPacksFilepath):
    os.makedirs(contentPacksFilepath)
__builtin__.ContentPackError = ContentPackError
__builtin__.contentPacksMgr = ContentPacksManager(
    filepath=contentPacksFilepath, sortFilename=contentPacksSortFilename)
contentPacksMgr.applyAll()


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
tempLoader = Loader()
backgroundNode = tempLoader.loadSync(Filename('phase_3/models/gui/loading-background'))
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
notify.info('Setting the default font...')
import ToontownGlobals
DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)
launcher.setPandaErrorCode(7)
import ToonBase
ToonBase.ToonBase()
from pandac.PandaModules import *
if base.win is None:
    notify.error('Unable to open window; aborting.')
launcher.setPandaErrorCode(0)
launcher.setPandaWindowOpen()
ConfigVariableDouble('decompressor-step-time').setValue(0.01)
ConfigVariableDouble('extractor-step-time').setValue(0.01)
backgroundNodePath = aspect2d.attachNewNode(backgroundNode, 0)
backgroundNodePath.setPos(0.0, 0.0, 0.0)
backgroundNodePath.setScale(render2d, VBase3(1))
backgroundNodePath.find('**/fg').hide()
logo = OnscreenImage(
    image='phase_3/maps/toontown-logo.png',
    scale=(0.9625 / (4.0/3.0), 1, 0.83 / (4.0/3.0)),
    pos=backgroundNodePath.find('**/fg').getPos())
logo.setTransparency(TransparencyAttrib.MAlpha)
logo.setBin('fixed', 20)
logo.reparentTo(backgroundNodePath)
backgroundNodePath.find('**/bg').setBin('fixed', 10)
base.graphicsEngine.renderFrame()
DirectGuiGlobals.setDefaultRolloverSound(base.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(base.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))
import TTLocalizer
from otp.otpbase import OTPGlobals
OTPGlobals.setDefaultProductPrefix(TTLocalizer.ProductPrefix)
if base.musicManagerIsValid:
    music = base.loadMusic('phase_3/audio/bgm/tti_theme.ogg')
    if music:
        music.setLoop(1)
        music.setVolume(0.9)
        music.play()
    notify.info('Loading the default GUI sounds...')
    DirectGuiGlobals.setDefaultRolloverSound(base.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
    DirectGuiGlobals.setDefaultClickSound(base.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
else:
    music = None
import ToontownLoader
from direct.gui.DirectGui import *
serverVersion = base.config.GetString('server-version', 'no_version_set')
version = OnscreenText(serverVersion, pos=(-1.3, -0.975), scale=0.06, fg=Vec4(0, 0, 0, 1), align=TextNode.ALeft)
version.setPos(0.03,0.03)
version.reparentTo(base.a2dBottomLeft)
from toontown.suit import Suit
Suit.loadModels()
loader.beginBulkLoad('init', TTLocalizer.LoaderLabel, 138, 0, TTLocalizer.TIP_NONE, 0)
from ToonBaseGlobal import *
from direct.showbase.MessengerGlobal import *
from toontown.distributed import ToontownClientRepository
cr = ToontownClientRepository.ToontownClientRepository(serverVersion, launcher)
cr.music = music
del music
base.initNametagGlobals()
base.cr = cr
loader.endBulkLoad('init')
from otp.friends import FriendManager
from otp.distributed.OtpDoGlobals import *
cr.generateGlobalObject(OTP_DO_ID_FRIEND_MANAGER, 'FriendManager')
if not launcher.isDummy():
    base.startShow(cr, launcher.getGameServer())
else:
    base.startShow(cr)
backgroundNodePath.reparentTo(hidden)
backgroundNodePath.removeNode()
del backgroundNodePath
del backgroundNode
del tempLoader
version.cleanup()
del version
base.loader = base.loader
__builtin__.loader = base.loader
autoRun = ConfigVariableBool('toontown-auto-run', 1)

# Now that everything is loaded we can enable the garbage collector again.
gc.enable()
gc.collect()

if autoRun:
    try:
        base.run()
    except SystemExit:
        raise
    except:
        from direct.showbase import PythonUtil
        print PythonUtil.describeException()
        raise
