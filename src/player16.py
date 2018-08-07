import player15
import threading
from socket import *
import math


class Player16(player15.Player15, threading.Thread):
    def __init__(self):
        super(Player16, self).__init__()
        self.inertia_moment = 5.0
        self.maxneckang = 90.0
        self.minneckang = -90.0
        self.m_dHeadAngle = []
        for _ in range(self.GAME_LENGTH):
            self.m_dHeadAngle.append(0.0)
        self.m_debugLv16 = False

    def analyzePhysicalMessage(self, message):
        super().analyzePhysicalMessage(message)
        # print("=============================")
        # print("PhysicalMessage:", message)
        # print("=============================")
        if self.m_dNeck[self.m_iTime] == self.OUT_OF_RANGE:
            return

        speed = self.getParam(message, "speed", 1)
        speed_angle = self.getParam(message, "speed", 2)

        # speedに第二引数はない, 困った
        # speed_angle は体の向きト速度の方向ベクトルの差
        # if speed_angle == self.OUT_OF_RANGE:
        #     return
        # print(speed_angle, "発見speedangle")
        # print("type of speed angle: ", type(speed_angle))
        # print("type of self.m_dNeck[self.m_iTime]: ", type(self.m_dNeck[self.m_iTime]))
        # print("type of self.normalizeAngle(self.m_dNeck[self.m_iTime] + speed_angle): ", type(self.normalizeAngle(self.m_dNeck[self.m_iTime] + speed_angle)))
        # print("self.m_dNeck[self.m_iTime] + speed_angle", self.m_dNeck[self.m_iTime] + speed_angle)
        # print("self.m_dNeck[self.m_iTime]", self.m_dNeck[self.m_iTime])
        # print("speed_angle",speed_angle)
        rad = self.normalizeAngle(self.m_dNeck[self.m_iTime] + speed_angle) * math.pi / 180.0
        vx = speed * math.cos(rad)
        vy = speed * math.sin(rad)
        self.m_dVX[self.m_iTime] = vx
        self.m_dVY[self.m_iTime] = vy
        head_angle = self.getParam(message, "head_angle", 1)
        # print("headangle:", head_angle)
        # if head_angle == self.OUT_OF_RANGE:
        #     return
        body_angle = self.normalizeAngle(self.m_dNeck[self.m_iTime] - head_angle)
        # print("headangle, speed2があるであろうmessage", message)
        self.m_dHeadAngle[self.m_iTime] = head_angle
        self.m_dBody[self.m_iTime] = body_angle

    def predictTurnCommand(self, i):
        next = (i + 1) % self.GAME_LENGTH
        if self.m_dNeck[i] == self.OUT_OF_RANGE:
            return
        command = self.m_strCommand[i]
        if command.startswith("(turn "):
            moment = self.getParam(command, "turn", 1)
            vx = self.m_dVX[i]
            vy = self.m_dVY[i]
            speed = math.sqrt(vx * vx + vy * vy)
            turn_angle = moment / (1 + self.inertia_moment * speed)
            self.m_dNeck[next] = self.normalizeAngle(self.m_dNeck[i] + turn_angle)
            self.m_dBody[next] = self.normalizeAngle(self.m_dBody[i] + turn_angle)
        else:
            self.m_dNeck[next] = self.m_dNeck[i]
            self.m_dBody[next] = self.m_dBody[i]
        index0 = command.find("(turn_neck")
        if index0 > -1:
            index1 = command.find(" ", index0+9)
            index2 = command.find(")", index1+1)
            angle = float(str(command[index1:index2]))
            # print("p16:angle:", angle)
            head_angle = self.normalizeAngle(self.m_dNeck[i] - self.m_dBody[i])
            if self.maxneckang < head_angle + angle:
                self.m_dNeck[next] = self.normalizeAngle(self.m_dBody[i] + self.maxneckang)
            elif self.minneckang > head_angle + angle:
                self.m_dNeck[next] = self.normalizeAngle(self.m_dBody[i] + self.minneckang)
            else:
                self.m_dNeck[next] = self.normalizeAngle(self.m_dNeck[next] + angle)

    def predict(self, start, end):
        super().predict(start, end)
        if 0 < self.m_iTime < 20 and self.m_debugLv16:
            print("時刻", self.m_iTime)
            print("start", start)
            print("end", end)
            print("スタミナ{0:.4f}".format(self.m_dStamina[self.m_iTime]))
            print("実行力{0:.4f}".format(self.m_dEffort[self.m_iTime]))
            print("回復力{0:.4f}".format(self.m_dRecovery[self.m_iTime]))
            print("位置{0:.4f}, {1:.4f}".format(self.m_dX[self.m_iTime], self.m_dY[self.m_iTime]))
            print("速度{0:.4f}, {1:.4f}".format(self.m_dVX[self.m_iTime], self.m_dVY[self.m_iTime]))
            print("首{0:.4f}".format(self.m_dNeck[self.m_iTime]))
            print("体{0:.4f}".format(self.m_dBody[self.m_iTime]))
            print("headangle", self.m_dBody[self.m_iTime])


    def analyzePlayerType(self, message):
        super().analyzePlayerType(message)
        type = self.m_strPlayerType[self.m_iPlayerType]
        self.inertia_moment = self.getParam(type, "inertia_moment", 1)

    def analyzeServerParam(self, message):
        super().analyzeServerParam(message)
        self.maxneckang = self.getParam(message, "maxneckang", 1)
        self.minneckang = self.getParam(message, "minneckang", 1)

    def play_0(self):
        super().play_0()
        if self.m_strPlayMode.startswith("kick_off"):
            command = "(turn 0)"
            if self.m_iTime == 1:
                command = "(turn 80)"
            elif self.m_iTime < 5:
                command = "(dash 100)"
            elif self.m_iTime == 5:
                command = "(turn 90)"
            elif self.m_iTime < 15:
                command = "(turn 0)(turn_neck -20)"
            elif self.m_iTime == 15:
                command = "(turn -30)(turn_neck 90)"
            elif self.m_iTime < 20:
                command = "(dash 100)"
            else:
                command = "(kick 30 45)"

            self.m_strCommand[self.m_iTime] = command


if __name__ == "__main__":
    player16s = []
    for i in range(11):
        p16 = Player16()
        player16s.append(p16)
        teamname = "p16s"
        player16s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player16s[i].start()

    player16s[0].m_debugLv16 = True

    print("試合登録完了")