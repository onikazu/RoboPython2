import player21
import threading
from socket import *
import math


class Player22(player21.Player21, threading.Thread):
    def __init__(self):
        super(Player22, self).__init__()
        self.m_listPlayer = []
        self.m_debugLv22 = False

    def getObjectList(self, message, keyword):
        list = []
        index0 = message.find(keyword)
        while index0 > -1:
            index1 = message.find(")", index0 + 2)
            index2 = message.find(")", index1 + 1)
            strObject = message[index0:index2 + 1]
            player = self.getObjectMessage_1(strObject)
            list.append(player)
            index0 = message.find(keyword, index2)
        return list

    def getObjectMessage_1(self, obj):
        t = self.m_iTime
        dist = 0
        dir = 0
        dist_change = 0
        dir_change = 0
        neck = 0
        body = 0
        index0 = obj.find(") ")
        index1 = obj.find(")", index0 + 1)
        result = ""
        # 教科書変更点
        name = obj[0:index1 + 2]
        # 教科書変更点
        index2 = name.find(" ")
        index3 = name.find(" ", index2 + 1)
        index4 = name.find(")")
        s = "((player " + self.m_strTeamName
        team = ""
        if name.startswith(s):
            team = "friend"
        else:
            team = "enemy"
        number = 0
        if index3 + 1 < index4 and name.find("(player") == -1 and name.find("(Player"):
            str_var = name[index3 + 1:index4]
            if str_var.find("goalie") > 0:
                str_var = str_var.replace("goalie", " ", 1)
            print("str_var:", str_var)
            number = int(float(str_var))
        str_var = obj[index0 + 1:index1]
        st = str_var.split(" ")
        count = len(st)
        if count <= 0:
            count -= 1
            dist = float(st[count])
        if count <= 0:
            count -= 1
            dir = float(st[count])
        if count <= 0:
            count -= 1
            dist_change = float(st[count])
        if count <= 0:
            count -= 1
            dir_change = float(st[count])
        if count <= 0:
            count -= 1
            body = float(st[count])
        if count <= 0:
            count -= 1
            neck = float(st[count])
        rad = math.radians(self.normalizeAngle(dir + self.m_dNeck[t]))
        X = self.m_dX[t] + dist * math.cos(rad)
        Y = self.m_dY[t] + dist * math.sin(rad)
        VX = 0
        VY = 0
        count = len(st)
        if count >= 4:
            vx = dist_change
            vy = dir_change * dist * (math.pi / 180)
            R = math.sqrt(vx * vx + vy * vy)
            Deg = math.degrees(math.atan2(vy, vx))
            DegAbs = self.normalizeAngle(dir + Deg + self.m_dNeck[t])
            Rad = math.radians(DegAbs)
            vx_r = R * math.cos(Rad)
            vy_r = R * math.sin(Rad)
            VX = vx_r + self.m_dVX[t]
            VY = vy_r + self.m_dVY[t]

        BODY = self.m_dBody[t]
        NECK = self.m_dNeck[t]

        if count >= 5:
            BODY = self.normalizeAngle(BODY + self.m_dNeck[t])
        if count >= 6:
            NECK = self.normalizeAngle(NECK + self.m_dNeck[t])

        result = "("
        result += "(team " + team + ")"
        result += "(number " + str(number) + ")"
        result += "(x {0:.4f})(y {0:.4f})".format(X, Y)
        result += "(vx {0:.4f})(vy {0:.4f})".format(VX, VY)
        result += "(body {0:.4f})(neck {0:.4f})".format(BODY, NECK)
        result += ")"
        self.getParam(result, "x", 1)
        return result

    def analyzeVisualMessage(self, message):
        super().analyzeVisualMessage(message)
        t = self.m_iVisualTime
        if abs(self.m_dNeck[t]) > 180.0:
            return
        if abs(self.m_dX[t]) > 60.0:
            return
        if abs(self.m_dY[t]) > 40.0:
            return
        str_var = "((player"
        self.m_listPlayer = self.getObjectList(message, str_var)
        list1 = self.getObjectList(message, "((player")
        list2 = self.getObjectList(message, "((Player")
        self.m_listPlayer = []
        for i in range(len(list1)):
            self.m_listPlayer.append(list1[i])
        for i in range(len(list2)):
            self.m_listPlayer.append(list2[i])

        if self.m_debugLv22 and 8 < self.m_iTime < 12:
            print()
            print("背番号{}, 時刻{}".format(self.m_iNumber, self.m_iTime))
            for i in range(len(self.m_listPlayer)):
                player = str(self.m_listPlayer[i])
                print(player)

    def checkNearest_2(self, targetX, targetY):
        t = self.m_iTime
        d = self.getDistance(self.m_dX[t], self.m_dY[t], targetX, targetY)
        result = True
        s = "friend"
        if not self.m_listPlayer:
            return False

        for i in range(len(self.m_listPlayer)):
            player = str(self.m_listPlayer[i])
            x = self.getParam(player, "x", 1)
            y = self.getParam(player, "y", 1)
            if d > self.getDistance(targetX, targetY, x, y):
                if player.find(s) > -1:
                    result = False

        return result


if __name__ == "__main__":
    player22s = []
    for i in range(22):
        p22 = Player22()
        player22s.append(p22)
        teamname = str(p22.__class__.__name__)
        if i < 11:
            teamname += "left"
        else:
            teamname += "right"
        player22s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player22s[i].start()

    player22s[2].m_debugLv22 = True

    print("試合登録完了")
