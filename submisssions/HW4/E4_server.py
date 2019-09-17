import asyncio
import time
import sys
from escape_room_004 import EscapeRoomGame
from E4_Datahandler import DataHandler


def printx(string):
    print(string.center(80, '-')+'\n')


class ServerProtocol(asyncio.Protocol):
    def connection_made(self, tranport):
        printx('Connection made')
        self.dataHandler = DataHandler(tranport)
        self.game = EscapeRoomGame(output=self.dataHandler.send)
        self.game.create_game()
        self.game.start()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(asyncio.wait(
            [asyncio.ensure_future(a) for a in self.game.agents]))

    def data_received(self, data):
        cmds = self.dataHandler.recv(data)
        for cmd in cmds:
            self.dataHandler.send(self.game.command(cmd))
            time.sleep(0.25)
        if self.game.status != "playing":
            printx('Student server side finished!')


def main(args):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ServerProtocol, '', 1109)
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
