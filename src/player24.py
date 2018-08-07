import player23
import threading
from socket import *
import math


class Player24(player23.Player23, threading.Thread):
    def __init__(self):
        super(Player24, self).__init__()
        self.m_debugLv24 = False

    def setKickTarget(self):
        t = self.m_iTime
        if self.m_strSide.startswith("r"):
            self.m_dKickX[t] = -52.5
            self.m_dKickY[t] = 0.0
            self.m_iKickTime[t] = self.m_iTime + 1
        else:
            self.m_dKickX[t] = 52.5
            self.m_dKickY[t] = 0.0
            self.m_iKickTime[t] = self.m_iTime + 1
        if self.m_strTeamName.startswith("Player24"):
            if self.m_iNumber == 10:
                self.m_dKickX[t] = -1
                self.m_dKickY[t] = 5.0
                self.m_iKickTime[t] = t + 1
            elif self.m_iNumber == 11:
                self.m_dKickX[t] = -8.0
                self.m_dKickY[t] = 15.0
                self.m_iKickTime[t] = t + 5
            else:
                self.m_dKickX[t] = self.m_dBallX[self.m_iTime]
                self.m_dKickY[t] = self.m_dBallY[self.m_iTime]
                self.m_iKickTime[t] = self.m_iTime + 10

    def kick_2(self, kickX, kickY):
        t = self.m_iTime
        kickAX = kickX - self.m_dBallX[t] - self.m_dBallVX[t]
        kickAY = kickY - self.m_dBallY[t] - self.m_dBallVY[t]
        ball_rad = math.atan2(self.m_dBallY[t] - self.m_dY[t], self.m_dBallX[t] - self.m_dX[t])
        dir = self.normalizeAngle(180 / math.pi * ball_rad - self.m_dBody[t])
        dir_diff = abs(dir / 180)
        dist = self.getDistance(self.m_dX[t], self.m_dY[t], self.m_dBallX[t], self.m_dBallY[t])
        dist_diff = (dist - self.player_size - self.ball_size) / self.kickable_margin
        rate = self.kick_power_rate * (1 - 0.25 * dir_diff - 0.25 * dist_diff)
        rad = math.atan2(kickAX, kickAY)
        kick_dir = self.normalizeAngle(math.degrees(rad) - self.m_dBody[t])
        kick_power = math.sqrt(kickAX * kickAX + kickAY * kickAY) / rate
        self.m_strCommand[t] = "(kick {0:.4f} {1:.4f})".format(kick_power, kick_dir)

    def kick_0(self):
        t = self.m_iTime
        dx = self.m_dKickX[t] - self.m_dBallX[t]
        dy = self.m_dKickY[t] - self.m_dBallY[t]
        rad = (math.atan2(dy, dx))
        steps = self.m_iKickTime[t] - self.m_iTime
        s = (1 - math.pow(self.ball_decay, steps)) / (1 - self.ball_decay)
        dist = math.sqrt(dx * dx + dy * dy) / s
        kickX = dist * math.cos(rad) + self.m_dBallX[t]
        kickY = dist * math.sin(rad) + self.m_dBallY[t]
        self.kick_2(kickX, kickY)
        if self.m_strTeamName.startswith("Player24"):
            print("時刻{}".format(self.m_iTime))
            print("背番号{}".format(self.m_iNumber))
            print("ボール位置{0:.4f}, {1:.4f}".format(self.m_dBallX[self.m_iTime], self.m_dBallY[self.m_iTime]))
            print("速度{0:.4f}, {1:.4f}".format(self.m_dBallVX[self.m_iTime], self.m_dBallVY[self.m_iTime]))
            print("キック目標")
            print("時刻{}".format(self.m_iKickTime))
            print("位置{0:.4f}, {1:.4f}".format(self.m_dKickX[self.m_iTime], self.m_dKickY[self.m_iTime]))
            print("1ステップ後のキック目標{0:.4f}, {1:.4f}".format(kickX, kickY))


if __name__ == "__main__":
    player24s = []
    for i in range(22):
        p24 = Player24()
        player24s.append(p24)
        teamname = str(p24.__class__.__name__)
        if i < 11:
            teamname += "left"
        else:
            teamname += "right"
        player24s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player24s[i].start()

    player24s[2].m_debugLv24 = True

    print("試合登録完了")


