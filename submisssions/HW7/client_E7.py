import asyncio
import playground
import sys

from autograder_ex6_packets import *
from cmdHandler_E7 import ClientCmdHandler, printx
# from playground.common.logging import EnablePresetLogging, PRESET_DEBUG
# EnablePresetLogging(PRESET_DEBUG)


def getFirstPkt():
    pkt = AutogradeStartTest(
        name="xiangjun", email="xjm@jhu.edu", team=2, port=1109)
    with open("Packets_E6.py", "rb") as f:
        pkt.packet_file = f.read()
    return pkt

# TODO: set test id
def getCheckResPkt():
    return AutogradeResultRequest(
        test_id="")


# set the pkt that will send right after connection made
Check_result_mode = True
firstPkt = getCheckResPkt() if Check_result_mode else getFirstPkt()


class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop, firstPkt=None):
        self.loop = loop
        self.firstPkt = firstPkt

    def connection_made(self, transport):
        printx("Connection made!")
        self.transport = transport
        self.cmdHandler = ClientCmdHandler(transport, self.firstPkt)
        # send init pkt

    def data_received(self, data):
        self.cmdHandler.clientRecvData(data)

    def connection_lost(self, exc):
        printx('The server closed the connction')
        printx('Stop the event loop')
        self.loop.stop()


def main(args):
    loop = asyncio.get_event_loop()
    coro = playground.create_connection(lambda: ClientProtocol(loop=loop, firstPkt=firstPkt),
                                        "20194.0.0.19000", 19006)  # for E5
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main(sys.argv[1:])
