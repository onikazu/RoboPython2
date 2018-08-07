# ボール位置の絶対座標を用いる
import player8
import threading
from socket import *
import math


class Player9(player8.Player8, threading.Thread):
    def __init__(self):
        super(Player9, self).__init__()
        self.m_dBallX = 0.0
        self.m_dBallY = 0.0
        self.m_dDefenceX = 0.0
        self.m_dDefenceY = 0.0

    def setDefencePosition(self, ballX, ballY):
        offsetX = 0.0
        offsetY = 0.0
        if self.m_iNumber == 1:
            offsetX, offsetY = -50.0, -0.0
        elif self.m_iNumber == 2:
            offsetX, offsetY = -30.0, -15.0
        elif self.m_iNumber == 3:
            offsetX, offsetY = -30.0, -5.0
        elif self.m_iNumber == 4:
            offsetX, offsetY = -30.0, +5.0
        elif self.m_iNumber == 5:
            offsetX, offsetY = -30.0, +15.0
        elif self.m_iNumber == 6:
            offsetX, offsetY = -10.0, -15.0
        elif self.m_iNumber == 7:
            offsetX, offsetY = -10.0, -15.0
        elif self.m_iNumber == 8:
            offsetX, offsetY = -10.0, +5.0
        elif self.m_iNumber == 9:
            offsetX, offsetY = -10.0, +15.0
        elif self.m_iNumber == 10:
            offsetX, offsetY = 10.0, -5.0
        elif self.m_iNumber == 11:
            offsetX, offsetY = 10.0, +5.0
        else:
            pass

        if self.m_iNumber == 1:
            # print("set gk")
            if self.m_strSide.startswith("r"):
                self.m_dDefenceX = 52.5
            else:
                self.m_dDefenceX = -52.5
            self.m_dDefenceY = 0.0
        else:
            if self.m_strSide.startswith("r"):
                self.m_dDefenceX = ballX / 2.0 - offsetX
                self.m_dDefenceY = ballY / 2.0 - offsetY
            else:
                self.m_dDefenceX = ballX / 2.0 + offsetX
                self.m_dDefenceY = ballY / 2.0 + offsetY

    def analyzeVisualMessage(self, message):
        super().analyzeVisualMessage(message)
        if message.find("(b)") == -1:
            return
        ballDist = self.getParam(message, "(b)", 1)
        ballDir = self.getParam(message, "(b)", 2)
        rad = math.radians(self.normalizeAngle(self.m_dNeck + ballDir))
        self.m_dBallX = self.m_dX + ballDist * math.cos(rad)
        self.m_dBallY = self.m_dY + ballDist * math.sin(rad)
        self.setDefencePosition(self.m_dBallX, self.m_dBallY)



if __name__ == "__main__":
    player8s = []
    for i in range(11):
        p8 = player8.Player8()
        player8s.append(p8)
        teamname = "p8s"
        player8s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player8s[i].start()
    player9s = []
    for i in range(11):
        p9 = Player9()
        player9s.append(p9)
        teamname = "p9s"
        player9s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player9s[i].start()

    print("試合登録完了")
