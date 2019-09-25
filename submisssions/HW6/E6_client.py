import asyncio
import playground
import sys
from autograder_ex6_packets import *
from playground.network.packet import PacketType

from my_packet import *
from E6_Datahandler import DataHandler
from E6_cmdHandler import *
# from playground.common.logging import EnablePresetLogging, PRESET_DEBUG
# EnablePresetLogging(PRESET_DEBUG)

PORT_NUM_STUDENT = 1107
E3_ESCAPE_STRING1 = ['SUBMIT,Xiangjun,xjm@jhu.edu,2,'+str(PORT_NUM_STUDENT), "look mirror", "get hairpin",
                     'unlock chest with hairpin', 'open chest', 'look in chest', 'get hammer in chest', "hit flyingkey with hammer", "get key",
                     "unlock door with key", "open door"]


def printx(string):
    print(string.center(80, '-')+'\n')


class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop, message=None):
        self.loop = loop
        self.cmd_num = 0
        self.message = message

    def connection_made(self, transport):

        printx("Connection made!")
        self.transport = transport
        self.dataHandler = DataHandler(transport)

        packet1 = AutogradeStartTest(
            name="xiangjun", email="xjm@jhu.edu", team=2, port=1107)
        with open("HW6/my_packet.py", "rb") as f:
            packet1.packet_file = f.read()
        self.dataHandler.sendInPkt(packet1)

    def data_received(self, data):
        pkts = self.dataHandler.recvInPkt(data)
        for pkt in pkts:
            self.pktCmdHandler(pkt)

    def connection_lost(self, exc):
        printx('The server closed the connction')
        printx('Stop the event loop')
        self.loop.stop()

    def pktCmdHandler(self, pkt):

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
            return

    def sendCmd(self):
        if self.cmd_num + 1 > len(E3_ESCAPE_STRING1):
            return
        self.dataHandler.sendInPkt(GameCommandPacket(
            cmd=E3_ESCAPE_STRING1[self.cmd_num]))
        self.cmd_num += 1

    def cmdHandler(self, cmd):
        first_word_cmd = cmd.split(' ')[0]
        if self.cmd_num+1 <= len(E3_ESCAPE_STRING1) and self.cmd_num != 6:
            self.dataHandler.sendInStr(
                E3_ESCAPE_STRING1[self.cmd_num])
            self.cmd_num += 1
            return
        elif self.cmd_num == 6:
            if(cmd.split(' ')[-1] == "wall"):
                self.dataHandler.sendInStr(E3_ESCAPE_STRING1[self.cmd_num])
                self.cmd_num += 1
        elif first_word_cmd == 'CLIENT':
            printx('Received client test ok')
            return


def main(args):
    loop = asyncio.get_event_loop()
    loop.set_debug(1)
    coro = playground.create_connection(lambda: ClientProtocol(loop=loop),
                                        "20194.0.0.19000", 19006)  # for E5
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main(sys.argv[1:])
