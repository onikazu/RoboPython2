import player14
import threading
from socket import *
import math


class Player15(player14.Player14, threading.Thread):
    def __init__(self):
        super(Player15, self).__init__()
        self.m_debugLv15 = False

    def predictDashCommand(self, i):
        command = self.m_strCommand[i]
        stamina = self.m_dStamina[i]
        recovery = self.m_dRecovery[i]
        effort = self.m_dEffort[i]
        if command.startswith("(dash"):
            dash_power = self.getParam(command, "dash", 1)
            if dash_power < 0:
                dash_power = dash_power * (-2.0)
            if stamina + self.extra_stamina < dash_power:
                dash_power = stamina + self.extra_stamina
                stamina = 0.0
                self.extra_stamina = 0.0
            elif stamina < dash_power:
                self.extra_stamina -= (dash_power - stamina)
                stamina = 0.0
            else:
                stamina -= dash_power

            if stamina <= self.recover_dec_thr * self.stamina_max:
                if recovery > self.recover_min:
                    recovery -= self.recover_dec
                recovery = max(recovery, self.recover_min)

            if stamina <= self.effort_dec_thr * self.stamina_max:
                if effort > self.effort_min:
                    effort -= self.effort_dec
                effort = max(effort, self.effort_min)

            if stamina >= self.effort_inc_thr * self.stamina_max:
                if effort < self.effort_max:

                # 正誤表より
                    effort += self.effort_inc
                effort = min(effort, self.effort_max)

            if self.getParam(command, "dash", 1) < 0:
                dash_power /= (-2.0)
            p = math.pi
            rad = self.m_dBody[i] * math.pi / 180
            ax = dash_power * self.dash_power_rate * self.m_dEffort[i] * math.cos(rad)
            ay = dash_power * self.dash_power_rate * self.m_dEffort[i] * math.sin(rad)
            self.m_dAX[i] = ax
            self.m_dAY[i] = ay

        stamina += recovery * self.stamina_inc_max
        stamina = min(stamina, self.stamina_max)
        next = (i + 1) % self.GAME_LENGTH
        self.m_dStamina[next] = stamina
        self.m_dEffort[next] = effort
        self.m_dRecovery[next] = recovery
        self.m_dVX[next] = (self.m_dVX[i] + self.m_dAX[i]) * self.player_decay
        self.m_dVY[next] = (self.m_dVY[i] + self.m_dAY[i]) * self.player_decay
        self.m_dX[next] = self.m_dX[i] + self.m_dVX[i] + self.m_dAX[i]
        self.m_dY[next] = self.m_dY[i] + self.m_dVY[i] + self.m_dAY[i]
        self.m_dAX[next] = 0.0
        self.m_dAY[next] = 0.0

    def predict(self, start, end):
        super().predict(start, end)
        if self.m_debugLv15 and 0 < self.m_iTime < 50:
            print("時刻", self.m_iTime)
            print("スタミナ {0:.4f}".format(self.m_dStamina[self.m_iTime]))
            print("実行効率{0:.4f}".format(self.m_dEffort[self.m_iTime]))
            print("回復力{0:.4f}".format(self.m_dRecovery[self.m_iTime]))
            print("位置{0:.4f}, {1:.4f}".format(self.m_dX[self.m_iTime], self.m_dY[self.m_iTime]))
            print("速度{0:.4f}, {1:.4f}".format(self.m_dVX[self.m_iTime], self.m_dVY[self.m_iTime]))


if __name__ == "__main__":
    player15s = []
    for i in range(11):
        p15 = Player15()
        player15s.append(p15)
        teamname = "p15s"
        player15s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player15s[i].start()

    player15s[0].m_debugLv15 = True
    print("試合登録完了")

