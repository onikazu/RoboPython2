# lv3
import player2
import threading
from socket import *


class Player3(player2.Player2, threading.Thread):
    def __init__(self):
        super(Player3, self).__init__()
        self.m_debugLv03 = False

    def analyzeInitialMessage(self, message):
        super().analyzeInitialMessage(message)
        if self.m_debugLv03:
            print("m_strPlayMode:" + self.m_strPlayMode)

    def analyzeMessage(self, message):
        super().analyzeMessage(message)
        if message.startswith("(hear "):
            self.analyzeAuralMessage(message)

    def analyzeAuralMessage(self, message):
        index0 = message.find(" ")
        index1 = message.find(" ", index0+1)
        index2 = message.find(" ", index1+1)
        index3 = message.find(")", index2+1)
        strSpeaker = message[index1+1:index2]
        strContent = message[index2+1:index3]

        if strSpeaker.startswith("referee"):
            self.m_strPlayMode = strContent

        if self.m_debugLv03:
            print("m_strPlayMode:" + self.m_strPlayMode)

    def play_1(self, message):
        super().play_1(message)
        command = ""
        if self.m_strPlayMode.startswith("kick_off_"):
            command = "(turn 20)"
        else:
            command = "(turn -60)"
        self.send(command)


if __name__ == "__main__":
    players = []
    for i in range(22):
        p = Player3()
        players.append(p)
        if i < 11:
            teamname = "left"
        else:
            teamname = "right"
        players[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        players[i].start()
    print("試合登録完了")
    players[10].m_debugLv03 = True
