import asynocio
import time
PORT_NUM_OF_SERVER = "4321"


class MsgHandler:
    def __init__(self, transport):
        self.t = transport

    def send(self, string_to_send):
        # process, send, print a string
        data = string_to_send+'<EOL>\n'
        data_as_byte = data.encode()
        self.t.write(data_as_byte)
        print("sent:".ljust(10)+string_to_send+'\n')

    def recv(self, data):
        # parse and print a data
        data_as_string = data.decode()
        lines = data_as_string.split('<EOL>\n')
        msg_list = []
        for line in lines:
            if line == "":
                continue
            print('received:'.ljust(10)+line+'\n')
            msg_list.append(line)
        return msg_list


class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        print("Connection made!".center(50, '-'))
        self.transport = transport
        self.msgHandler = MsgHandler(transport)
        self.msgHandler.send("Hello!")
        # for E3
        e3_cmd_list = ["STRING,Xiangjun,xjm@jhu.edu,2,"+PORT_NUM_OF_SERVER,
                       "look mirror", "get hairpin", "unlock door with hairpin", "open door"]
        for cmd in e3_cmd_list:
            self.msgHandler.send(cmd)
            time.sleep(0.25)

    def data_received(self, data):
        self.msgHandler.recv(data)
