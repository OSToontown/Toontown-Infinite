from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase.ToontownGlobals import *
from toontown.toonbase import TTLocalizer
from toontown.parties import PartyGlobals
import Fireworks
import FireworkShows
from FireworkGlobals import skyTransitionDuration, preShowPauseDuration
from toontown.effects.FireworkShow import FireworkShow

FIREWORK_SHOW_LOCATION = {
    ToontownCentral: (150, 0, 80, 90, 0, 0),
    DonaldsDock: (150, 0, 50, 90, 0, 0),
    MinniesMelodyland: (150, -25, 40, 90, 0, 0),
    TheBrrrgh: (-200, -60, 50, 270, 0, 0),
    DaisyGardens: (-80, -50, 60, 0, 0, 0),
    OutdoorZone: (-450, -80, 140, 300, 0, 0),
    GoofySpeedway: (60, -350, 80, 20, 0, 0),
    DonaldsDreamland: (-160, 0, 80, 270, 0, 0),
    PartyHood: (0, -400, 120, 0, 0, 0)
}

PRESHOW_DICT = {
    JULY4_FIREWORKS: [
        TTLocalizer.FireworksInstructions,
        TTLocalizer.FireworksJuly4Beginning,
        TTLocalizer.FireworksJuly4Ending,
        ['tt_summer', 'firework_music']
    ],
    NEWYEARS_FIREWORKS: [
        TTLocalizer.FireworksInstructions,
        TTLocalizer.FireworksNewYearsEveBeginning,
        TTLocalizer.FireworksNewYearsEveEnding,
        ['new_years_fireworks_music', 'tt_s_ara_gen_fireworks_auldLangSyne']
    ],
    PartyGlobals.FireworkShows.Summer: [
        TTLocalizer.FireworksActivityInstructions,
        TTLocalizer.FireworksActivityBeginning,
        TTLocalizer.FireworksActivityEnding,
        ['tt_party1', 'tt_party2']
    ],
    COMBO_FIREWORKS: [
        TTLocalizer.FireworksInstructions,
        TTLocalizer.FireworksComboBeginning,
        TTLocalizer.FireworksComboEnding,
        ['new_years_fireworks_music', 'tt_s_ara_gen_fireworks_auldLangSyne']
    ]
}

POSTSHOW_DICT = {
    JULY4_FIREWORKS: TTLocalizer.FireworksJuly4Ending,
    NEWYEARS_FIREWORKS: TTLocalizer.FireworksNewYearsEveEnding,
    PartyGlobals.FireworkShows.Summer: TTLocalizer.FireworksActivityEnding,
    COMBO_FIREWORKS: TTLocalizer.FireworksComboEnding
}


class FireworkShowMixin:
    notify = DirectNotifyGlobal.directNotify.newCategory('FireworkShowMixin')

    def __init__(self, restorePlaygroundMusic = True, startDelay = 0.0):
        self.currentShow = None
        self.restorePlaygroundMusic = restorePlaygroundMusic
        self.startDelay = startDelay
        self.timestamp = None
        self.fireworkShow = None
        self.eventId = JULY4_FIREWORKS
        self.accept('MusicEnabled', self.startMusic)
        return

    def disable(self):
        if self.currentShow:
            self.currentShow.pause()
            self.currentShow = None
            if base.config.GetBool('want-old-fireworks', False):
                ivalMgr.finishIntervalsMatching('shootFirework*')
            else:
                self.destroyFireworkShow()
        hood = self.getHood()
        if hood is not None:
            if hood.id == DonaldsDock:
                hood.whiteFogColor = Vec4(0.8, 0.8, 0.8, 1)
        self.restoreCameraLens()
        if hood is not None:
            if hasattr(hood, 'loader'):
                self.getGeom().clearColorScale()
            if hasattr(hood, 'sky'):
                self.getSky().show()
                self.getSky().clearColorScale()
        if hasattr(base, 'localAvatar') and base.localAvatar:
            base.localAvatar.clearColorScale()
        base.setBackgroundColor(DefaultBackgroundColor)
        self.ignoreAll()

    def startMusic(self):
        if self.timestamp:
            self.getLoader().music.stop()
            t = globalClockDelta.localElapsedTime(self.timestamp) - self.startDelay
            base.playMusic(self.showMusic, 0, 1, 1, max(0, t))

    def shootFirework(self, x, y, z, style, color1, color2):
        amp = 5
        Fireworks.shootFirework(style, x, y, z, color1, color2, amp)

    def startShow(self, eventId, style, songId, timestamp, root = render):
        t = globalClockDelta.localElapsedTime(timestamp) - self.startDelay
        self.timestamp = timestamp
        self.showMusic = None
        self.eventId = eventId
        if base.config.GetBool('want-old-fireworks', 0):
            self.currentShow = self.getFireworkShowIval(eventId, style, songId, t)
            if self.currentShow:
                self.currentShow.start(t)
            return

        self.createFireworkShow()
        if t > self.fireworkShow.getShowDuration():
            return
        preShow = self.preShow(eventId, songId, t)
        postShow = self.postShow(eventId)
        beginFireworkShow = Func(self.beginFireworkShow, max(0, t), root)
        self.currentShow = Sequence(
            preShow, beginFireworkShow, Wait(max(0, self.fireworkShow.getShowDuration() - max(0, t))), postShow
        )
        self.currentShow.start()
        return

    def preShow(self, eventId, songId, startT):
        if eventId not in PRESHOW_DICT:
            FireworkShowMixin.notify.warning('Invalid fireworks event ID: %d' % eventId)
            return None

        instructionMessage, startMessage, endMessage, songs = PRESHOW_DICT[eventId]
        musicFile = 'phase_4/audio/bgm/%s.ogg' % songs[songId]

        self.showMusic = loader.loadMusic(musicFile)
        self.showMusic.setVolume(1)

        def __lightDecorationOn__():
            place = base.cr.playGame.getPlace()
            if place is None:
                return
            if hasattr(place, 'halloweenLights'):
                if not self.__checkStreetValidity():
                    return
                else:
                    place.halloweenLights = base.cr.playGame.getPlace().loader.geom.findAllMatches('**/*light*')
                    place.halloweenLights.extend(base.cr.playGame.getPlace().loader.geom.findAllMatches('**/*lamp*'))
                    for light in place.halloweenLights:
                        light.setColorScaleOff(0)

            elif not self.__checkHoodValidity():
                return
            else:
                place.loader.hood.halloweenLights = base.cr.playGame.hood.loader.geom.findAllMatches('**/*light*')
                place.loader.hood.halloweenLights.extend(base.cr.playGame.hood.loader.geom.findAllMatches('**/*lamp*'))
                for light in base.cr.playGame.hood.halloweenLights:
                    light.setColorScaleOff(0)

            if self.fireworkShow and not self.fireworkShow.isEmpty():
                self.fireworkShow.setColorScaleOff(0)
            return

        if self.__checkHoodValidity() and hasattr(base.cr.playGame, 'hood') and base.cr.playGame.hood \
                and hasattr(base.cr.playGame.hood, 'sky') and base.cr.playGame.hood.sky:
            return Sequence(
                Func(base.localAvatar.setSystemMessage, 0, startMessage),
                Parallel(
                    LerpColorScaleInterval(base.cr.playGame.hood.sky, 2.5, Vec4(0.0, 0.0, 0.0, 1.0)),
                    LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, 2.5, Vec4(0.25, 0.25, 0.35, 1)),
                    LerpColorScaleInterval(base.localAvatar, 2.5, Vec4(0.85, 0.85, 0.85, 1)), Func(__lightDecorationOn__)
                ),
                Func(base.setBackgroundColor, Vec4(0, 0, 0, 1)),
                Func(self.__checkDDFog), Func(base.camLens.setFar, 1000.0),
                Func(base.cr.playGame.hood.sky.hide),
                Func(base.localAvatar.setSystemMessage, 0, instructionMessage),
                Func(self.getLoader().music.stop),
                Wait(2.0),
                Func(base.playMusic, self.showMusic, 0, 1, 0.8, max(0, startT))
            )
        return None

    def restoreCameraLens(self):
        hood = self.getHood()
        if hood is not None:
            if hood.id == GoofySpeedway or hood.id == OutdoorZone:
                base.camLens.setFar(SpeedwayCameraFar)
            else:
                base.camLens.setFar(DefaultCameraFar)

    def postShow(self, eventId):
        endMessage = POSTSHOW_DICT.get(eventId)
        if endMessage is None:
            FireworkShowMixin.notify.warning('Invalid fireworks event ID: %d' % eventId)
            return None

        if self.__checkHoodValidity() and hasattr(base.cr.playGame.hood, 'sky') and base.cr.playGame.hood.sky:
            postShow = Sequence(
                Func(base.cr.playGame.hood.sky.show),
                Parallel(
                    LerpColorScaleInterval(base.cr.playGame.hood.sky, 2.5, Vec4(1, 1, 1, 1)),
                    LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, 2.5, Vec4(1, 1, 1, 1)),
                    LerpColorScaleInterval(base.localAvatar, 2.5, Vec4(1, 1, 1, 1))
                ),
                Func(self.__restoreDDFog),
                Func(self.restoreCameraLens),
                Func(base.setBackgroundColor, DefaultBackgroundColor),
                Func(self.showMusic.stop),
                Func(base.localAvatar.setSystemMessage, 0, endMessage)
            )
        if self.restorePlaygroundMusic:
            postShow.append(Wait(2.0))
            postShow.append(Func(base.playMusic, self.getLoader().music, 1, 1, 0.8))
        return postShow

    def createFireworkShow(self):
        if not self.fireworkShow:
            self.fireworkShow = FireworkShow(self.eventId)

    def destroyFireworkShow(self):
        if self.fireworkShow:
            self.fireworkShow.cleanupShow()
            self.fireworkShow = None
        return

    def beginFireworkShow(self, timeStamp, root):
        if self.fireworkShow and not self.fireworkShow.isPlaying():
            self.fireworkShow.begin(timeStamp)
            self.fireworkShow.reparentTo(root)
            hoodId = self.getHood().id
            if hoodId in FIREWORK_SHOW_LOCATION:
                self.fireworkShow.setPosHpr(*FIREWORK_SHOW_LOCATION[hoodId])
            if hoodId == PartyHood:
                self.fireworkShow.setScale(1.8)

    def getFireworkShowIval(self, eventId, index, songId, startT):
        show = FireworkShows.getShow(eventId, index)
        if show is None:
            FireworkShowMixin.notify.warning('could not find firework show: index: %s' % index)
            return
        preShow = self.preShow(eventId, songId, startT)
        mainShow = Sequence()
        currentT = skyTransitionDuration + preShowPauseDuration
        for effect in show:
            waitTime, style, colorIndex1, colorIndex2, amp, x, y, z = effect
            if waitTime > 0:
                currentT += waitTime
                mainShow.append(Wait(waitTime))
            if currentT >= startT:
                mainShow.append(Func(Fireworks.shootFirework, style, x, y, z, colorIndex1, colorIndex2, amp))

        postShow = self.postShow(eventId)
        return Sequence(preShow, mainShow, postShow)

    def clearMyColorScales(self):
        if self.getGeom() and not self.getGeom().isEmpty():
            self.getGeom().clearColorScale()
        if self.getSky() and not self.getSky().isEmpty():
            self.getSky().clearColorScale()

    def getLoader(self):
        if base.cr.playGame.hood is not None:
            return base.cr.playGame.hood.loader
        return

    def getHood(self):
        if base.cr.playGame.hood is not None:
            return base.cr.playGame.hood
        return

    def getGeom(self):
        loader = self.getLoader()
        if loader:
            return loader.geom
        return None

    def getSky(self):
        hood = self.getHood()
        if hood:
            return hood.sky
        return None

    def __checkDDFog(self):
        if self.getHood().id == DonaldsDock:
            self.getHood().whiteFogColor = Vec4(0.2, 0.2, 0.2, 1)
            if hasattr(base.cr.playGame.getPlace(), 'cameraSubmerged'):
                if not base.cr.playGame.getPlace().cameraSubmerged:
                    self.getHood().setWhiteFog()

    def __restoreDDFog(self):
        if self.getHood().id == DonaldsDock:
            self.getHood().whiteFogColor = Vec4(0.8, 0.8, 0.8, 1)
            if hasattr(base.cr.playGame.getPlace(), 'cameraSubmerged'):
                if not base.cr.playGame.getPlace().cameraSubmerged:
                    self.getHood().setWhiteFog()

    def __checkStreetValidity(self):
        return hasattr(base.cr.playGame, 'getPlace') and base.cr.playGame.getPlace()\
            and hasattr(base.cr.playGame.getPlace(), 'loader') and base.cr.playGame.getPlace().loader\
            and hasattr(base.cr.playGame.getPlace().loader, 'geom') and base.cr.playGame.getPlace().loader.geom

    def __checkHoodValidity(self):
        return hasattr(base.cr.playGame, 'hood') and base.cr.playGame.hood\
            and hasattr(base.cr.playGame.hood, 'loader') and base.cr.playGame.hood.loader\
            and hasattr(base.cr.playGame.hood.loader, 'geom') and base.cr.playGame.hood.loader.geom
