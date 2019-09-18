import asyncio
import playground
import sys
from E5_Datahandler import DataHandler

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

        self.dataHandler.send0()
        # self.transport.write(b"<EOL>\n")

        if self.message != None:
            self.dataHandler.send(self.message)

    def data_received(self, data):
        cmds = self.dataHandler.recv(data)
        for cmd in cmds:
            self.cmdHandler(cmd)

    def connection_lost(self, exc):
        printx('The server closed the connction')
        printx('Stop the event loop')
        self.loop.stop()

    def cmdHandler(self, cmd):
        first_word_cmd = cmd.split(' ')[0]
        if self.cmd_num+1 <= len(E3_ESCAPE_STRING1) and self.cmd_num != 6:
            self.dataHandler.send(
                E3_ESCAPE_STRING1[self.cmd_num])
            self.cmd_num += 1
            return
        elif self.cmd_num == 6:
            if(cmd.split(' ')[-1] == "wall"):
                self.dataHandler.send(E3_ESCAPE_STRING1[self.cmd_num])
                self.cmd_num += 1
        elif first_word_cmd == 'CLIENT':
            printx('Received client test ok')
            return


def main(args):
    loop = asyncio.get_event_loop()
    # loop.set_debug(1)
    coro = playground.create_connection(lambda: ClientProtocol(loop=loop),
                                        "20194.0.0.19000", 19005)  # for E5
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main(sys.argv[1:])
