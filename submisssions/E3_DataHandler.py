class DataHandler:
    def __init__(self, transport):
        self.t = transport

    def send(self, string_to_send):
        # process, send, print a string
        if string_to_send == None:
            return
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