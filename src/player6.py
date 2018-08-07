import player5
import threading
from socket import *
import math


class Player6(player5.Player5, threading.Thread):
    def __init__(self):
        super(Player6, self).__init__()

    # 自分がボールに一番近いかどうかの判断
    def checkNearest(self, message, ballDist, ballDir):
        teamname = "(player " + self.m_strTeamName
        player = self.getObjectMessage(message, "((p")
        # print("player infomation: ", player)
        index0 = player.find(teamname, 0)
        while index0 > -1:
            # print("judged 最寄り判定")
            index1 = player.find(")", index0)
            index2 = player.find(" ", index1 + 1)
            index3 = player.find(" ", index2 + 1)
            index4 = player.find(" ", index3 + 1)
            index5 = player.find(")", index3 + 1)
            if index5 < index4 or index4 == -1:
                index4 = index5
            playerDist = float(player[index2:index3])
            playerDir = float(player[index3:index4])
            A = ballDist
            B = playerDist
            rad = math.pi / 180.0 * (playerDir - ballDir)
            dist = math.sqrt(A * A + B * B - 2 * A * B * math.cos(rad))
            if dist < ballDist:
                return False
                # print("judged")
            index0 = player.find(teamname, index0 + len(teamname))
        return True

    def getCommandAsDefence(self, message, ballDist, ballDir):
        command = ""
        goal = "(g l)"
        if self.m_strSide.startswith("r"):
            goal = "(g r)"
        if message.find(goal) > -1:
            goalDist = self.getParam(message, goal, 1)
            if goalDist > 50.0:
                command = "(dash 80)"
        return command

    def play_3(self, message, ballDist, ballDir):
        # ボールが視界に無いとき
        command = ""
        # 体の正面にある
        if abs(ballDir) < 20.0:
            # そして近い
            if ballDist < 1.0:
                command = self.kick(message)
                print("b No",self.m_iNumber, command)
            # 遠い
            elif self.checkNearest(message, ballDist, ballDir):
                command = "(dash 80)"
                print("d No",self.m_iNumber, command)
            else:
                command = self.getCommandAsDefence(message, ballDist, ballDir)
                print("defencecommandNo",self.m_iNumber, command)
        # 体の正面にはない　ここがおかしいと見て間違いない
        else:
            command = "(turn " + str(ballDir) + ")"
            print("c No",self.m_iNumber, command)

        self.send(command)
        # print("p6 command No", self.m_iNumber, command)


if __name__ == "__main__":
    player6s = []
    for i in range(11):
        p6 = Player6()
        player6s.append(p6)
        teamname = "p6s"
        player6s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player6s[i].start()
    player5s = []
    for i in range(11):
        p5 = player5.Player5()
        player5s.append(p5)
        teamname = "p5s"
        player5s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player5s[i].start()

    print("試合登録完了")
