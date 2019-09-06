# Import socket module 
import socket                
  
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 12345                
  
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
print("success connect")
  
while True:
    s.send((input(">> ")).encode())
    data = s.recv(1024) # this could be multiple messages
    data_as_string = data.decode() # convert from bytes to string
    lines = data_as_string.split("\n")
    for line in lines:
        print (line)
    
# receive data from the server 

# close the connection 
s.close()  