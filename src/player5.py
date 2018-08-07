import player4
import threading
from socket import *


class Player5(player4.Player4, threading.Thread):
    def __init__(self):
        super(Player5, self).__init__()
        self.m_debugLv05 = False

    def kick(self, message):
        target_goal = ""
        if self.m_strSide.startswith("r"):
            target_goal = "(g l)"
        else:
            target_goal = "(g r)"
        index0 = message.find(target_goal)
        # ゴールが見えているときはゴール方向に蹴る
        if index0 > -1:
            goalDist = self.getParam(message, target_goal, 1)
            goalDir = self.getParam(message, target_goal, 2)
            return "(kick 100 " + str(goalDir) + ")"
        else:
            # そうでないときは斜め後ろに蹴る
            return "(kick 20 135)"

    def play_3(self, message, ballDist, ballDir):
        command = ""
        # 体の正面にある
        if abs(ballDir) < 20.0:
            # そして近い
            if ballDist < 1.0:
                command = self.kick(message)
                print("b", command)
            # 遠い
            elif self.checkNearest(message, ballDist, ballDir):
                command = "(dash 80)"
                print("d", command)
        # 体の正面にはない　ここがおかしいと見て間違いない
        else:
            command = "(turn " + str(ballDir) + ")"
            print("c", command)
        self.send(command)

    def checkNearest(self, message, ballDist, ballDir):
        return True


if __name__ == "__main__":
    players = []
    for i in range(22):
        p = Player5()
        players.append(p)
        if i < 11:
            teamname = "left"
        else:
            teamname = "right"
        players[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        players[i].start()
    print("試合登録完了")
