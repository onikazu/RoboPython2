import player12
import threading
from socket import *
import math


class Player13(player12.Player12, threading.Thread):
    def __init__(self):
        super(Player13, self).__init__()
        self.dash_power_rate = 0.006
        self.player_decay = 0.4
        self.m_debugLv13 = False

    def predictDashCommand(self, i):
        command = self.m_strCommand[i]
        if command.startswith("(dash"):
            dash_power = self.getParam(command, "dash", 1)
            p = math.pi
            rad = self.m_dBody[i] * math.pi / 180
            ax = dash_power * self.dash_power_rate * math.cos(rad)
            ay = dash_power * self.dash_power_rate * math.sin(rad)
            self.m_dAX[i] = ax
            self.m_dAY[i] = ay
        next = (i + 1) % self.GAME_LENGTH

        # どちらもint型
        # print("next", type(next))
        # print("i", type(i))
        # print("VX", type(self.m_dVX))
        # print("AX", type(self.m_dAX))
        # print("pd", type(self.player_decay))
        self.m_dVX[next] = (self.m_dVX[i] + self.m_dAX[i]) * self.player_decay
        self.m_dVY[next] = (self.m_dVY[i] + self.m_dAY[i]) * self.player_decay
        self.m_dX[next] = self.m_dX[i] + self.m_dVX[i] + self.m_dAX[i]
        self.m_dY[next] = self.m_dY[i] + self.m_dVY[i] + self.m_dAY[i]
        self.m_dAX[next] = 0.0
        self.m_dAY[next] = 0.0

    def predict(self, start, end):
        super().predict(start, end)
        if self.m_debugLv13 and self.m_iTime > 0 and self.m_iTime < 50:
            print()
            print("時刻", self.m_iTime)
            print("位置 {0:.4f}, {1:.4f}".format(self.m_dX[self.m_iTime], self.m_dY[self.m_iTime]))
            print("速度 {0:.4f}, {1:.4f}".format(self.m_dVX[self.m_iTime], self.m_dVY[self.m_iTime]))

    def play_0(self):
        super().play_0()
        if self.m_strPlayMode.startswith("kick_off"):
            command = ""
            if self.m_iTime % 10 < 5:
                command = "(dash 100)"
            else:
                command = "(dash -100)"
            self.m_strCommand[self.m_iTime] = command

    def analyzeServerParam(self, message):
        super().analyzeServerParam(message)
        self.player_decay = self.getParam(self.m_strServerParam, "player_decay", 1)
        self.dash_power_rate = self.getParam(self.m_strServerParam, "dash_power_rate", 1)


if __name__ == "__main__":
    player13s = []
    for i in range(11):
        p13 = Player13()
        player13s.append(p13)
        teamname = "p13s"
        player13s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player13s[i].start()

    player13s[0].m_debugLv13 = True
    print("試合登録完了")
