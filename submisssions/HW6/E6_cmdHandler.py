from HW6.my_packet import *
from HW6.E6_Datahandler import *
PORT_NUM_STUDENT = 1107

E6_STR = ['SUBMIT,Xiangjun,xjm@jhu.edu,2,'+str(PORT_NUM_STUDENT), "look mirror", "get hairpin",
          'unlock chest with hairpin', 'open chest', 'look in chest', 'get hammer in chest', "hit flyingkey with hammer", "get key",
          "unlock door with key", "open door"]


def printx(string):
    print(string.center(80, '-')+'\n')


class PktCmdHandler:
    def __init__(self, transport, game=None):
        self.dataHandler = DataHandler(transport)
        self.cmd_num = 0
        self.game = game

    def clientRecvData(data):
        pkts = self.dataHandler.recvInPkt(data)
        for pkt in pkts:
            self.handleClientPkt(pkt)
        if self.game.status != "playing":
            print

    def serverRecvData(data):
        pkts = self.dataHandler.recvInPkt(data)
        for pkt in pkts:
            self.handleServerPkt(pkt)
        if self.game.status != "playing":
            printx('Student server side finished!')

    def handleServerPkt(self, pkt):
        res = self.game.command(pkt.command())
        sta = self.game.status
        pkt = GameResponsePacket(res, sta)
        self.dataHandler.sendInPkt(pkt)
        time.sleep(0.25)

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
