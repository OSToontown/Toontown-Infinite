from pandac.PandaModules import *
from panda3d.core import loadPrcFileData 
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
loadPrcFileData("",
"""
   load-display p3tinydisplay # to force CPU only rendering
   window-type offscreen # Spawn an offscreen buffer
   audio-library-name null # Prevent ALSA errors
   show-frame-rate-meter 0
   sync-video 0
   default-model-extension .bam
   model-path ../resources
""")
from direct.showbase.ShowBase import ShowBase 
base = ShowBase() 
from direct.actor.Actor import Actor

from SnapshotRendererConsts import *

def compileGlobalAnimList():
    phaseList = [Phase3AnimList,
     Phase3_5AnimList,
     Phase4AnimList,
     Phase5AnimList,
     Phase5_5AnimList,
     Phase6AnimList,
     Phase9AnimList,
     Phase10AnimList,
     Phase12AnimList]
    phaseStrList = ['phase_3',
     'phase_3.5',
     'phase_4',
     'phase_5',
     'phase_5.5',
     'phase_6',
     'phase_9',
     'phase_10',
     'phase_12']
    for animList in phaseList:
        phaseStr = phaseStrList[phaseList.index(animList)]
        for key in LegDict.keys():
            LegsAnimDict.setdefault(key, {})
            for anim in animList:
                file = phaseStr + LegDict[key] + anim[1]
                LegsAnimDict[key][anim[0]] = file

        for key in TorsoDict.keys():
            TorsoAnimDict.setdefault(key, {})
            for anim in animList:
                file = phaseStr + TorsoDict[key] + anim[1]
                TorsoAnimDict[key][anim[0]] = file

        for key in HeadDict.keys():
            if key.find('d') >= 0:
                HeadAnimDict.setdefault(key, {})
                for anim in animList:
                    file = phaseStr + HeadDict[key] + anim[1]
                    HeadAnimDict[key][anim[0]] = file


def loadModels():
    global Preloaded
    if not Preloaded:
        print 'Preloading avatars...'

        for key in LegDict.keys():
            fileRoot = LegDict[key]

            Preloaded[fileRoot+'-1000'] = loader.loadModel('phase_3' + fileRoot + '1000')
            Preloaded[fileRoot+'-500'] = loader.loadModel('phase_3' + fileRoot + '500')
            Preloaded[fileRoot+'-250'] = loader.loadModel('phase_3' + fileRoot + '250')

        for key in TorsoDict.keys():
            fileRoot = TorsoDict[key]

            Preloaded[fileRoot+'-1000'] = loader.loadModel('phase_3' + fileRoot + '1000')

            if len(key) > 1:
                Preloaded[fileRoot+'-500'] = loader.loadModel('phase_3' + fileRoot + '500')
                Preloaded[fileRoot+'-250'] = loader.loadModel('phase_3' + fileRoot + '250')


class SnapshotRenderer:
    def __init__(self, dnaString):
        self.dnaString = dnaString
        loadModels()
        compileGlobalAnimList()
        self.makeFromNetString(dnaString)
        self.toon = Actor()
        self.generateToon()
        self.renderSnapshot()


    def makeFromNetString(self, string):
        dg = PyDatagram(string)
        dgi = PyDatagramIterator(dg)
        self.type = dgi.getFixedString(1)
        if self.type == 't':
            headIndex = dgi.getUint8()
            torsoIndex = dgi.getUint8()
            legsIndex = dgi.getUint8()
            self.head = toonHeadTypes[headIndex]
            self.torso = toonTorsoTypes[torsoIndex]
            self.legs = toonLegTypes[legsIndex]
            gender = dgi.getUint8()
            if gender == 1:
                self.gender = 'm'
            else:
                self.gender = 'f'
            self.topTex = dgi.getUint8()
            self.topTexColor = dgi.getUint8()
            self.sleeveTex = dgi.getUint8()
            self.sleeveTexColor = dgi.getUint8()
            self.botTex = dgi.getUint8()
            self.botTexColor = dgi.getUint8()
            self.armColor = dgi.getUint8()
            self.gloveColor = dgi.getUint8()
            self.legColor = dgi.getUint8()
            self.headColor = dgi.getUint8()
        else:
            notify.error('unknown avatar type: ', self.type)

    def getAnimal(self):
        if self.head[0] == 'd':
            return 'dog'
        elif self.head[0] == 'c':
            return 'cat'
        elif self.head[0] == 'm':
            return 'mouse'
        elif self.head[0] == 'h':
            return 'horse'
        elif self.head[0] == 'r':
            return 'rabbit'
        elif self.head[0] == 'f':
            return 'duck'
        elif self.head[0] == 'p':
            return 'monkey'
        elif self.head[0] == 'b':
            return 'bear'
        elif self.head[0] == 's':
            return 'pig'
        else:
            notify.error('unknown headStyle: ', self.head[0])

    def getArmColor(self):
        try:
            return allColorsList[self.armColor]
        except:
            return allColorsList[0]

    def getLegColor(self):
        try:
            return allColorsList[self.legColor]
        except:
            return allColorsList[0]

    def getHeadColor(self):
        try:
            return allColorsList[self.headColor]
        except:
            return allColorsList[0]

    def getGloveColor(self):
        try:
            return allColorsList[self.gloveColor]
        except:
            return allColorsList[0]

    def getGender(self):
        return self.gender

    def generateToon(self):
        self.setLODs()
        self.generateToonLegs()
        self.generateToonHead(1, ('1000', '500', '250'))
        self.generateToonTorso()
        self.generateToonColor()
        self.parentToonParts()
        # self.rescaleToon()
        # self.resetHeight()
        # self.setupToonNodes()
        self.toon.reparentTo(render)
        self.toon.setPos(0, 5, -3)
        self.toon.setH(180)
        self.toon.getPart('head', '1000').setR(10)
        self.toon.pose('neutral', 0)

    def generateToonLegs(self, copy = 1):
        global Preloaded
        legStyle = self.legs
        filePrefix = LegDict.get(legStyle)
        if filePrefix is None:
            print('unknown leg style: %s' % legStyle)
        self.toon.loadModel(Preloaded[filePrefix+'-1000'], 'legs', '1000', True)
        self.toon.loadModel(Preloaded[filePrefix+'-500'], 'legs', '500', True)
        self.toon.loadModel(Preloaded[filePrefix+'-250'], 'legs', '250', True)
        if not copy:
            self.toon.showPart('legs', '1000')
            self.toon.showPart('legs', '500')
            self.toon.showPart('legs', '250')
        self.toon.loadAnims(LegsAnimDict[legStyle], 'legs', '1000')
        self.toon.loadAnims(LegsAnimDict[legStyle], 'legs', '500')
        self.toon.loadAnims(LegsAnimDict[legStyle], 'legs', '250')
        self.toon.findAllMatches('**/boots_short').stash()
        self.toon.findAllMatches('**/boots_long').stash()
        self.toon.findAllMatches('**/shoes').stash()
        return

    def generateToonTorso(self, copy = 1, genClothes = 1):
        global Preloaded
        torsoStyle = self.torso
        filePrefix = TorsoDict.get(torsoStyle)
        if filePrefix is None:
            self.notify.error('unknown torso style: %s' % torsoStyle)
        self.toon.loadModel(Preloaded[filePrefix+'-1000'], 'torso', '1000', True)
        if len(torsoStyle) == 1:
            self.toon.loadModel(Preloaded[filePrefix+'-1000'], 'torso', '500', True)
            self.toon.loadModel(Preloaded[filePrefix+'-1000'], 'torso', '250', True)
        else:
            self.toon.loadModel(Preloaded[filePrefix+'-500'], 'torso', '500', True)
            self.toon.loadModel(Preloaded[filePrefix+'-250'], 'torso', '250', True)
        if not copy:
            self.toon.showPart('torso', '1000')
            self.toon.showPart('torso', '500')
            self.toon.showPart('torso', '250')
        self.toon.loadAnims(TorsoAnimDict[torsoStyle], 'torso', '1000')
        self.toon.loadAnims(TorsoAnimDict[torsoStyle], 'torso', '500')
        self.toon.loadAnims(TorsoAnimDict[torsoStyle], 'torso', '250')
        if genClothes == 1 and not len(torsoStyle) == 1:
            self.generateToonClothes()
        return

    def generateToonClothes(self, fromNet = 0):
        swappedTorso = 0
        if self.toon.hasLOD():
            if self.getGender() == 'f' and fromNet == 0:
                try:
                    bottomPair = GirlBottoms[self.botTex]
                except:
                    bottomPair = GirlBottoms[0]
            try:
                texName = Shirts[self.topTex]
            except:
                texName = Shirts[0]

            shirtTex = loader.loadTexture(texName, okMissing=True)
            if shirtTex is None:
                shirtTex = loader.loadTexture(Shirts[0])
            shirtTex.setMinfilter(Texture.FTLinearMipmapLinear)
            shirtTex.setMagfilter(Texture.FTLinear)
            try:
                shirtColor = ClothesColors[self.topTexColor]
            except:
                shirtColor = ClothesColors[0]

            try:
                texName = Sleeves[self.sleeveTex]
            except:
                texName = Sleeves[0]

            sleeveTex = loader.loadTexture(texName, okMissing=True)
            if sleeveTex is None:
                self.sendLogSuspiciousEvent('failed to load texture %s' % texName)
                sleeveTex = loader.loadTexture(Sleeves[0])
            sleeveTex.setMinfilter(Texture.FTLinearMipmapLinear)
            sleeveTex.setMagfilter(Texture.FTLinear)
            try:
                sleeveColor = ClothesColors[self.sleeveTexColor]
            except:
                sleeveColor = ClothesColors[0]

            if self.getGender() == 'm':
                try:
                    texName = BoyShorts[self.botTex]
                except:
                    texName = BoyShorts[0]

            else:
                try:
                    texName = GirlBottoms[self.botTex][0]
                except:
                    texName = GirlBottoms[0][0]

            bottomTex = loader.loadTexture(texName, okMissing=True)
            if bottomTex is None:
                self.sendLogSuspiciousEvent('failed to load texture %s' % texName)
                if self.getGender() == 'm':
                    bottomTex = loader.loadTexture(BoyShorts[0])
                else:
                    bottomTex = loader.loadTexture(GirlBottoms[0][0])
            bottomTex.setMinfilter(Texture.FTLinearMipmapLinear)
            bottomTex.setMagfilter(Texture.FTLinear)
            try:
                bottomColor = ClothesColors[self.botTexColor]
            except:
                bottomColor = ClothesColors[0]

            darkBottomColor = bottomColor * 0.5
            darkBottomColor.setW(1.0)
            for lodName in self.toon.getLODNames():
                thisPart = self.toon.getPart('torso', lodName)
                top = thisPart.find('**/torso-top')
                top.setTexture(shirtTex, 1)
                top.setColor(shirtColor)
                sleeves = thisPart.find('**/sleeves')
                sleeves.setTexture(sleeveTex, 1)
                sleeves.setColor(sleeveColor)
                bottoms = thisPart.findAllMatches('**/torso-bot')
                for bottomNum in xrange(0, bottoms.getNumPaths()):
                    bottom = bottoms.getPath(bottomNum)
                    bottom.setTexture(bottomTex, 1)
                    bottom.setColor(bottomColor)

                caps = thisPart.findAllMatches('**/torso-bot-cap')
                caps.setColor(darkBottomColor)

        return swappedTorso

    def generateToonColor(self):
        parts = self.toon.findAllMatches('**/head*')
        parts.setColor(self.getHeadColor())
        animalType = self.getAnimal()
        if animalType == 'cat' or animalType == 'rabbit' or animalType == 'bear' or animalType == 'mouse' or animalType == 'pig':
            parts = self.toon.findAllMatches('**/ear?-*')
            parts.setColor(self.getHeadColor())

        armColor = self.getArmColor()
        gloveColor = self.getGloveColor()
        legColor = self.getLegColor()
        for lodName in self.toon.getLODNames():
            torso = self.toon.getPart('torso', lodName)
            if len(self.torso) == 1:
                parts = torso.findAllMatches('**/torso*')
                parts.setColor(armColor)
            for pieceName in ('arms', 'neck'):
                piece = torso.find('**/' + pieceName)
                piece.setColor(armColor)

            hands = torso.find('**/hands')
            hands.setColor(gloveColor)
            legs = self.toon.getPart('legs', lodName)
            for pieceName in ('legs', 'feet'):
                piece = legs.find('**/%s;+s' % pieceName)
                piece.setColor(legColor)

    def generateToonHead(self, copy, lods):
        headStyle = self.head
        fix = None
        if headStyle == 'dls':
            filePrefix = HeadDict['dls']
            headHeight = 0.75
        elif headStyle == 'dss':
            filePrefix = HeadDict['dss']
            headHeight = 0.5
        elif headStyle == 'dsl':
            filePrefix = HeadDict['dsl']
            headHeight = 0.5
        elif headStyle == 'dll':
            filePrefix = HeadDict['dll']
            headHeight = 0.75
        elif headStyle == 'cls':
            filePrefix = HeadDict['c']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'css':
            filePrefix = HeadDict['c']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'csl':
            filePrefix = HeadDict['c']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'cll':
            filePrefix = HeadDict['c']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'hls':
            filePrefix = HeadDict['h']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'hss':
            filePrefix = HeadDict['h']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'hsl':
            filePrefix = HeadDict['h']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'hll':
            filePrefix = HeadDict['h']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'mls':
            filePrefix = HeadDict['m']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'mss':
            filePrefix = HeadDict['m']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'rls':
            filePrefix = HeadDict['r']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'rss':
            filePrefix = HeadDict['r']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'rsl':
            filePrefix = HeadDict['r']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'rll':
            filePrefix = HeadDict['r']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'fls':
            filePrefix = HeadDict['f']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'fss':
            filePrefix = HeadDict['f']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'fsl':
            filePrefix = HeadDict['f']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'fll':
            filePrefix = HeadDict['f']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'pls':
            filePrefix = HeadDict['p']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'pss':
            filePrefix = HeadDict['p']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'psl':
            filePrefix = HeadDict['p']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'pll':
            filePrefix = HeadDict['p']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'bls':
            filePrefix = HeadDict['b']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'bss':
            filePrefix = HeadDict['b']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'bsl':
            filePrefix = HeadDict['b']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'bll':
            filePrefix = HeadDict['b']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'sls':
            filePrefix = HeadDict['s']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'sss':
            filePrefix = HeadDict['s']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'ssl':
            filePrefix = HeadDict['s']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'sll':
            filePrefix = HeadDict['s']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        else:
            ToonHead.notify.error('unknown head style: %s' % headStyle)
        if len(lods) == 1:
            self.toon.loadModel(filePrefix + lods[0], 'head', 'lodRoot', copy)
            if not copy:
                self.toon.showAllParts('head')
            if fix != None:
                fix(None, copy)
            self.__lods = lods
            self.__headStyle = headStyle
            self.__copy = copy
        else:
            for lod in lods:
                self.toon.loadModel(filePrefix + lod, 'head', lod, copy)
                if not copy:
                    self.toon.showAllParts('head', lod)
                if fix != None:
                    fix(lod, copy)
                self.__lods = lods
                self.__headStyle = headStyle
                self.__copy = copy

        # self.setupEyelashes()
        self.setupMuzzles()
        return headHeight


    def setupMuzzles(self):
        self.__muzzles = []
        self.__surpriseMuzzles = []
        self.__angryMuzzles = []
        self.__sadMuzzles = []
        self.__smileMuzzles = []
        self.__laughMuzzles = []

        def hideAddNonEmptyItemToList(item, list):
            if not item.isEmpty():
                item.hide()
                list.append(item)

        def hideNonEmptyItem(item):
            if not item.isEmpty():
                item.hide()

        if self.toon.hasLOD():
            for lodName in self.toon.getLODNames():
                animal = self.getAnimal()
                if animal != 'dog':
                    muzzle = self.toon.find('**/' + lodName + '/**/muzzle*neutral')
                else:
                    muzzle = self.toon.find('**/' + lodName + '/**/muzzle*')
                    if lodName == '1000' or lodName == '500':
                        filePrefix = DogMuzzleDict[self.head]
                        muzzles = self.toon.loadModel(filePrefix + lodName)
                        if base.config.GetBool('want-new-anims', 1):
                            if not self.toon.find('**/' + lodName + '/**/__Actor_head/def_head').isEmpty():
                                muzzles.reparentTo(self.toon.find('**/' + lodName + '/**/__Actor_head/def_head'))
                            else:
                                muzzles.reparentTo(self.toon.find('**/' + lodName + '/**/joint_toHead'))
                        elif self.toon.find('**/' + lodName + '/**/joint_toHead'):
                            muzzles.reparentTo(self.toon.find('**/' + lodName + '/**/joint_toHead'))
                surpriseMuzzle = self.toon.find('**/' + lodName + '/**/muzzle*surprise')
                angryMuzzle = self.toon.find('**/' + lodName + '/**/muzzle*angry')
                sadMuzzle = self.toon.find('**/' + lodName + '/**/muzzle*sad')
                smileMuzzle = self.toon.find('**/' + lodName + '/**/muzzle*smile')
                laughMuzzle = self.toon.find('**/' + lodName + '/**/muzzle*laugh')
                self.__muzzles.append(muzzle)
                hideAddNonEmptyItemToList(surpriseMuzzle, self.__surpriseMuzzles)
                hideAddNonEmptyItemToList(angryMuzzle, self.__angryMuzzles)
                hideAddNonEmptyItemToList(sadMuzzle, self.__sadMuzzles)
                hideAddNonEmptyItemToList(smileMuzzle, self.__smileMuzzles)
                hideAddNonEmptyItemToList(laughMuzzle, self.__laughMuzzles)

    def setupEyelashes(self):
        animal = self.head[0]
        model = self.toon.loadModel(EyelashDict[animal])
        if self.toon.hasLOD():
            head = self.toon.getPart('head', '1000')
        else:
            head = self.toon.getPart('head', 'lodRoot')
        length = self.head[1]
        if length == 'l':
            openString = 'open-long'
            closedString = 'closed-long'
        else:
            openString = 'open-short'
            closedString = 'closed-short'
        self.__eyelashOpen = model.find('**/' + openString).copyTo(head)
        self.__eyelashClosed = model.find('**/' + closedString).copyTo(head)
        model.removeNode()
        return

    def parentToonParts(self):
        if self.toon.hasLOD():
            for lodName in self.toon.getLODNames():
                if base.config.GetBool('want-new-anims', 1):
                    if not self.toon.getPart('torso', lodName).find('**/def_head').isEmpty():
                        self.toon.attach('head', 'torso', 'def_head', lodName)
                    else:
                        self.toon.attach('head', 'torso', 'joint_head', lodName)
                else:
                    self.toon.attach('head', 'torso', 'joint_head', lodName)
                self.toon.attach('torso', 'legs', 'joint_hips', lodName)
        else:
            self.toon.attach('head', 'torso', 'joint_head')
            self.toon.attach('torso', 'legs', 'joint_hips')

    def __fixHeadLongLong(self, lodName=None, copy=1):
        if lodName == None:
            searchRoot = self.toon
        else:
            searchRoot = self.toon.find('**/' + str(lodName))
        otherParts = searchRoot.findAllMatches('**/*short*')
        for partNum in xrange(0, otherParts.getNumPaths()):
            if copy:
                otherParts.getPath(partNum).removeNode()
            else:
                otherParts.getPath(partNum).stash()

        return

    def __fixHeadLongShort(self, lodName=None, copy=1):
        animalType = self.getAnimal()
        headStyle = self.head
        if lodName == None:
            searchRoot = self.toon
        else:
            searchRoot = self.toon.find('**/' + str(lodName))
        if animalType != 'duck' and animalType != 'horse':
            if animalType == 'rabbit':
                if copy:
                    searchRoot.find('**/ears-long').removeNode()
                else:
                    searchRoot.find('**/ears-long').hide()
            elif copy:
                searchRoot.find('**/ears-short').removeNode()
            else:
                searchRoot.find('**/ears-short').hide()
        if animalType != 'rabbit':
            if copy:
                searchRoot.find('**/eyes-short').removeNode()
            else:
                searchRoot.find('**/eyes-short').hide()
        if animalType != 'dog':
            if copy:
                searchRoot.find('**/joint_pupilL_short').removeNode()
                searchRoot.find('**/joint_pupilR_short').removeNode()
            else:
                searchRoot.find('**/joint_pupilL_short').stash()
                searchRoot.find('**/joint_pupilR_short').stash()
        if animalType != 'rabbit':
            muzzleParts = searchRoot.findAllMatches('**/muzzle-long*')
            for partNum in xrange(0, muzzleParts.getNumPaths()):
                if copy:
                    muzzleParts.getPath(partNum).removeNode()
                else:
                    muzzleParts.getPath(partNum).hide()

        else:
            muzzleParts = searchRoot.findAllMatches('**/muzzle-short*')
            for partNum in xrange(0, muzzleParts.getNumPaths()):
                if copy:
                    muzzleParts.getPath(partNum).removeNode()
                else:
                    muzzleParts.getPath(partNum).hide()

        return

    def __fixHeadShortLong(self, lodName=None, copy=1):
        animalType = self.getAnimal()
        headStyle = self.head
        if lodName == None:
            searchRoot = self.toon
        else:
            searchRoot = self.toon.find('**/' + str(lodName))
        if animalType != 'duck' and animalType != 'horse':
            if animalType == 'rabbit':
                if copy:
                    searchRoot.find('**/ears-short').removeNode()
                else:
                    searchRoot.find('**/ears-short').hide()
            elif copy:
                searchRoot.find('**/ears-long').removeNode()
            else:
                searchRoot.find('**/ears-long').hide()
        if animalType != 'rabbit':
            if copy:
                searchRoot.find('**/eyes-long').removeNode()
            else:
                searchRoot.find('**/eyes-long').hide()
        if animalType != 'dog':
            if copy:
                searchRoot.find('**/joint_pupilL_long').removeNode()
                searchRoot.find('**/joint_pupilR_long').removeNode()
            else:
                searchRoot.find('**/joint_pupilL_long').stash()
                searchRoot.find('**/joint_pupilR_long').stash()
        if copy:
            searchRoot.find('**/head-long').removeNode()
            searchRoot.find('**/head-front-long').removeNode()
        else:
            searchRoot.find('**/head-long').hide()
            searchRoot.find('**/head-front-long').hide()
        if animalType != 'rabbit':
            muzzleParts = searchRoot.findAllMatches('**/muzzle-short*')
            for partNum in xrange(0, muzzleParts.getNumPaths()):
                if copy:
                    muzzleParts.getPath(partNum).removeNode()
                else:
                    muzzleParts.getPath(partNum).hide()

        else:
            muzzleParts = searchRoot.findAllMatches('**/muzzle-long*')
            for partNum in xrange(0, muzzleParts.getNumPaths()):
                if copy:
                    muzzleParts.getPath(partNum).removeNode()
                else:
                    muzzleParts.getPath(partNum).hide()

        return

    def __fixHeadShortShort(self, lodName=None, copy=1):
        if lodName == None:
            searchRoot = self
        else:
            searchRoot = self.toon.find('**/' + str(lodName))
        otherParts = searchRoot.findAllMatches('**/*long*')
        for partNum in xrange(0, otherParts.getNumPaths()):
            if copy:
                otherParts.getPath(partNum).removeNode()
            else:
                otherParts.getPath(partNum).stash()

        return

    def setLODs(self):
        self.toon.setLODNode()
        levelOneIn = base.config.GetInt('lod1-in', 20)
        levelOneOut = base.config.GetInt('lod1-out', 0)
        levelTwoIn = base.config.GetInt('lod2-in', 80)
        levelTwoOut = base.config.GetInt('lod2-out', 20)
        levelThreeIn = base.config.GetInt('lod3-in', 280)
        levelThreeOut = base.config.GetInt('lod3-out', 80)
        self.toon.addLOD(1000, levelOneIn, levelOneOut)
        self.toon.addLOD(500, levelTwoIn, levelTwoOut)
        self.toon.addLOD(250, levelThreeIn, levelThreeOut)

    def loadPhaseAnims(self, phaseStr = 'phase_3', loadFlag = 1):
        if phaseStr == 'phase_3':
            animList = Phase3AnimList
        elif phaseStr == 'phase_3.5':
            animList = Phase3_5AnimList
        elif phaseStr == 'phase_4':
            animList = Phase4AnimList
        elif phaseStr == 'phase_5':
            animList = Phase5AnimList
        elif phaseStr == 'phase_5.5':
            animList = Phase5_5AnimList
        elif phaseStr == 'phase_6':
            animList = Phase6AnimList
        elif phaseStr == 'phase_9':
            animList = Phase9AnimList
        elif phaseStr == 'phase_10':
            animList = Phase10AnimList
        elif phaseStr == 'phase_12':
            animList = Phase12AnimList
        else:
            self.notify.error('Unknown phase string %s' % phaseStr)
        for key in LegDict.keys():
            for anim in animList:
                if loadFlag:
                    pass
                elif anim[0] in LegsAnimDict[key]:
                    if self.legs == key:
                        self.toon.unloadAnims([anim[0]], 'legs', None)

        for key in TorsoDict.keys():
            for anim in animList:
                if loadFlag:
                    pass
                elif anim[0] in TorsoAnimDict[key]:
                    if self.torso == key:
                        self.toon.unloadAnims([anim[0]], 'torso', None)

        for key in HeadDict.keys():
            if key.find('d') >= 0:
                for anim in animList:
                    if loadFlag:
                        pass
                    elif anim[0] in HeadAnimDict[key]:
                        if self.head == key:
                            self.toon.unloadAnims([anim[0]], 'head', None)
    def renderSnapshot(self):
        print 'Rendering Snapshot...'
        base.graphicsEngine.renderFrame()
        base.screenshot(namePrefix='snapshot-render', defaultFilename=1, source=None, imageComment="")
