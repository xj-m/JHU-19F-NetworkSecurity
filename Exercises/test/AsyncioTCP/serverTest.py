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

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername).center(50,'-'))
        self.transport = transport
        self.msgHandler = MsgHandler(self.transport)

    def data_received(self, data):
        lines = self.msgHandler.recv(data)
        for line in lines:
            self.msgHandler.send(line)

loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 8888)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()).center(50,'-'))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()