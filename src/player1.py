from socket import *
import threading


class Player1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.HOSTNAME = "localhost"
        self.PORT = 6000
        self.ADDRESS = gethostbyname(self.HOSTNAME)
        self.m_strPlayMode = ""
        self.m_iNumber = 0
        self.m_strTeamName = ""
        self.m_strHostName = ""
        self.m_strSide = ""
        self.m_debugLv01 = False

    def send(self, command):
        if len(command) == 0:
            return
        # print("p1command No", self.m_iNumber, command)
        to_byte_command = command.encode(encoding='utf_8')
        self.socket.sendto(to_byte_command, (self.ADDRESS, self.PORT))
        # print("sending ", command, " is done")

    def receive(self):
        message, arr = self.socket.recvfrom(4096)
        message = message.decode("UTF-8")
        # print("メッセージ（サーバーから", self.m_iNumber, "番）：", message)
        return message

    def initialize(self, number, team_name, server_name, server_port):
        self.m_iNumber = number
        self.m_strTeamName = team_name
        self.m_strHostName = server_name
        if self.m_iNumber == 1:
            command = "(init " + self.m_strTeamName + "(goalie))"
        else:
            command = "(init " + self.m_strTeamName + ")"
        self.send(command)

    # thread を動かしている最中に行われる関数
    def run(self):
        while True:
            message = self.receive()
            # print(message)
            self.analyzeMessage(message)

    def analyzeInitialMessage(self, message):
        index0 = message.index(" ")
        index1 = message.index(" ", index0 + 1)
        index2 = message.index(" ", index1 + 1)
        index3 = message.index(")", index2 + 1)

        self.m_strSide = message[index0+1:index1]
        self.m_iNumber = int(message[index1+1:index2])
        self.m_strPlayMode = message[index2+1:index3]

    def analyzeMessage(self, message):
        if isinstance(message, type(None)):
            return
            # print(message)
        elif message.startswith("(init"):
            self.analyzeInitialMessage(message)
        elif message.startswith("(warning") or message.startswith("(error"):
            print("Something is wrong when analyzeMessage: ", message)


if __name__ == "__main__":
    players = []
    for i in range(11):
        p = Player1()
        players.append(p)
        players[i].initialize(i+1, "kazu", "localhost", 6000)
        players[i].start()

    players[0].m_debugLv01 = True
    print("試合登録完了")
