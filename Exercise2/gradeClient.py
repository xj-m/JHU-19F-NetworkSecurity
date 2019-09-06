import socket
import time

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
            print("received:"+line)
            msg_list.append(line)

s = socket.socket()
host ="192.168.200.52"
port = 19002
s.connect((host,port))
print("success connnect")
msgHandler = msgHandler(s)

msgHandler.recv()
name = "xiangjunTest"
msgHandler.send(name)

escape_strings = ["look mirror", "get hairpin", "unlock door with hairpin", "open door"]
for escape_string in escape_strings:
    msgHandler.send(escape_string)
    time.sleep(0.25)
    msgHandler.recv()



