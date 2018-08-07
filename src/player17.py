import player16
import threading
from socket import *
import math


class Player17(player16.Player16, threading.Thread):
    def __init__(self):
        super(Player17, self).__init__()
        self.m_dBallX = []
        self.m_dBallY = []
        self.m_dBallVX = []
        self.m_dBallVY = []
        self.m_dBallAX = []
        self.m_dBallAY = []
        self.ball_size = 0.085
        self.player_size = 0.3
        self.kickable_margin = 0.7
        self.ball_decay = 0.96
        self.kick_power_rate = 0.027
        for _ in range(self.GAME_LENGTH):
            self.m_dBallX.append(0.0)
            self.m_dBallY.append(0.0)
            self.m_dBallVX.append(0.0)
            self.m_dBallVY.append(0.0)
            self.m_dBallAX.append(0.0)
            self.m_dBallAY.append(0.0)
        self.m_debugLv17 = False

    def predictKickCommand(self, i):
        next = (i + 1) % self.GAME_LENGTH
        if self.m_iVisualTime < 0:
            return
        command = self.m_strCommand[i]
        if command.startswith("(kick"):
            kick_power = self.getParam(command, "kick", 1)
            kick_angle = self.getParam(command, "kick", 2)
            angle = self.normalizeAngle(self.m_dBody[i] + kick_angle)
            kick_rad = angle * math.pi / 180
            ball_rad = math.atan2(self.m_dBallY[i] - self.m_dY[i], self.m_dBallX[i] - self.m_dX[i])
            dir = self.normalizeAngle(180 / math.pi * ball_rad - self.m_dBody[i])
            dir_diff = abs(dir / 180)
            dist = self.getDistance(self.m_dX[i], self.m_dY[i], self.m_dBallX[i], self.m_dBallY[i])
            dist_diff = (dist - self.player_size - self.ball_size) / self.kickable_margin
            if dist_diff < 1.0:
                ep = self.kick_power_rate * (1 - 0.25 * dir_diff - 0.25 * dist_diff)
                self.m_dBallAX[i] = kick_power * ep * math.cos(kick_rad)
                self.m_dBallAY[i] = kick_power * ep * math.sin(kick_rad)
            else:
                self.m_dBallAX[i] = 0.0
                self.m_dBallAY[i] = 0.0
        self.m_dBallVX[next] = (self.m_dBallVX[i] + self.m_dBallAX[i]) * self.ball_decay
        self.m_dBallVY[next] = (self.m_dBallVY[i] + self.m_dBallAY[i]) * self.ball_decay
        self.m_dBallX[next] = self.m_dBallX[i] + self.m_dBallVX[i] + self.m_dBallAX[i]
        self.m_dBallY[next] = self.m_dBallY[i] + self.m_dBallVY[i] + self.m_dBallAY[i]

    def predict(self, start, end):
        super().predict(start, end)

        if 0 < self.m_iTime < 25 and self.m_debugLv17:
            print("時刻", self.m_iTime)
            print("ボール")
            print("位置{0:.4f}, {1:.4f}".format(self.m_dBallX[self.m_iTime], self.m_dBallY[self.m_iTime]))
            print("速度{0:.4f}, {1:.4f}".format(self.m_dBallVX[self.m_iTime], self.m_dBallVY[self.m_iTime]))

            print("自分")
            print("位置{0:.4f}, {1:.4f}".format(self.m_dX[self.m_iTime], self.m_dY[self.m_iTime]))
            print("速度{0:.4f}, {1:.4f}".format(self.m_dVX[self.m_iTime], self.m_dVY[self.m_iTime]))
            print("首 {0:.4f}".format(self.m_dNeck[self.m_iTime]))
            print("体 {0:.4f}".format(self.m_dBody[self.m_iTime]))

    def analyzeServerParam(self, message):
        super().analyzeServerParam(message)
        self.ball_decay = self.getParam(self.m_strServerParam, "ball_decay", 1)
        self.player_decay = self.getParam(self.m_strServerParam, "player_decay", 1)
        self.ball_size = self.getParam(self.m_strServerParam, "ball_size", 1)
        self.kick_power_rate = self.getParam(self.m_strServerParam, "kick_power_rate", 1)

    def analyzePlayerType(self, message):
        super().analyzePlayerType(message)
        str = self.m_strPlayerType[self.m_iPlayerType]
        self.player_size = self.getParam(str, "player_size", 1)
        self.kickable_margin = self.getParam(str, "kickable_margin", 1)


if __name__ == "__main__":
    player17s = []
    for i in range(11):
        p17 = Player17()
        player17s.append(p17)
        teamname = "p17s"
        player17s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player17s[i].start()
    player17s[0].m_debugLv17 = True

    print("試合登録完了")