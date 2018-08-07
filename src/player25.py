import player24
import threading
from socket import *
import math


class Player25(player24.Player24, threading.Thread):
    def __init__(self):
        super(Player25, self).__init__()
        self.m_debugLv25 = False

    def setKickTarget(self):
        # m_list でattribute error
        if not len(self.m_listPlayer):
            return
        t = self.m_iTime
        if self.m_strTeamName.startswith("Player25"):
            print("===========================")
            print("チーム{}".format(self.m_strTeamName))
            print("背番号{}".format(self.m_iNumber))
            print("時刻{}".format(self.m_iTime))
            print("視覚情報{}".format(self.m_iVisualTime))
            for i in range(len(self.m_listPlayer)):
                player = str(self.m_listPlayer[i])
                print(player)
                X = self.getParam(player, "x", 1)
                Y = self.getParam(player, "y", 1)
                Dir = self.getDirection(self.m_dX[t], self.m_dY[t], X, Y)
                Dist = self.getDistance(self.m_dX[t], self.m_dY[t], X, Y)
                print("Dir={0:.4f}, Dist={0:.4f}".format(Dir, Dist))

        for i in range(len(self.m_listPlayer)):
            player1 = str(self.m_listPlayer[1])
            friendDir = self.OUT_OF_RANGE
            friendDist = self.OUT_OF_RANGE
            max_score = 0.0
            if player1.find("friend") > -1:
                friendX = self.getParam(player1, "x", 1)
                friendY = self.getParam(player1, "y", 1)
                friendDir = self.getDirection(self.m_dX[t], self.m_dY[t], friendX, friendY)
                friendDist = self.getDistance(self.m_dX[t], self.m_dY[t], friendX, friendY)
                if friendDist < 5.0 or friendDist > 45.0:
                    friendDist = friendDir = self.OUT_OF_RANGE
                score = self.getPassValue(self.m_dX[t], self.m_dY[t], friendX, friendY)
                if score > max_score:
                    self.m_dKickX[t] = friendX
                    self.m_dKickY[t] = friendY
                    self.m_iKickTime[t] = self.m_iTime + self.getPassCount(friendDist)
                    max_score = score
                if self.m_strTeamName.startswith("Player25"):
                    print("パス候補")
                    print("背番号 {}".format(self.getParam(player1, "number", 1)))
                    print("位置 {0:.4f},{1:.4f}".format(friendX, friendY))
                    print("距離 {0:.4f}".format(friendDist))
                    print("評価 {0:.4f}".format(score))

    def getMoveCount(self, dist, v0):
        count = 1
        d = 0.0
        v = v0
        while dist > d and count < 100:
            d = d + v
            v = v * self.player_decay + 100.0 * self.dash_power_rate
            count += 1
        return count

    def getPassCount(self, dist):
        if dist > 50.0:
            return 100
        v = 100.0 * self.kick_power_rate
        d = 0
        count = 1
        while dist > d and count < 100:
            d = d + v
            v = v * self.ball_decay
            count += 1
        return count

    def getPassValue(self, x0, y0, x1, y1):
        t = self.m_iTime
        value = 0.0
        goalX = 0.0
        goalY = 0.0
        if self.m_strSide.startswith("r"):
            goalX = -52.5
            goalY = 0.0
        else:
            goalX = 52.5
            goalY = 0.0
        value += 100.0 - self.getDistance(goalX, goalY, x1, y1)
        passDist = self.getDistance(x0, y0, x1, y1)
        passDir = self.getDirection(x0, y0, x1, y1)
        for j in range(len(self.m_listPlayer)):
            player2 = str(self.m_listPlayer[j])
            if player2.find("enemy") > -1:
                enemyX = self.getParam(player2, "x", 1)
                enemyY = self.getParam(player2, "y", 1)
                enemyDir = self.getDirection(x0, y0, enemyX, enemyY)
                enemyDist = self.getDistance(x0, y0, enemyX, enemyY)
                diff = abs(self.normalizeAngle(enemyDir - passDir))
                if diff < 10.0 and enemyDist < passDist:
                    value = 0.0

        return value

    def analyzeVisualMessage(self, message):
        super().analyzeVisualMessage(message)


if __name__ == "__main__":
    player25s = []
    for i in range(22):
        p25 = Player25()
        player25s.append(p25)
        teamname = str(p25.__class__.__name__)
        if i < 11:
            teamname += "left"
        else:
            teamname += "right"
        player25s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player25s[i].start()

    player25s[2].m_debugLv25 = True

    print("試合登録完了")
