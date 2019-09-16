import asyncio, time, sys
from escape_room_001 import EscapeRoomGame
from E3_DataHandler import DataHandler
from formatter import *

class ServerProtocol(asyncio.Protocol):
    def connection_made(self, tranport):
        print_announce('Connection made')
        self.dataHandler = DataHandler(tranport)
        self.game = EscapeRoomGame(output=self.dataHandler.send)
        self.game.create_game()
        self.game.start()

    def data_received(self,data):
        cmds = self.dataHandler.recv(data)
        for cmd in cmds:
            self.dataHandler.send(self.game.command(cmd))
            time.sleep(0.25)
        if self.game.status !="playing":
            print_announce('Student server side finished!')

def main(args):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ServerProtocol, '',1109)
    server = loop.run_until_complete(coro)

    print_announce('Servering on{}'.format(server.sockets[0].getsockname()))
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