import player13
import threading
from socket import *
import math


class Player14(player13.Player13, threading.Thread):
    def __init__(self):
        super(Player14, self).__init__()
        self.stamina_max = 4000
        self.stamina_inc_max = 45
        self.recover_min = 0.5
        self.extra_stamina = 0.0
        self.recover_dec_thr = 0.3
        self.recover_dec = 0.002
        self.effort_min = 0.6
        self.effort_max = 1.0
        self.effort_dec_thr = 0.3
        self.effort_inc_thr = 0.6
        self.effort_dec = 0.005
        self.effort_inc = 0.01
        self.m_debugLv14 = False

    def analyzePlayerType(self, message):
        super().analyzePlayerType(message)
        type = self.m_strPlayerType[self.m_iPlayerType]
        # print("type", type)
        self.dash_power_rate = self.getParam(type, "dash_power_rate", 1)
        self.stamina_inc_max = self.getParam(type, "stamina_inc_max", 1)
        self.extra_stamina = self.getParam(type, "extra_stamina", 1)
        self.effort_max = self.getParam(type, "effort_max", 1)
        self.effort_min = self.getParam(type, "effort_min", 1)

    def analyzeServerParam(self, message):
        super().analyzeServerParam(message)
        self.stamina_max = self.getParam(message, "stamina_max", 1)
        self.recover_dec_thr = self.getParam(message, "recover_dec_thr", 1)
        self.recover_dec = self.getParam(message, "recover_dec", 1)
        self.recover_min = self.getParam(message, "recover_min", 1)
        self.effort_dec_thr = self.getParam(message, "effort_dec_thr", 1)
        self.effort_inc_thr = self.getParam(message, "effort_inc_thr", 1)
        self.effort_dec = self.getParam(message, "effort_dec", 1)
        self.effort_inc = self.getParam(message, "effort_inc", 1)

    def analyzePhysicalMessage(self, message):
        super().analyzePhysicalMessage(message)
        if self.m_strPlayMode.startswith("before_kick_off"):
            self.m_dRecovery[self.m_iTime] = 1.0
            self.m_dEffort[self.m_iTime] = 1.0
            self.m_dStamina[self.m_iTime] = self.stamina_max


if __name__ == "__main__":
    player14s = []
    for i in range(11):
        p14 = Player14()
        player14s.append(p14)
        teamname = "p14s"
        player14s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player14s[i].start()

    player14s[0].m_debugLv14 = True
    print("試合登録完了")
