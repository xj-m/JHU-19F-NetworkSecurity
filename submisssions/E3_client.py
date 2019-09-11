import asyncio,sys
from E3_DataHandler import DataHandler
from formatter import *

PORT_NUM_STUDENT = 1109
E3_STUDENT_CLIENT_SEND_STRINGS = ['SUBMIT,Xiangjun,xjm@jhu.edu,2,'+str(PORT_NUM_STUDENT), "look mirror", "get hairpin",
                                  'unlock chest with hairpin', 'open chest', 'look in chest', 'get hammer in chest', "unlock door with hairpin", "open door"]

E3_STUDENT_CLIENT_SEND_STRINGS_2 = ['RESULT,f5c4d25c919834fa6766d13f4457d1cd9390b4f112c8b8876b863052eb20848c']

class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop,message=None):
        self.loop = loop
        self.num_of_cmd = 0
        self.message = message

    def connection_made(self, transport):
        print_announce("Connection made!")
        self.dataHandler = DataHandler(transport)
        if self.message != None:
            self.dataHandler.send(self.message)

    def data_received(self, data):
        cmds = self.dataHandler.recv(data)
        for cmd in cmds:
            self.cmdHandler(cmd)

    def connection_lost(self, exc):
        print_announce('The server closed the connction')
        print_announce('Stop the event loop')
        self.loop.stop()

    def cmdHandler(self, cmd):
        first_word_cmd = cmd.split(' ')[0]
        if self.num_of_cmd+1 <= len(E3_STUDENT_CLIENT_SEND_STRINGS):
            self.dataHandler.send(E3_STUDENT_CLIENT_SEND_STRINGS[self.num_of_cmd])
            self.num_of_cmd+=1
            return
        elif first_word_cmd =='CLIENT':
            print_announce('Received client test ok')
            return

def main(args):
    loop = asyncio.get_event_loop()
    # loop.set_debug(1)
    coro = loop.create_connection(lambda: ClientProtocol(loop=loop),
                                "192.168.200.52", 19003)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

if __name__ == "__main__":
    main(sys.argv[1:])