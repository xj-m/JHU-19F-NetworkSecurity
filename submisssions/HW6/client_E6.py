import asyncio
import playground
import sys
from autograder_ex6_packets import *

from my_packet import *
from clientCmdHandler_E6 import *
# from playground.common.logging import EnablePresetLogging, PRESET_DEBUG
# EnablePresetLogging(PRESET_DEBUG)


class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop, message=None):
        self.loop = loop
        self.message = message

    def connection_made(self, transport):
        printx("Connection made!")
        self.transport = transport
        self.cmdHandler = ClientCmdHandler(transport)

        # send init pkt
        packet1 = AutogradeStartTest(
            name="xiangjun", email="xjm@jhu.edu", team=2, port=1109)
        with open("my_packet.py", "rb") as f:
            packet1.packet_file = f.read()
        self.cmdHandler.dataHandler.sendPkt(packet1)

    def data_received(self, data):
        self.cmdHandler.clientRecvData(data)

    def connection_lost(self, exc):
        printx('The server closed the connction')
        printx('Stop the event loop')
        self.loop.stop()


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
