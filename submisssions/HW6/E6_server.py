import asyncio
import playground
import time
import sys
from escape_room_006 import EscapeRoomGame
from HW6.E6_cmdHandler import *


def printx(string):
    print(string.center(80, '-')+'\n')


class ServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        # NOTE: why this line have to exist?
        self.transport = transport
        printx('Connection made')

        game = EscapeRoomGame(output=self.dataHandler.send)
        game.create_game()
        game.start()

        self.cmdHandler = PktCmdHandler(transport, game)
        self.cmdHandler.dataHandler.send('hi')

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(asyncio.wait(
            [asyncio.ensure_future(a) for a in self.game.agents]))

    def data_received(self, data):
        self.cmdHandler.serverRecvData(data)


def main(args):
    loop = asyncio.get_event_loop()
    coro = playground.create_server(
        ServerProtocol, "localhost", 1107)  # for E5
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
