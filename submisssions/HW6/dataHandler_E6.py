from playground.network.packet import PacketType


class DataHandler:
    def __init__(self, transport):
        self.fl = 7
        self.sl = 15
        self.t = transport
        self.deserializer = PacketType.Deserializer()

    def sendPkt(self, pkt):
        pktBytes = pkt.__serialize__()
        self.t.write(pktBytes)
        self.printSent(pkt.DEFINITION_IDENTIFIER)
        self.printPkt(pkt)

    def recvPkt(self, data):
        self.deserializer.update(data)
        pkts = []
        for pkt in self.deserializer.nextPackets():
            self.printRecv(pkt.DEFINITION_IDENTIFIER)
            self.printPkt(pkt)
            pkts.append(pkt)
        return pkts
        # self.printRecv(pkg)

    def printSent(self, string):
        print("sent:".ljust(self.fl)+string)

    def printRecv(self, string):
        print('recv:'.ljust(self.fl)+string)

    def printPkt(self, pkt):
        for field in pkt.FIELDS:
            fName = field[0]
            print("".ljust(self.fl)+fName.ljust(self.sl) +
                  str(pkt._fields[fName]._data))
        print('\n')
