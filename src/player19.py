import player18
import threading
from socket import *
import math


class Player19(player18.Player18, threading.Thread):
    def __init__(self):
        super(Player19, self).__init__()
        self.m_iBallTime = -6
        self.m_iSearchCount = 0
        self.m_debugLv19 = False

    # 視覚情報の解析
    def analyzeVisualMessage(self, message):
        super().analyzeVisualMessage(message)
        if message.find("(ball") > -1:
            self.m_iBallTime = self.m_iVisualTime
            self.m_iSearchCount = 0
        elif self.checkFresh(self.m_iBallTime) == False:
            # print(self.m_iNumber, "p19 message without ball", message)
            if self.m_iSearchCount == 0 and self.checkInitialMode() == False:
                self.m_iSearchCount = 9

    # 時刻が最新の時刻であるか検査
    def checkFresh(self, time):
        if self.m_iTime - time > 3:
            return False
        else:
            return True

    # ボールを探す
    def searchBall(self, searchCount):
        t = self.m_iTime
        if searchCount == 9:
            self.m_strCommand[t] += "(turn_neck 180)"
            self.m_strCommand[t] += "(change_view wide high)"
        if searchCount == 6:
            self.m_strCommand[t] += "(turn_neck -180)"
            self.m_strCommand[t] += "(change_view wide high)"
        if searchCount == 3:
            # 教科書みす?
            self.m_strCommand[t] = "(turn 180)"
            self.m_strCommand[t] += "(turn_neck 90)"
            self.m_strCommand[t] += "(change_view wide high)"
        print(self.m_iNumber, "のserchcount: ", searchCount)

    # 座標で指定された方向に首を向ける
    def lookAt(self, faceX, faceY):
        t = self.m_iTime
        turn_angle = 0.0
        command = self.m_strCommand[t]
        if command.startswith("(turn "):
            moment = self.getParam(command, "turn", 1)
            vx = self.m_dVX[t]
            vy = self.m_dVY[t]
            speed = math.sqrt(vx * vx + vy * vy)
            turn_angle = moment / (1 + self.inertia_moment * speed)
        face_dir = self.getDirection(self.m_dX[t], self.m_dY[t], faceX, faceY)
        neck_diff = self.normalizeAngle(face_dir - turn_angle - self.m_dNeck[t])
        body_diff = self.normalizeAngle(face_dir - turn_angle - self.m_dBody[t])
        if self.m_dHeadAngle[t] + neck_diff > self.maxneckang:
            neck_diff = self.normalizeAngle(self.maxneckang - self.m_dHeadAngle[t])
        elif self.m_dHeadAngle[t] + neck_diff < self.minneckang:
            neck_diff = self.normalizeAngle(self.minneckang - self.m_dHeadAngle[t])

        if self.m_debugLv19 and 0 < t < 30:
            print("時刻{}".format(t))
            print("self.m_iSearchCount:", self.m_iSearchCount)
            print("視覚{}".format(self.m_iVisualTime))
            # 適切な出力得られていない
            print("目標")
            print("位置{0:.4f}, {1:.4f}".format(self.m_dBallX[t], self.m_dBallY[t]))
            print("方向{0:.4f}".format(face_dir))
            print("自分")
            print("位置{0:.4f}, {1:.4f}".format(self.m_dX[t], self.m_dY[t]))
            print("首{0:.4f}".format(self.m_dNeck[t]))
            print("体{0:.4f}".format(self.m_dBody[t]))
            print("body_diff {0:.4f}, neck_diff {0:.4f}".format(body_diff, neck_diff))
            print("self.m_strCommand: ", self.m_strCommand[t])
        # print("No. {}".format(self.m_iNumber))

        if abs(body_diff) < 90 + 22.5 / 2 and abs(neck_diff) < 22.5:
            self.m_strCommand[self.m_iTime] += "(turn_neck {0:.2f})".format(neck_diff)
            self.m_strCommand[self.m_iTime] += "(change_view narrow high)"
            # print("changed narrow view!!!!")
        elif abs(body_diff) < 90 + 45.0 / 2 and abs(neck_diff) < 45.0:
            self.m_strCommand[self.m_iTime] += "(turn_neck {0:.2f})".format(neck_diff)
            self.m_strCommand[self.m_iTime] += "(change_view normal high)"
        else:
            self.m_strCommand[self.m_iTime] += "(turn_neck {0:.2f})".format(neck_diff)
            self.m_strCommand[self.m_iTime] += "(change_view wide high)"

    # ボールが見えているときの行動を決定する
    def playWithBall(self):
        if self.m_debugLv19:
            print("ボール見えてるよ")
        t = self.m_iTime
        self.m_strCommand[t] = "(turn 0)"
        self.lookAt(self.m_dBallX[t], self.m_dBallY[t])

    # 行動を決定する
    def play_0(self):
        t = self.m_iTime
        self.m_strCommand[t] = "(turn 0)"
        if self.checkInitialMode():
            self.setKickOffPosition()
            command = "(move {} {})".format(self.m_dKickOffX, self.m_dKickOffY)
            self.m_strCommand[t] = command
        else:
            if abs(self.m_dNeck[t]) > 180.0:
                return
            if abs(self.m_dBody[t]) > 180.0:
                return
            if t > 0:
                if self.checkFresh(self.m_iBallTime) == False:
                    self.searchBall(self.m_iSearchCount)
                else:
                    self.playWithBall()

        self.m_iSearchCount -= 1
        if self.m_iSearchCount < 0:
            self.m_iSearchCount = 0


if __name__ == "__main__":
    player19s = []
    for i in range(22):
        p19 = Player19()
        player19s.append(p19)
        teamname = str(p19.__class__.__name__)
        if i < 11:
            teamname += "left"
        else:
            teamname += "right"
        player19s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player19s[i].start()

    player19s[15].m_debugLv19 = True

    print("試合登録完了")
