from escape_room_001 import EscapeRoomGame
import time, socket

class MsgHandler:
    def __init__ (self, socket):
        self.s = socket
    def send(self, string_to_send):
        data = string_to_send +"<EOL>\n"
        data_as_byte = str.encode(data)
        self.s.send(data_as_byte)
        print("sent:".ljust(12)+string_to_send+'\n')
    def recv(self):
        data = self.s.recv(1024)
        data_as_string = data.decode()
        lines = data_as_string.split("<EOL>\n")
        msg_list = []
        for line in lines:
            if line == "":
                continue
            print("received:".ljust(12)+line+'\n')
            msg_list.append(line)
        return msg_list

# create socket
s = socket.socket()
host ="192.168.200.52"
port = 19002
s.connect((host,port))
print("Socket successfully created!\n")

msgHandler = MsgHandler(s)

# send student name
msgHandler.recv()
student_name = "xjmTest"
msgHandler.send(student_name)
print(("student name sent:"+student_name).center(100,'-')+'\n')

# section 1
escape_strings = ["look mirror", "get hairpin", "unlock door with hairpin", "open door"]
for escape_string in escape_strings:
    msgHandler.send(escape_string)
    time.sleep(0.25)
    msgHandler.recv()
print("section 1 finished".center(100,'-')+"\n")
    
# section 2
game = EscapeRoomGame(output=msgHandler.send)
game.create_game()
game.start()
while game.status == "playing":
    lines = msgHandler.recv()
    for msg in lines:
        if msg == "":
            continue
        game.command(msg)
        time.sleep(0.25)
print("Section 2 finished!".center(100,'-')+'\n')