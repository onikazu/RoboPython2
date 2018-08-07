import player7
import threading
from socket import *
import math


class Player8(player7.Player7, threading.Thread):
    def __init__(self):
        super(Player8, self).__init__()
        self.m_strFlagName = []
        self.m_dFlagX = []
        self.m_dFlagY = []
        self.m_debugLv08 = False
        self.m_dX = 0.0
        self.m_dY = 0.0
        self.m_dNeck = 0.0
        self.m_strFlagName.append("g r");
        self.m_dFlagX.append(52.5);
        self.m_dFlagY.append(0.0)
        self.m_strFlagName.append("g l");
        self.m_dFlagX.append(-52.5);
        self.m_dFlagY.append(0.0)
        self.m_strFlagName.append("f c t");
        self.m_dFlagX.append(0.0);
        self.m_dFlagY.append(-34.0)
        self.m_strFlagName.append("f c b");
        self.m_dFlagX.append(0.0);
        self.m_dFlagY.append(+34.0)
        self.m_strFlagName.append("f c");
        self.m_dFlagX.append(0.0);
        self.m_dFlagY.append(0.0)
        self.m_strFlagName.append("f p l t");
        self.m_dFlagX.append(-36.0);
        self.m_dFlagY.append(-20.16)
        self.m_strFlagName.append("f p l b");
        self.m_dFlagX.append(-36.0);
        self.m_dFlagY.append(20.16)
        self.m_strFlagName.append("f p l c");
        self.m_dFlagX.append(-36.0);
        self.m_dFlagY.append(0.0)
        self.m_strFlagName.append("f p r t");
        self.m_dFlagX.append(36.0);
        self.m_dFlagY.append(-20.16)
        self.m_strFlagName.append("f p r b");
        self.m_dFlagX.append(36.0);
        self.m_dFlagY.append(20.16)
        self.m_strFlagName.append("f p r c");
        self.m_dFlagX.append(36.0);
        self.m_dFlagY.append(0.0)
        self.m_strFlagName.append("f g l t");
        self.m_dFlagX.append(-52.5);
        self.m_dFlagY.append(-7.01)
        self.m_strFlagName.append("f g l b");
        self.m_dFlagX.append(-52.5);
        self.m_dFlagY.append(7.01)
        self.m_strFlagName.append("f g r t");
        self.m_dFlagX.append(52.5);
        self.m_dFlagY.append(-7.01)
        self.m_strFlagName.append("f g r b");
        self.m_dFlagX.append(52.5);
        self.m_dFlagY.append(7.01)
        self.m_strFlagName.append("f t l 50)");
        self.m_dFlagX.append(-50.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t l 40");
        self.m_dFlagX.append(-40.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t l 30");
        self.m_dFlagX.append(-30.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t l 20");
        self.m_dFlagX.append(-20.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t l 10");
        self.m_dFlagX.append(-10.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t 0");
        self.m_dFlagX.append(0.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t r 10");
        self.m_dFlagX.append(10.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t r 20");
        self.m_dFlagX.append(20.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t r 30");
        self.m_dFlagX.append(30.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t r 40");
        self.m_dFlagX.append(40.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t r 50");
        self.m_dFlagX.append(50.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f b l 50");
        self.m_dFlagX.append(-50.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b l 40");
        self.m_dFlagX.append(-40.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b l 30");
        self.m_dFlagX.append(-30.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b l 20");
        self.m_dFlagX.append(-20.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b l 10");
        self.m_dFlagX.append(-10.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b 0");
        self.m_dFlagX.append(0.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b r 10");
        self.m_dFlagX.append(10.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b r 20");
        self.m_dFlagX.append(20.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b r 30");
        self.m_dFlagX.append(30.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b r 40");
        self.m_dFlagX.append(40.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b r 50");
        self.m_dFlagX.append(50.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f l t 30");
        self.m_dFlagX.append(-57.5);
        self.m_dFlagY.append(-30.0)
        self.m_strFlagName.append("f l t 20");
        self.m_dFlagX.append(-57.5);
        self.m_dFlagY.append(-20.0)
        self.m_strFlagName.append("f l t 10");
        self.m_dFlagX.append(-57.5);
        self.m_dFlagY.append(-10.0)
        self.m_strFlagName.append("f l 0");
        self.m_dFlagX.append(-57.5);
        self.m_dFlagY.append(0.0)
        self.m_strFlagName.append("f l b 10");
        self.m_dFlagX.append(-57.5);
        self.m_dFlagY.append(10.0)
        self.m_strFlagName.append("f l b 20");
        self.m_dFlagX.append(-57.5);
        self.m_dFlagY.append(20.0)
        self.m_strFlagName.append("f l b 30");
        self.m_dFlagX.append(-57.5);
        self.m_dFlagY.append(30.0)
        self.m_strFlagName.append("f r t 30");
        self.m_dFlagX.append(57.5);
        self.m_dFlagY.append(-30.0)
        self.m_strFlagName.append("f r t 20");
        self.m_dFlagX.append(57.5);
        self.m_dFlagY.append(-20.0)
        self.m_strFlagName.append("f r t 10");
        self.m_dFlagX.append(57.5);
        self.m_dFlagY.append(-10.0)
        self.m_strFlagName.append("f r 0");
        self.m_dFlagX.append(57.5);
        self.m_dFlagY.append(0.0)
        self.m_strFlagName.append("f r b 10");
        self.m_dFlagX.append(57.5);
        self.m_dFlagY.append(10.0)
        self.m_strFlagName.append("f r b 20");
        self.m_dFlagX.append(57.5);
        self.m_dFlagY.append(20.0)
        self.m_strFlagName.append("f r b 30");
        self.m_dFlagX.append(57.5);
        self.m_dFlagY.append(30.0)
        self.m_strFlagName.append("f l t");
        self.m_dFlagX.append(-52.5);
        self.m_dFlagY.append(-34.0)
        self.m_strFlagName.append("f l b");
        self.m_dFlagX.append(-52.5);
        self.m_dFlagY.append(34.0)
        self.m_strFlagName.append("f r t");
        self.m_dFlagX.append(52.5);
        self.m_dFlagY.append(-34.0)
        self.m_strFlagName.append("f r b");
        self.m_dFlagX.append(52.5);
        self.m_dFlagY.append(34.0)

    # おそらくいらないが・・・
    def getLandMarker(self, message, playerX, playerY):
        message = message.replace("B", "b", 1)
        if message.find("(F)") > -1:
            name = "(F)"
            min_dist = self.OUT_OF_RANGE
            for i in range(2, 55):
                dist = self.getDistance(playerX, playerY, self.m_dFlagX[i], self.m_dFlagY[i])
                if min_dist > dist:
                    min_dist = dist
                    name = self.m_strFlagName[i]
            message = message.replace("F", name, 1)

        if message.find("(G)") > -1:
            name = "(G)"
            min_dist = self.OUT_OF_RANGE
            for i in range(2):
                dist = self.getDistance(playerX, playerY, self.m_dFlagX[i], self.m_dFlagY[i])
                if min_dist > dist:
                    min_dist = dist
                    name = self.m_strFlagName[i]
            message = message.replace("G", name)

        return message


    def getDistance(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        return math.sqrt(dx * dx + dy * dy)

    # メッセージに大文字が含まれていないために、省略（バージョンの仕様？？）
    # def getLandMarker(self, message, playerX, playerY):
    #     pass

    # 返り値は辞書型になっている。教科書と違うので注意
    def estimatePosition(self, message, neckDir, playerX, playerY):
        result = {"x": 999, "y": 999}
        message = self.getLandMarker(message, playerX, playerY)

        flag = self.getObjectMessage(message, "((g") + \
               self.getObjectMessage(message, "((f")
        index0 = flag.find("((")
        X = Y = W = S = 0.0
        flags = 0
        while index0 > -1:
            index1 = flag.find(")", index0 + 2)
            index2 = flag.find(")", index1 + 1)
            name = flag[index0 + 2:index1]
            # print("name", name)
            j = 0
            while self.m_strFlagName[j].endswith(name) is False:
                j += 1
            dist = self.getParam(flag, name, 1)
            dir = self.getParam(flag, name, 2)
            rad = math.radians(self.normalizeAngle(dir + neckDir))
            W = 1 / dist
            X += W * (self.m_dFlagX[j] - dist * math.cos(rad))
            Y += W * (self.m_dFlagY[j] - dist * math.sin(rad))
            S += W
            flags += 1
            index0 = flag.find("((", index0 + 2)

        if flags > 0:
            result["x"] = X / S
            result["y"] = Y / S

        if self.m_debugLv08:
            print("X={0:.4f}, Y={1:.4f}".format(result["x"],result["y"]))

        return result

    # @override
    def analyzeVisualMessage(self, message):
        time = int(self.getParam(message, "see", 1))
        if time < 1:
            return
        self.m_dNeck = self.getNeckDir(message)
        if self.m_dNeck == self.OUT_OF_RANGE:
            return
        if self.checkInitialMode():
            self.m_dX = self.m_dKickOffX
            self.m_dY = self.m_dKickOffY

        pos = self.estimatePosition(message, self.m_dNeck, self.m_dX, self.m_dY)
        self.m_dX = pos["x"]
        self.m_dY = pos["y"]


if __name__ == "__main__":
    player8s = []
    for i in range(11):
        p8 = Player8()
        player8s.append(p8)
        teamname = "p8s"
        player8s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player8s[i].start()
    player7s = []
    for i in range(11):
        p7 = player7.Player7()
        player7s.append(p7)
        teamname = "p7s"
        player7s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player7s[i].start()

    print("試合登録完了")
