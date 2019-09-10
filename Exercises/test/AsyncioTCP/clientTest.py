import asyncio

class MsgHandler:
    def __init__ (self, transport):
        self.t = transport
    def send(self, string_to_send):
        data = string_to_send +"<EOL>\n"
        data_as_byte = str.encode(data)
        self.t.write(data_as_byte)
        print("sent:".ljust(12)+string_to_send+'\n')
    def recv(self, data):
        data_as_string = data.decode()
        lines = data_as_string.split("<EOL>\n")
        msg_list = []
        for line in lines:
            if line == "":
                continue
            print("received:".ljust(12)+line+'\n')
            msg_list.append(line)
        return msg_list

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        print("connection make!".center(50,"-"))
        self.transport = transport
        self.msgHandler = MsgHandler(self.transport)
        self.msgHandler.send('Hello World')

    def data_received(self, data):
        self.msgHandler.recv(data)
        self.msgHandler.send(input(">> "))

    def connection_lost(self, exc):
        print('The server closed the connection'.center(50,'-'))
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()
message = 'Hello World!'
coro = loop.create_connection(lambda: EchoClientProtocol(message, loop),
                              '127.0.0.1', 8888)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()