from my_packet import *
from dataHandler_E6 import *
from escape_room_006 import EscapeRoomGame

E6_STR = ["look mirror", "get hairpin",
          'unlock chest with hairpin', 'open chest', 'look in chest', 'get hammer in chest', "hit flyingkey with hammer", "get key",
          "unlock door with key", "open door"]


def printx(string):
    print(string.center(80, '-')+'\n')


class ClientCmdHandler:
    def __init__(self, transport,pkt=None):
        self.dataHandler = DataHandler(transport)
        self.cmd_num = 0
        if(pkt!=None):
            self.dataHandler.sendPkt(pkt)

    def clientRecvData(self, data):
        pkts = self.dataHandler.recvPkt(data)
        for pkt in pkts:
            self.handleClientPkt(pkt)

    def handleClientPkt(self, pkt):
        if pkt.DEFINITION_IDENTIFIER == "20194.exercise6.autogradesubmitresponse":
            self.sendGameCmdPkt()

        cmd = pkt.response()
        first_word = cmd.split(' ')[0]

        if self.cmd_num != 6:
            self.sendGameCmdPkt()
        elif self.cmd_num == 6:
            if(cmd.split(' ')[-1] == 'wall'):
                self.sendGameCmdPkt()
        elif first_word == 'VICTORY!':
            printx("Received client test ok")

    def sendGameCmdPkt(self):
        if self.cmd_num + 1 > len(E6_STR):
            return
        self.dataHandler.sendPkt(GameCommandPacket(
            cmd=E6_STR[self.cmd_num]))
        self.cmd_num += 1
