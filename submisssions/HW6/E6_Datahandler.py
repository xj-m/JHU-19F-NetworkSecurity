from playground.network.packet import PacketType
FirstLjust = 6
SecondLjust = 15


class DataHandler:
    def __init__(self, transport):
        self.t = transport
        self.deserializer = PacketType.Deserializer()

    def sendInStr(self, string):
        # process, send, print a string
        # if string_to_send == None:
        #     return
        data = string+"<EOL>\n"
        data_as_byte = data.encode()
        self.t.write(data_as_byte)
        self.printSent(string)

    def recvInStr(self, data):
        # parse and print a date
        data_as_string = data.decode()
        lines = data_as_string.split('<EOL>\n')
        cmds = []
        for line in lines:
            self.printRecv(line)
            cmds.append(line)
        return cmds

    def sendInPkt(self, pkt):
        pktBytes = pkt.__serialize__()
        self.t.write(pktBytes)
        self.printSent(pkt.DEFINITION_IDENTIFIER)
        self.printPkt(pkt)

    def recvInPkt(self, data):
        self.deserializer.update(data)
        pkts = []
        for pkt in self.deserializer.nextPackets():
            self.printRecv(pkt.DEFINITION_IDENTIFIER)
            self.printPkt(pkt)
            pkts.append(pkt)
        return pkts
        # self.printRecv(pkg)

    def send0(self):
        self.t.write(b"<EOL>\n")
        print("sent:".ljust(10)+"a EOL cmd\n")

    def printSent(self, string):
        print("sent:".ljust(FirstLjust)+string+'\n')

    def printRecv(self, string):
        print('recv:'.ljust(FirstLjust)+string+'\n')

    def printPkt(self, pkt):
        for field in pkt.FIELDS:
            fName = field[0]
            print("".ljust(FirstLjust)+fName.ljust(SecondLjust) +
                  str(pkt._fields[fName]._data))
        print('\n')
