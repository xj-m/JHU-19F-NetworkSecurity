import time
from playground.network.packet import PacketType
from my_packet import *
from escape_room_006 import EscapeRoomGame

E6_STR = ["look mirror", "get hairpin",
          'unlock chest with hairpin', 'open chest', 'look in chest', 'get hammer in chest', "hit flyingkey with hammer", "get key",
          "unlock door with key", "open door"]

def printx(string):
    print(string.center(80, '-')+'\n')

class ServerCmdHandler:
    def __init__(self, transport):
        self.dataHandler = DataHandler(transport)
        self.cmd_num = 0
        self.game = EscapeRoomGame(output=self.sendGameResPkt)
        self.game.create_game()
        self.game.start()

    def serverRecvData(self, data):
        pkts = self.dataHandler.recvPkt(data)
        for pkt in pkts:
            self.handleServerPkt(pkt)
        if self.game.status != "playing":
            printx('Student server side finished!')

    def handleServerPkt(self, pkt):
        self.game.command(pkt.command())
        time.sleep(0.25)

    def sendGameResPkt(self, string):
        pkt = GameResponsePacket(res=string, sta=self.game.status)
        self.dataHandler.sendPkt(pkt)

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

class DataHandler:
    def __init__(self, transport):
        self.fl = 7
        self.sl = 15
        self.t = transport
        self.deserializer = PacketType.Deserializer()

    def sendPkt(self, pkt):
        pktBytes = pkt.__serialize__()
        self.t.write(pktBytes)
        self.printSent(pkt.DEFINITION_IDENTIFIER)
        self.printPkt(pkt)

    def recvPkt(self, data):
        self.deserializer.update(data)
        pkts = []
        for pkt in self.deserializer.nextPackets():
            self.printRecv(pkt.DEFINITION_IDENTIFIER)
            self.printPkt(pkt)
            pkts.append(pkt)
        return pkts
        # self.printRecv(pkg)

    def printSent(self, string):
        print("sent:".ljust(self.fl)+string)

    def printRecv(self, string):
        print('recv:'.ljust(self.fl)+string)

    def printPkt(self, pkt):
        for field in pkt.FIELDS:
            fName = field[0]
            print("".ljust(self.fl)+fName.ljust(self.sl) +
                  str(pkt._fields[fName]._data))
        print('\n')
