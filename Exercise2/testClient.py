import socket

class msgHandler:
    def __init__ (self, socket):
        self.s = socket
    def send(self, string_to_send):
        data = string_to_send +"<EOL>\n"
        data_as_byte = str.encode(data)
        self.s.send(data_as_byte)
        print("sent:"+string_to_send)
    def recv(self):
        data = self.s.recv(1024)
        data_as_string = data.decode()
        lines = data_as_string.split("<EOL>\n")
        msg_list = []
        for line in lines:
            if line == "":
                print("end of msg")
                continue
            print("received:"+line)
            msg_list.append(line)

s = socket.socket()
host ="127.0.0.1"
port = 12345
s.connect((host,port))
print("success connnect")
msgHandler = msgHandler(s)
while True:
    msgHandler.send(input(">>"))
    msgHandler.recv()
    