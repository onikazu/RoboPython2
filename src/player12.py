import player11
import threading
from socket import *
import math


class Player12(player11.Player11, threading.Thread):
    def __init__(self):
        super(Player12, self).__init__()
        self.m_dY = []
        self.m_dX = []
        self.m_dVX = []
        self.m_dVY = []
        self.m_dAX = []
        self.m_dAY = []
        self.m_dNeck = []
        self.m_dBody = []
        self.m_dStamina = []
        self.m_dEffort = []
        self.m_dRecovery = []
        self.m_debugLv12 = False
        for _ in range(self.GAME_LENGTH):
            self.m_dY.append(0.0)
            self.m_dX.append(0.0)
            self.m_dVX.append(0.0)
            self.m_dVY.append(0.0)
            self.m_dAX.append(0.0)
            self.m_dAY.append(0.0)
            self.m_dNeck.append(0.0)
            self.m_dBody.append(0.0)
            self.m_dStamina.append(0.0)
            self.m_dEffort.append(0.0)
            self.m_dRecovery.append(0.0)
        # print(self.m_dX[4])

    def predictMoveCommand(self, i):
        command = self.m_strCommand[i]
        if command.startswith("(move"):
            # print("moveコマンド", command)
            # print("self.m_strSide", self.m_strSide)
            x = self.getParam(command, "move", 1)
            y = self.getParam(command, "move", 2)

            if self.m_strSide.startswith("r"):
                # print("xy", x, y)
                x = -x
                y = -y

            self.m_dX[i] = x

            self.m_dY[i] = y
            # print(self.m_dY, self.m_dX)
            self.m_dAX[i] = self.m_dVX[i] = 0.0
            self.m_dAY[i] = self.m_dVY[i] = 0.0

        next = (i + 1) % self.GAME_LENGTH
        self.m_dX[next] = self.m_dX[i]
        self.m_dY[next] = self.m_dY[i]

    def predict(self, start, end):
        super().predict(start, end)
        if self.m_debugLv12 and self.m_iTime > 0 and self.m_iTime < 20:
            # print(type(self.m_dX))
            print("時刻", self.m_iTime)
            print("位置 {0:.4f}, {1:.4f}".format(self.m_dX[self.m_iTime], self.m_dY[self.m_iTime]))
            print(self.m_dX[:20])
            print(self.m_dY[:20])

    def analyzeInitialMessage(self, message):
        super().analyzeInitialMessage(message)
        if self.m_strSide.startswith("r"):
            self.m_dX[0] = 3 + 3 * self.m_iNumber
            self.m_dY[0] = -37.0
        else:
            self.m_dX[0] = -3 - 3 * self.m_iNumber
            self.m_dY[0] = -37.0


if __name__ == "__main__":
    player12s = []
    for i in range(11):
        p12 = Player12()
        player12s.append(p12)
        teamname = "p12s"
        player12s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player12s[i].start()

    player12s[1].m_debugLv12 = True
    print("試合登録完了")
