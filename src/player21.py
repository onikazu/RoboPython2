import player20
import threading
from socket import *
import math


class Player21(player20.Player20, threading.Thread):
    def __init__(self):
        super(Player21, self).__init__()
        self.m_debugLv21 = False

    def kick_0(self):
        t = self.m_iTime
        kickDir = self.getDirection(self.m_dX[t], self.m_dY[t], self.m_dKickX[t], self.m_dKickY[t])
        kickAngle = self.normalizeAngle(kickDir - self.m_dBody[t])
        self.m_strCommand[t] = "(kick 100 {0:.4f})".format(kickAngle)

    def move_0(self):
        t = self.m_iTime
        moveDir = self.getDirection(self.m_dX[t], self.m_dY[t], self.m_dMoveX[t], self.m_dMoveY[t])
        moveDist = self.getDistance(self.m_dX[t], self.m_dY[t], self.m_dMoveX[t], self.m_dMoveY[t])
        kickable_area = self.player_size + self.ball_size + self.kickable_margin
        if moveDist < kickable_area:
            self.m_strCommand[t] = "(turn 0)"
            return
        turn = self.normalizeAngle(moveDir - self.m_dBody[t])
        speed = math.sqrt(self.m_dVX[t] * self.m_dVX[t] + self.m_dVY[t] * self.m_dVY[t])
        turn_moment = turn * (1 + self.inertia_moment * speed * self.player_decay)
        dist = self.getDistance(self.m_dX[t], self.m_dY[t], self.m_dMoveX[t], self.m_dMoveY[t])
        self.dash_power_max = 100.0
        dash_power = 40.0

        if self.checkNearest_2(self.m_dMoveX[t], self.m_dMoveY[t]):
            dash_power = max(40.0, self.m_dStamina[t] / self.stamina_max * 100.0)

        d = dist

        count = 0

        while d > kickable_area and count < 50:
            speed = speed * self.player_decay + dash_power * self.m_dEffort[self.m_iTime] * self.dash_power_rate
            d -= speed
            count += 1

        # もし目的地の方向を向いていて
        if abs(turn) < 20.0:
            turn = 0.0
            dist = self.getDistance(self.m_dX[t], self.m_dY[t], self.m_dMoveX[t], self.m_dMoveY[t])
            # 更に遠ければ
            if dist > 0.75:
                self.m_strCommand[t] = "(dash {0:.4f})".format(dash_power)
        # もし目的地より反対方向を向いていて
        elif abs(turn) > 160.0 and dist < 3.51:
            turn = 0.0
            # 遠ければ
            if dist > 0.75:
                self.m_strCommand[t] = "(dash {0:.4f})".format(-dash_power)
        elif abs(turn_moment <= 180.0):
            self.m_strCommand[t] = "(turn {0:.4f})".format(turn_moment)
            if self.m_debugLv21:
                print("================================")
                print("t = {}".format(t))
                print("m_dMoveX[t]:{0:.4f}".format(self.m_dMoveX[t]))
                print("m_dMoveY[t]:{0:.4f}".format(self.m_dMoveY[t]))
                print("m_dBallX[t]:{0:.4f}".format(self.m_dBallX[t]))
                print("m_dBallY[t]:{0:.4f}".format(self.m_dBallY[t]))
                print("m_dTrapX{0:.4f}".format(self.m_dTrapX))
                print("m_dTrapY{0:.4f}".format(self.m_dTrapY))
                # ===================================
                print("moveDir{0:.4f}".format(moveDir))
                print("moveDist{0:.4f}".format(moveDist))
                print("m_headAngle[t]{0:.4f}".format(self.m_dHeadAngle[t]))
                print("m_dNeck[t]{0:.4f}".format(self.m_dNeck[t]))
                print("m_dBody[t]{0:.4f}".format(self.m_dBody[t]))
                print("speed{0:.4f}".format(speed))
                print("turn{0:.4f}".format(turn))
                print("turn_moment{0:.4f}".format(turn_moment))
                print("dist{0:.4f}".format(dist))
        else:
            speed_dir = self.getDirection(0, 0, self.m_dVX[t], self.m_dVY[t])
            rate = self.dash_power_rate * self.m_dEffort[t]
            if abs(self.normalizeAngle(speed_dir - moveDir)) < 20.0:
                dash_power = max(speed * self.player_decay / rate, dash_power)
            else:
                dash_power = min(-speed * self.player_decay / rate, -dash_power)
            self.m_strCommand[t] = "(dash {0:.4f})(say {1:.4f})".format(dash_power, turn_moment)
        print("self.m_strCommend[t]:", self.m_strCommand[t])

    def playWithBall(self):
        t = self.m_iTime
        super().playWithBall()
        if self.m_debugLv21:
            print("時刻{}".format(t))
            print("視覚{}".format(self.m_iVisualTime))
            print("player{}".format(self.m_iNumber))
            print("位置{0:.4f}, {1:.4f}".format(self.m_dX[t], self.m_dY[t]))
            print("速度{0:.4f}, {1:.4f}".format(self.m_dVX[t], self.m_dVY[t]))
            print("首{0:.4f}".format(self.m_dNeck[t]))
            print("体{0:.4f}".format(self.m_dBody[t]))
            print("ball({0:.4f}, {1:.4f})".format(self.m_dBallX[t], self.m_dBallY[t]))
            print("速度{0:.4f}, {1:.4f}".format(self.m_dBallVX[t], self.m_dBallVY[t]))
            print("コマンド{}".format(self.m_strCommand[t]))


if __name__ == "__main__":
    player21s = []
    for i in range(22):
        p21 = Player21()
        player21s.append(p21)
        teamname = str(p21.__class__.__name__)
        if i < 11:
            teamname += "left"
        else:
            teamname += "right"
        player21s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player21s[i].start()

    player21s[9].m_debugLv21 = True

    print("試合登録完了")