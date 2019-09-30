import sys
import os
import time
import asyncio
sys.path.insert(1, '../../BitPoints-Bank-Playground3/src/')
from playground.network.packet import PacketType
from Packets_E7 import *
from escape_room_006 import EscapeRoomGame
from CipherUtil import loadCertFromFile
from OnlineBank import BankClientProtocol, OnlineBankConfig
import playground
import getpass
# insert at 1, 0 is the script path (or '' in REPL)


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
UNAME = "xma39"
PASS = ""
TEST_UNAME = ""
MY_ACCOUNT = "xma39_account"
AMOUNT = 10


# for formatting print
FL = 7
SL = 20


def printx(string):
    print(string.center(80, '-')+'\n')


class BankManager:
    def __init__(self):
        bankconfig = OnlineBankConfig()
        self.bank_addr = bankconfig.get_parameter("CLIENT", "bank_addr")
        self.bank_port = int(bankconfig.get_parameter("CLIENT", "bank_port"))
        # bank_stack = bankconfig.get_parameter("CLIENT", "stack", "default")
        self.bank_username = bankconfig.get_parameter("CLIENT", "username")
        self.certPath = os.path.join(bankconfig.path(), "20194_online_bank.cert")
        self.bank_cert = loadCertFromFile(self.certPath)
        self.bank_client = BankClientProtocol(
            self.bank_cert, self.bank_username, PASS)

    async def transfer(self, src, dst, amount, memo):

        # get bank_client
        password = getpass.getpass("Enter password for {}: ".format(self.bank_username))
        self.bank_client = BankClientProtocol(
            self.bank_cert, self.bank_username, password)

        # connect to bank port
        await playground.create_connection(
            lambda: self.bank_client,
            self.bank_addr,
            self.bank_port,
            family='default'
        )
        print("Connected. Logging in.")

        # bank_client login
        try:
            await self.bank_client.loginToServer()
        except Exception as e:
            print("Login error. {}".format(e))
            return (None, None)
        # bank_client swtch account
        try:
            await self.bank_client.switchAccount(MY_ACCOUNT)
        except Exception as e:
            print("Could not set source account as {} because {}".format(
                src,
                e))
            return (None, None)
        # get transfer result
        try:
            result = await self.bank_client.transfer(dst, amount, memo)
        except Exception as e:
            print("Could not transfer because {}".format(e))
            return (None, None)

        receipt = result.Receipt
        receipt_sig = result.ReceiptSignature
        return (receipt, receipt_sig)


class ClientCmdHandler:
    def __init__(self, transport, pkt=None):
        self.dataHandler = DataHandler(transport)
        self.cmd_num = 0
        self.pkt = pkt
        if(self.pkt != None):
            self.dataHandler.sendPkt(pkt)
        self.bankManager = BankManager()

    def clientRecvData(self, data):
        pkts = self.dataHandler.recvPkt(data)
        for pkt in pkts:
            self.handleClientPkt(pkt)

    def handleClientPkt(self, pkt):
        pktID = pkt.DEFINITION_IDENTIFIER
        # respond to auto grade submit pkt
        if pktID == "20194.exercise6.autogradesubmitresponse":
            if pkt.client_status == 1:
                return
            self.sendGameInitRequestPkt()

        # respond to game payment request pkt
        elif pktID == "exercise7.gamepaymentrequest":
            id, account, amount = process_game_require_pay_packet(pkt)
            asyncio.create_task(self.sendGamePaymentResponsePkt(id, account, amount))

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

    def sendGameInitRequestPkt(self):
        pkt = create_game_init_packet(TEST_UNAME)
        self.dataHandler.sendPkt(pkt)

    async def sendGamePaymentResponsePkt(self, id, account, amount):
        if(amount > 10):
            printx("the amount is "+amount +
                   ", which is over 10, so stop the process")
            return

        receipt, receipt_sig =await self.bankManager.transfer(MY_ACCOUNT, account, amount, id)
        if(receipt == None or receipt_sig == None):
            printx("the bank transaction didn't complete, so the process stopped")
            return
        pkt = create_game_pay_packet(receipt, receipt_sig)
        self.dataHandler.sendPkt(pkt)

    def sendGameCmdPkt(self):
        if self.cmd_num + 1 > len(E6_STRS):
            return
        self.dataHandler.sendPkt(GameCommandPacket(
            command_string=E6_STRS[self.cmd_num]))
        self.cmd_num += 1


class ServerCmdHandler:
    def __init__(self, transport):
        self.dataHandler = DataHandler(transport)
        self.cmd_num = 0
        self.game = EscapeRoomGame(output=self.sendGameResPkt)
        self.game.create_game()
        self.payStatus = False

    def serverRecvData(self, data):
        pkts = self.dataHandler.recvPkt(data)
        for pkt in pkts:
            self.handleServerPkt(pkt)
        if self.game.status == "escaped":
            self.payStatus = False
            printx('Student server side finished!')

    def handleServerPkt(self, pkt):
        pktID = pkt.DEFINITION_IDENTIFIER
        # respond to game init pkt
        if pktID == "exercise7.gameinit":
            self.sendGamePaymentRequestPkt()

        # respond to game payment response pkt
        elif pktID == "exercise7.gamepaymentresponse":
            receipt, receipt_sig = process_game_pay_packet(pkt)
            if(self.checkPayment(receipt, receipt_sig)):
                printx("payment confirmed")
                self.payStatus = True
                # if passed
                self.game.start()
            else:
                printx("payment confirm failed")

        # respond to game command pkt
        elif pktID == "exercise7.gamecommand":
            if self.payStatus:
                self.game.command(pkt.command())
                time.sleep(0.25)
            else:
                printx("client try to play game before the payment is confirmed!")

        else:
            printx("unknown pkt:" + pktID)

    def sendGamePaymentRequestPkt(self):
        pkt = create_game_require_pay_packet(UNAME, MY_ACCOUNT, AMOUNT)
        self.dataHandler.sendPkt(pkt)

    def checkPayment(self, receipt, receipt_sig):
        # TODO: check payment, and return true if payment confirmed
        return True

    def sendGameResPkt(self, string):
        pkt = create_game_response(string, self.game.status)
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
