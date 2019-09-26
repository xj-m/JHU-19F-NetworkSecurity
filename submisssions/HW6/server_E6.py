import asyncio
import playground
import time
import sys
from cmdHandler_E6 import ServerCmdHandler, printx
from playground.common.logging import EnablePresetLogging, PRESET_VERBOSE
EnablePresetLogging(PRESET_VERBOSE)

PORT_NUM = 1109


class ServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        printx('Connection made')
        self.transport = transport  # NOTE: why this line have to exist?
        self.cmdHandler = ServerCmdHandler(transport)

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(asyncio.wait(
            [asyncio.ensure_future(a) for a in self.cmdHandler.game.agents]))

    def data_received(self, data):
        self.cmdHandler.serverRecvData(data)


def main(args):
    loop = asyncio.get_event_loop()
    coro = playground.create_server(
        ServerProtocol, "localhost", PORT_NUM)  # for E5
    server = loop.run_until_complete(coro)

    printx('Servering on{}'.format(server.sockets[0].getsockname()))
    # loop.set_debug(1)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    main(sys.argv[1:])
