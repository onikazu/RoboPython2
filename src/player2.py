import player1
import threading
from socket import *


class Player2(player1.Player1, threading.Thread):
    def __init__(self):
        super(Player2, self).__init__()
        self.m_dKickOffX = 0.0
        self.m_dKickOffY = 0.0
        self.m_debugLv02 = False
        self.m_didPosition = False
        self.m_didTurn = False

    def checkInitialMode(self):
        if self.m_strPlayMode.startswith("before_kick_off") or \
            self.m_strPlayMode.startswith("goal_l") or \
            self.m_strPlayMode.startswith("goal_r"):
            return True
        else:
            return False

    def analyzeVisualMessage(self, message):
        return

    def setKickOffPosition(self):
        if self.m_iNumber == 1:
            self.m_dKickOffX = -50.0
            self.m_dKickOffY = -0.0
        elif self.m_iNumber == 2:
            self.m_dKickOffX = -40.0
            self.m_dKickOffY = -15.0
        elif self.m_iNumber == 3:
            self.m_dKickOffX = -40.0
            self.m_dKickOffY = -5.0
        elif self.m_iNumber == 4:
            self.m_dKickOffX = -40.0
            self.m_dKickOffY = +5.0
        elif self.m_iNumber == 5:
            self.m_dKickOffX = -40.0
            self.m_dKickOffY = +15.0
        elif self.m_iNumber == 6:
            self.m_dKickOffX = -20.0
            self.m_dKickOffY = -15.0
        elif self.m_iNumber == 7:
            self.m_dKickOffX = -20.0
            self.m_dKickOffY = -5.0
        elif self.m_iNumber == 8:
            self.m_dKickOffX = -20.0
            self.m_dKickOffY = +5.0
        elif self.m_iNumber == 9:
            self.m_dKickOffX = -20.0
            self.m_dKickOffY = +15.0
        elif self.m_iNumber == 10:
            self.m_dKickOffX = -1.0
            self.m_dKickOffY = -5.0
        elif self.m_iNumber == 11:
            self.m_dKickOffX = -4.0
            self.m_dKickOffY = +10.0
        else:
            print("範囲外の背番号の選手です")

    # 引数が一つのplay関数
    def play_1(self, message):
        if self.checkInitialMode():
            self.setKickOffPosition()
            command = "(move " + str(self.m_dKickOffX) + " " \
                + str(self.m_dKickOffY) + ")"
            if self.m_strSide.startswith("r"):
                command += "(turn_neck 180)"

            self.send(command)
            print(command)


    def analyzeMessage(self, message):
        super().analyzeMessage(message)
        if isinstance(message, type(None)):
            pass
            # print(message)
        elif message.startswith("(see "):
            self.analyzeVisualMessage(message)
            self.play_1(message)
        else:
            pass
            # print(message)


if __name__ == "__main__":
    players = []
    for i in range(22):
        p = Player2()
        players.append(p)
        if i < 11:
            teamname = "left"
        else:
            teamname = "right"
        players[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        players[i].start()
    print("試合登録完了")
