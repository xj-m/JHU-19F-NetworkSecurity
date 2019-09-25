from my_packet import *
from dataHandler_E6 import *
import time
from escape_room_006 import EscapeRoomGame



def printx(string):
    print(string.center(80, '-')+'\n')


class PktCmdHandler:
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
