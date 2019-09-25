from HW6.my_packet import *
from HW6.E6_Datahandler import *
PORT_NUM_STUDENT = 1107

E6_STR = ['SUBMIT,Xiangjun,xjm@jhu.edu,2,'+str(PORT_NUM_STUDENT), "look mirror", "get hairpin",
          'unlock chest with hairpin', 'open chest', 'look in chest', 'get hammer in chest', "hit flyingkey with hammer", "get key",
          "unlock door with key", "open door"]


def printx(string):
    print(string.center(80, '-')+'\n')


class pktCmdHandler:
    def __init__(self, transport):
        self.dataHandler = DataHandler(transport)
        self.cmd_num = 0

    def clientRecvData(data):
        pkts = self.dataHandler.recvInPkt(data)
        for pkt in pkts:
            self.handleClientPkt(pkt)

    def handleClientPkt(self, pkt):
        if pkt.DEFINITION_IDENTIFIER == "20194.exercise6.autogradesubmitresponse":
            self.sendCmd()

        cmd = pkt.response()
        first_word_cmd = cmd.split(' ')[0]

        if self.cmd_num != 6:
            self.sendCmd()
        elif self.cmd_num == 6:
            if(cmd.split(' ')[-1] == 'wall'):
                self.sendCmd()
        elif first_word_cmd == 'VICTORY!':
            printx("Received client test ok")

    def sendCmd(self):
        if self.cmd_num + 1 > len(E6_STR):
            return
        self.dataHandler.sendInPkt(GameCommandPacket(
            cmd=E6_STR[self.cmd_num]))
        self.cmd_num += 1
