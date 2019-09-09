from escape_room_001 import EscapeRoomGame,MsgHandler
import time, socket

# create socket
s = socket.socket()
host ="192.168.200.52"
port = 19002
s.connect((host,port))
print("Socket successfully created!")

msgHandler = MsgHandler(s)

# send student name
msgHandler.recv()
name = "xjmTest"
msgHandler.send(name)

# section 1
escape_strings = ["look mirror", "get hairpin", "unlock door with hairpin", "open door"]
for escape_string in escape_strings:
    msgHandler.send(escape_string)
    time.sleep(0.25)
    msgHandler.recv()
    
# section 2
game = EscapeRoomGame(msgHandler=msgHandler)
game.create_game()
game.start()
print("Game created!")
while game.status == "playing":
    lines = msgHandler.recv()
    for msg in lines:
        if msg == "":
            continue
        game.command(msg)
        time.sleep(0.25)