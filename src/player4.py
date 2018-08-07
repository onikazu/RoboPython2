# lv4
import player3
import threading
from socket import *


class Player4(player3.Player3, threading.Thread):
    def __init__(self):
        super(Player4, self).__init__()
        self.OUT_OF_RANGE = 999.9
        self.m_debugLv04 = False

    def getObjectMessage(self, message, keyword):
        result = ""
        index0 = message.find(keyword)
        while -1 < index0:
            index1 = message.find(")", index0+2)
            index2 = message.find(")", index1+1)
            result += message[index0:index2+1]
            result += ")"
            index0 = message.find(keyword, index2)
        return result

    def getParam(self, message, keyword, number):
        key = "(" + keyword
        index0 = message.find(key)
        if index0 < 0:
            return self.OUT_OF_RANGE

        index1 = message.find(" ", index0 + len(key))
        if number == 4:
            index1 = message.find(" ", index1 + 1)
        elif number == 3:
            index1 = message.find(" ", index1 + 1)
        elif number == 2:
            index1 = message.find(" ", index1 + 1)
        else:
            pass
        index2 = message.find(" ", index1+1)
        index3 = message.find(")", index1+1)
        if index3 < index2 and index3 != -1 or index2 == -1:
            index2 = index3
        result = 0.0
        try:
            result = float(message[index1:index2])
        except Exception:
            # print("player4[getParam]:文字データによるエラー")
            # print("error 時のgetparamの引数{} ,{}, {}".format(message, keyword, number))
            result = self.OUT_OF_RANGE
        return result

    # ボールが見えていないときのplay
    def play_1(self, message):
        if self.checkInitialMode():
            self.setKickOffPosition()
            command = "(move " + str(self.m_dKickOffX) + " " \
                + str(self.m_dKickOffY) + ")"
            self.send(command)
        else:
            message = message.replace("B", "b")
            ball = self.getObjectMessage(message, "((b")

            if ball.startswith("((b"):
                ballDist = self.getParam(ball, "(b)", 1)
                ballDir = self.getParam(ball, "(b)", 2)
                # print("p4 message", message)
                self.play_3(message, ballDist, ballDir)
            else:
                command = "(turn 30)"
                self.send(command)

    # ボールが見えているときのplay
    def play_3(self, message, ballDist, ballDir):
        pass


if __name__ == "__main__":
    players = []
    for i in range(22):
        p = Player4()
        players.append(p)
        if i < 11:
            teamname = "left"
        else:
            teamname = "right"
        players[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        players[i].start()
    print("試合登録完了")
    players[10].m_debugLv04 = True
