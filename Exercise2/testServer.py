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
            # NOTE: cant get rid of this
            if line == "":
                continue
            print("received:"+line)
            msg_list.append(line)

s = socket.socket()
port = 12345
s.bind(('',port))
print("binded")
s.listen(5)
print("listen")

c, addr = s.accept()
msgHandler = msgHandler(c)
i = 1
while True:
    msgHandler.recv()
    msgHandler.send("thank you"+str(i))
    i= i+1
