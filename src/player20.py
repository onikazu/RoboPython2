import player19
import threading
from socket import *
import math


class Player20(player19.Player19, threading.Thread):
    def __init__(self):
        super(Player20, self).__init__()
        # キック目標座標
        self.m_dKickX = []
        self.m_dKickY = []
        # 移動目標座標
        self.m_dMoveX = []
        self.m_dMoveY = []
        # 方向目標座標
        self.m_dFaceX = []
        self.m_dFaceY = []
        self.m_iKickTime = []
        self.m_iMoveTime = []
        self.m_dTrapX = 0.0
        self.m_dTrapY = 0.0
        self.m_iTrapTime = 0
        for i in range(self.GAME_LENGTH):
            self.m_dKickX.append(0.0)
            self.m_dKickY.append(0.0)
            self.m_dMoveX.append(0.0)
            self.m_dMoveY.append(0.0)
            self.m_dFaceX.append(0.0)
            self.m_dFaceY.append(0.0)
            self.m_iKickTime.append(0)
            self.m_iMoveTime.append(0)
            self.m_iTime = i
            self.setKickTarget()
            self.setMoveTarget()
            self.setFaceTarget()
        self.m_iTime = 0
        self.m_debugLv20 = False

    def setKickTarget(self):
        t = self.m_iTime
        if self.m_strSide.startswith("r"):
            self.m_dKickX[t] = -52.5
        else:
            self.m_dKickX[t] = 52.5
        self.m_dKickY[t] = 0
        self.m_iKickTime[t] = self.m_iTime + 1

    def setTrapPosition(self):
        t = self.m_iTime
        self.m_dTrapX = self.m_dBallX[t]
        self.m_dTrapY = self.m_dBallY[t]

    def setDefencePosition_0(self):
        t = self.m_iTime
        self.setDefencePosition(self.m_dBallX[t], self.m_dBallY[t])

    def checkNearest_2(self, targetX, targetY):
        if self.m_iNumber == 10:
            return True
        else:
            return False

    def checkSetPlay(self):
        if self.m_strPlayMode.find("fault") > -1:
            return False
        if self.m_strPlayMode.startswith("kick_off_") or self.m_strPlayMode.startswith("kick_in_") \
            or self.m_strPlayMode.startswith("goal_kick_") or self.m_strPlayMode.startswith("corner_kick_") \
            or self.m_strPlayMode.startswith("free_kick_") or self.m_strPlayMode.startswith("indirect_free_kick_") \
            or self.m_strPlayMode.startswith("penalty_kick_"):
            return True
        else:
            return False

    def setMoveTarget(self):
        t = self.m_iTime
        self.m_iMoveTime[t] = t + 100
        self.setTrapPosition()
        self.setDefencePosition_0()
        if self.m_strPlayMode.startswith("play_on") or (self.checkSetPlay() and self.m_strPlayMode.endswith(self.m_strSide)):
            if self.checkNearest_2(self.m_dTrapX, self.m_dTrapY):
                self.m_dMoveX[t] = self.m_dTrapX
                self.m_dMoveY[t] = self.m_dTrapY
            else:
                self.m_dMoveX[t] = self.m_dDefenceX
                self.m_dMoveY[t] = self.m_dDefenceY
        else:
            self.m_dMoveX[t] = self.m_dX[t]
            self.m_dMoveY[t] = self.m_dY[t]

        if self.m_dMoveX[t] < -52.5:
            self.m_dMoveX[t] = -52.5
        if self.m_dMoveX[t] > 52.5:
            self.m_dMoveX[t] = 52.5
        if self.m_dMoveY[t] < -34.0:
            self.m_dMoveY[t] = -34.0
        if self.m_dMoveY[t] > 34.0:
            self.m_dMoveY[t] = 34.0

    def setFaceTarget(self):
        t = self.m_iTime
        next = (t + 1) % self.GAME_LENGTH
        self.m_dFaceX[t] = self.m_dBallX[next]
        self.m_dFaceY[t] = self.m_dBallY[next]

    def checkKickable(self):
        t = self.m_iTime
        kickablearea = self.ball_size + self.player_size + self.kickable_margin
        d = self.getDistance(self.m_dBallX[t], self.m_dBallY[t], self.m_dX[t], self.m_dY[t])
        if d > kickablearea:
            return False
        else:
            return True

    def kick_0(self):
        return

    def move_0(self):
        return

    def playWithBall(self):
        t = self.m_iTime
        if self.checkKickable():
            self.setKickTarget()
            self.kick_0()
        else:
            self.setMoveTarget()
            self.move_0()

        self.predict(t, t + 1)
        self.setFaceTarget()
        self.lookAt(self.m_dFaceX[t], self.m_dFaceY[t])

        if self.m_debugLv20:
            print("時刻{}".format(t))
            print("視覚{}".format(self.m_iVisualTime))
            print("player{}".format(self.m_iNumber))
            print("位置{0:.4f}, {1:.4f}".format(self.m_dX[t], self.m_dY[t]))
            print("kick{0:.4f}, {1:.4f}".format(self.m_dKickX[t], self.m_dKickY[t]))
            print("move{0:.4f}, {1:.4f}".format(self.m_dMoveX[t], self.m_dMoveY[t]))
            print("視線{0:.4f}, {1:.4f}".format(self.m_dFaceX[t], self.m_dFaceY[t]))
            print("コマンド{}".format(self.m_strCommand[t]))


if __name__ == "__main__":
    player20s = []
    for i in range(22):
        p20 = Player20()
        player20s.append(p20)
        teamname = str(p20.__class__.__name__)
        if i < 11:
            teamname += "left"
        else:
            teamname += "right"
        player20s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player20s[i].start()

    player20s[0].m_debugLv20 = True

    print("試合登録完了")