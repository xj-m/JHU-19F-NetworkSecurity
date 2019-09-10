import asyncio, time
from escape_room_001 import EscapeRoomGame
from E3_DataHandler import DataHandler

class ServerProtocol(asyncio.Protocol):
    def connection_made(self, tranport):
        print('Connection made'.center(100,'-')+'\n')
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
            print('Student server side finished!'.center(100,'-')+'\n')

loop = asyncio.get_event_loop()
coro = loop.create_server(ServerProtocol, '',4321)
server = loop.run_until_complete(coro)

print('Servering on{}'.format(server.sockets[0].getsockname()).center(100,'-'))
loop.set_debug(1)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

        

