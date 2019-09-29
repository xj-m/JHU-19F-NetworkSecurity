import time
from playground.network.packet import PacketType
from Packets_E6 import *
from escape_room_006 import EscapeRoomGame

E6_STRS = ["look mirror",
           "get hairpin",
           'unlock chest with hairpin',
           'open chest',
           'look in chest',
           'get hammer in chest',
           "hit flyingkey with hammer",
           "get key",
           "unlock door with key",
           "open door"]
# TODO: set following
UNAME = ""
TEST_UNAME = ""
ACCOUNT =""
AMOUNT = 10

# for formatting print
FL = 7
SL = 15


def printx(string):
    print(string.center(80, '-')+'\n')

class ClientCmdHandler:
    def __init__(self, transport, pkt=None):
        self.dataHandler = DataHandler(transport)
        self.cmd_num = 0
        self.pkt = pkt
        if(self.pkt != None):
            self.dataHandler.sendPkt(pkt)

    def clientRecvData(self, data):
        pkts = self.dataHandler.recvPkt(data)
        for pkt in pkts:
            self.handleClientPkt(pkt)

    def handleClientPkt(self, pkt):
        pktID = pkt.DEFINITION_IDENTIFIER
        # respond to auto grade submit pkt
        if pktID == "20194.exercise6.autogradesubmitresponse":
            self.sendGameInitRequestPkt()
        
        # respond to game payment request pkt
        elif pktID == "exercise7.gamepaymentrequest":
            # TODO: check if this syntax works
            id, account, amount = process_game_require_pay_packet(pkt)
            self.sendGamePaymentResponsePkt(id,account,amount)
        
        elif pktID == "exercise7.gameresponse":
            # respond to game response 
            cmd = pkt.response()
            if self.cmd_num != 6:
                self.sendGameCmdPkt()
            elif self.cmd_num == 6:
                if(cmd.split(' ')[-1] == 'wall'):
                    self.sendGameCmdPkt()
        else:
            printx("unknown pkt recived:" + pktID)

    def sendGameInitRequestPkt():
        pkt = create_game_init_packet(TEST_UNAME)
        self.dataHandler.sendPkt(pkt)

    def sendGamePaymentResponsePkt(id,account,amount):
        if(amount > 10):
            printx("the amount is "+amount+", which is over 10, so stop the process")
            return
        receipt, receipt_sig = self.bankTransfer(id, account, amount)
        if(receipt = None or receipt_sig = None):
            printx("the bank transaction didn't complete, so the process stopped")
            return
        pkt = create_game_pay_packet(receipt, receipt_sig)
        self.dataHandler.sendPkt(pkt)

    # TODO:
    def bankTransfer(id,account,amount):
        receipt = None
        receipt_sig = None
        return (receipt,receipt_sig)

    def sendGameCmdPkt(self):
        if self.cmd_num + 1 > len(E6_STRS):
            return
        self.dataHandler.sendPkt(GameCommandPacket(
            cmd=E6_STRS[self.cmd_num]))
        self.cmd_num += 1

class ServerCmdHandler:
    def __init__(self, transport):
        self.dataHandler = DataHandler(transport)
        self.cmd_num = 0
        self.game = EscapeRoomGame(output=self.sendGameResPkt)
        self.game.create_game()
        self.game.start()
        self.payStatus = False

    def serverRecvData(self, data):
        pkts = self.dataHandler.recvPkt(data)
        for pkt in pkts:
            self.handleServerPkt(pkt)
        if self.game.status != "playing":
            self.payStatus = False
            printx('Student server side finished!')

    def handleServerPkt(self, pkt):
        pktID = pkt.DEFINITION_IDENTIFIER
        # respond to game init pkt
        if pktID == "exercise7.gameinit":
            self.sendGamePaymentRequestPkt()

        # respond to game payment response pkt
        elif pktID == "exercise7.gamepaymentresponse":
            receipt,receipt_sig = process_game_pay_packet(pkt)
            if(self.checkPayment(receipt,receipt_sig)):
                printx("payment confirmed")
                self.payStatus = True
            else:
                printx("payment confirm failed")

        elif pktID == "exercise7.gamecommand":
            if self.payStatus:
                self.game.command(pkt.command())
                time.sleep(0.25)
            else:
                printx("client try to play game before the payment is confirmed!")

        else:
            printx("unknown pkt:" + pktID)

    def sendGamePaymentRequestPkt():
        pkt = create_game_require_pay_packet(UNAME,ACCOUNT, AMOUNT)
        self.dataHandler.sendPkt(pkt)

    def checkPayment(receipt,receipt_sig):
        # TODO: complete this func
        return False
    

    def sendGameResPkt(self, string):
        pkt = create_game_response(res=string, sta=self.game.status)
        self.dataHandler.sendPkt(pkt)

class DataHandler:
    def __init__(self, transport):
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

    def printSent(self, string):
        print("sent:".ljust(FL)+string)

    def printRecv(self, string):
        print('recv:'.ljust(FL)+string)

    def printPkt(self, pkt):
        for field in pkt.FIELDS:
            fName = field[0]
            print("".ljust(FL)+fName.ljust(SL) +
                  str(pkt._fields[fName]._data))
        print('\n')
