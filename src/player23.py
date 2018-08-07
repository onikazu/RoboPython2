import player22
import threading
from socket import *
import math


class Player23(player22.Player22, threading.Thread):
    def __init__(self):
        super(Player23, self).__init__()
        self.m_iTrapMarginSteps = 3
        self.player_speed_max = 1.20
        self.m_debugLv23 = False
        for _ in range(self.GAME_LENGTH):
            self.setKickTarget()
            self.setMoveTarget()
            self.setFaceTarget()

    def setTrapPosition(self):
        t = self.m_iTime
        moveTurn = 2
        dash_power = 100.0 * self.m_dEffort[t] * self.m_dStamina[t] / self.stamina_max
        self.setTrapPosition_2(dash_power, moveTurn)
        d = self.getDistance(self.m_dTrapX, self.m_dTrapY, self.m_dX[t], self.m_dY[t])
        rad = math.atan2(self.m_dTrapY - self.m_dY[t], self.m_dTrapX - self.m_dX[t])
        turnAngle = abs(self.normalizeAngle(math.degrees(rad) - self.m_dBody[t]))
        if turnAngle < 10.0 or turnAngle > 170.0:
            moveTurn = 0
            self.setTrapPosition_2(dash_power, moveTurn)
        elif turnAngle < 60.0:
            moveTurn = 1
            self.setTrapPosition_2(dash_power, moveTurn)
        else:
            moveTurn = 2
            self.setTrapPosition_2(dash_power, moveTurn)

        # m_debug で何故かエラー
        if 0 < self.m_iTime < 40 and self.m_debugLv23:
            print("時刻{}".format(self.m_iTime))
            print("視覚{}".format(self.m_iVisualTime))
            print("トラップ{}".format(self.m_iTrapTime))
            print("場所{0:.4f}, {1:.4f}".format(self.m_dTrapX, self.m_dTrapY))
            print("ボール")
            print("位置{0:.4f}, {1:.4f}".format(self.m_dBallX[self.m_iTime], self.m_dBallY[self.m_iTime]))
            print("速度{0:.4f}, {1:.4f}".format(self.m_dBallVX[self.m_iTime], self.m_dBallVY[self.m_iTime]))
            print("自分")
            print("位置{0:.4f}, {0:.4f}".format(self.m_dX[self.m_iTime], self.m_dY[self.m_iTime]))
            print("速度{0:.4f}, {0:.4f}".format(self.m_dVX[self.m_iTime], self.m_dVY[self.m_iTime]))
            print("体{0:.4f}".format(self.m_dNeck[self.m_iTime]))
            print("首{0:.4f}".format(self.m_dBody[self.m_iTime]))

    def setTrapPosition_2(self, dash_power, stable_steps):
        t = self.m_iTime
        next = (t + 1) % self.GAME_LENGTH
        kickable_area = self.player_size + self.ball_size + self.kickable_margin
        cover_area = kickable_area
        ball_dist = self.getDistance(self.m_dX[t], self.m_dY[t], self.m_dBallX[t], self.m_dBallY[t])
        player_speed = 0.0
        while cover_area < ball_dist and abs(t - next) < 100:
            # ボールの将来位置の予測
            self.m_dBallX[next] = self.m_dBallX[t] + self.m_dBallVX[t]
            self.m_dBallY[next] = self.m_dBallY[t] + self.m_dBallVY[t]
            self.m_dBallVX[next] = self.m_dBallVX[t] * self.ball_decay
            self.m_dBallVY[next] = self.m_dBallVY[t] * self.ball_decay
            # 選手の計算開始位置の予測
            self.m_dX[next] = self.m_dX[t] + self.m_dVX[t]
            self.m_dY[next] = self.m_dY[t] + self.m_dVY[t]
            self.m_dVX[next] = self.m_dVX[t] * self.player_decay
            self.m_dVY[next] = self.m_dVY[t] * self.player_decay
            self.m_dBody[next] = self.m_dBody[t]
            self.m_dNeck[next] = self.m_dNeck[t]
            current_power = 0.0
            if (t - self.m_iTime) >= stable_steps + self.m_iTrapMarginSteps:
                current_power = abs(dash_power)
            speed = player_speed * self.player_decay + current_power * self.dash_power_rate
            player_speed = min(speed, self.player_speed_max)
            cover_area += (player_speed * 0.9)
            t = (t + 1) % self.GAME_LENGTH
            next = (t + 1) % self.GAME_LENGTH
            ball_dist = self.getDistance(self.m_dX[t], self.m_dY[t], self.m_dBallX[t], self.m_dBallY[t])
        self.m_dTrapX = self.m_dBallX[t]
        self.m_dTrapY = self.m_dBallY[t]
        self.m_iTrapTime = t

    def analyzePlayerType(self, message):
        super().analyzePlayerType(message)
        type = self.m_strPlayerType[self.m_iPlayerType]
        # selfでは？
        player_speed_max = self.getParam(type, "player_speed_max", 1)


if __name__ == "__main__":
    player23s = []
    for i in range(22):
        p23 = Player23()
        player23s.append(p23)
        teamname = str(p23.__class__.__name__)
        if i < 11:
            teamname += "left"
        else:
            teamname += "right"
        player23s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player23s[i].start()

    player23s[2].m_debugLv23 = True

    print("試合登録完了")