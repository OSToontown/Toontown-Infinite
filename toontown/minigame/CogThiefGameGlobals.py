from pandac.PandaModules import VBase3, BitMask32
from itertools import izip

GameTime = 60
NumBarrels = 4
BarrelStartingPositions = (VBase3(4.3, 4, 0),
 VBase3(4.3, -4, 0),
 VBase3(-4.3, 4, 0),
 VBase3(-4.3, -4, 0))
ToonStartingPositions = (VBase3(0, 16, 0),
 VBase3(0, -16, 0),
 VBase3(-16, 0, 0),
 VBase3(16, 0, 0))
CogStartingPositions = (VBase3(35, 18, 0),
 VBase3(35, 0, 0),
 VBase3(35, -18, 0),
 VBase3(-35, 18, 0),
 VBase3(-35, 0, 0),
 VBase3(-35, -18, 0),
 VBase3(0, 27, 0),
 VBase3(0, -27, 0),
 VBase3(35, 9, 0),
 VBase3(-35, 9, 0),
 VBase3(35, -9, 0),
 VBase3(-35, -9, 0))
CogReturnPositions = (VBase3(-35, 28, 0),
 VBase3(-14, 28, 0),
 VBase3(14, 28, 0),
 VBase3(35, 28, 0),
 VBase3(35, 0, 0),
 VBase3(35, -28, 0),
 VBase3(-14, -28, 0),
 VBase3(14, -28, 0),
 VBase3(-35, -28, 0),
 VBase3(-35, 0, 0))
StageHalfWidth = 25
StageHalfHeight = 18
NoGoal = 0
BarrelGoal = 1
ToonGoal = 2
RunAwayGoal = 3
InvalidGoalId = -1
GoalStr = {NoGoal: 'NoGoal',
 BarrelGoal: 'BarrelGoal',
 ToonGoal: 'ToonGoal',
 RunAwayGoal: 'RunAwayGoal',
 InvalidGoalId: 'InvalidGoa'}
BarrelBitmask = BitMask32(512)
BarrelOnGround = -1
NoBarrelCarried = -1
LyingDownDuration = 2.0
MAX_SCORE = 20
MIN_SCORE = 3


def calcScore(t):
    range = MAX_SCORE - MIN_SCORE
    score = range * (float(t) / GameTime) + MIN_SCORE
    return int(score + 0.5)


def getMaxScore():
    result = calcScore(GameTime)
    return result

Zones = (1000, 2000, 3000, 4000, 5000, 9000)

NumCogsTable = [
    {zoneId: i + zoneId / 1500 for zoneId in Zones} for i in xrange(5, 13, 2)
]

CogSpeedTable = [
    {zoneId: speed / 10.0 + zoneId / 20000.0 for zoneId, speed in izip(Zones, xrange(60, 84, 4))} for i in xrange(4)
]

ZoneSuitLevels = {zoneId: level for zoneId, level in izip(Zones, xrange(6))}

ToonSpeed = 9.0
PerfectBonus = [i for i in xrange(8, 0, -2)]


def calculateCogs(numPlayers, safezone):
    result = 5
    if numPlayers <= len(NumCogsTable):
        if safezone in NumCogsTable[numPlayers - 1]:
            result = NumCogsTable[numPlayers - 1][safezone]
    return result


def calculateCogSpeed(numPlayers, safezone):
    result = 6.0
    if numPlayers <= len(NumCogsTable):
        if safezone in CogSpeedTable[numPlayers - 1]:
            result = CogSpeedTable[numPlayers - 1][safezone]
    return result