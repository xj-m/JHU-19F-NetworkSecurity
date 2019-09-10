import asyncio
import time
PORT_NUM_STUDENT = 4321
PORT_NUM_OF_REMOTE_SERVER_FOR_E3 = "192.168.200.52"
HOST_NUM_OF_REMOTE_SERVER_FOR_E3 = 19003
E3_STUDENT_CLIENT_SEND_STRINGS = ['SUBMIT,Xiangjun,xjm@jhu.edu,2,'+str(PORT_NUM_STUDENT), "look mirror", "get hairpin",'unlock chest with hairpin','open chest','look in chest','get hammer in chest', "unlock door with hairpin", "open door"]


class DataHandler:
    def __init__(self,transport):
        self.t = transport

    def send(self, string_to_send):
        # process, send, print a string
        data = string_to_send+'<EOL>\n'
        data_as_byte = data.encode()
        self.t.write(data_as_byte)
        print("sent:".ljust(10)+string_to_send+'\n')

    def recv(self, data):
        # parse and print a date
        data_as_string = data.decode()
        lines = data_as_string.split('<EOL>\n')
        cmds = []
        for line in lines:
            if line == "":
                continue
            print('received:'.ljust(10)+line+'\n')
            cmds.append(line)
        return cmds


class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.num_of_cmd = 0


    def connection_made(self, transport):
        print("Connection made!".center(100, '-')+'\n')
        self.dataHandler = DataHandler(transport)

    def data_received(self, data):
        cmds = self.dataHandler.recv(data)
        for cmd in cmds:
            self.cmdHandler(cmd)
      
    def connection_lost(self, exc):
        print('The server closed the connection'.center(100,'-')+'\n')
        print('Stop the event loop'+'\n')
        self.loop.stop()

    def cmdHandler(self, cmd):
        if cmd.split(" ")[0] =="SUBMIT":
            self.dataHandler.send(E3_STUDENT_CLIENT_SEND_STRINGS[0])
        else:
            if self.num_of_cmd+1 == len(E3_STUDENT_CLIENT_SEND_STRINGS):
                return
            self.dataHandler.send(E3_STUDENT_CLIENT_SEND_STRINGS[self.num_of_cmd+1])
            self.num_of_cmd = self.num_of_cmd+1
        

loop = asyncio.get_event_loop()
loop.set_debug(1)
coro = loop.create_connection(lambda: ClientProtocol(loop),
                              "192.168.200.52", 19003)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()