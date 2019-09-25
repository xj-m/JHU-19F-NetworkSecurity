import asyncio
import playground
from escape_room_006 import EscapeRoomGame
from playground.network.packet import PacketType
from autograder_ex6_packets import *
from my_packet import *
from playground.common.logging import EnablePresetLogging, PRESET_VERBOSE

EnablePresetLogging(PRESET_VERBOSE)


class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        self.game = EscapeRoomGame()
        self.game.create_game(cheat=False, conn=transport)
        self.game.start()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(asyncio.wait(
            [asyncio.ensure_future(a) for a in self.game.agents]))
        self.deserializer = PacketType.Deserializer()

    def data_received(self, data):
        print('Data received. Deserializing...')
        self.deserializer.update(data)
        for packet in self.deserializer.nextPackets():
            if packet.DEFINITION_IDENTIFIER == "20194.exercise6.autogradesubmitresponse":
                print_test_status_packet(packet)
            elif packet.DEFINITION_IDENTIFIER == "team2.william.gamecommand":
                print_game_command_packet(packet)
                if self.game.status == "playing":
                    output = self.game.command(packet.game_command)
            else:
                print("Unidentifiable packet.")


def print_test_status_packet(packet):
    print('Autograder Submit Response Packet.')
    print('\t test_id: ' + packet.test_id)
    print('\t submit_status: ', packet.submit_status)
    print('\t client_status: ', packet.client_status)
    print('\t server_status: ', packet.server_status)
    if packet.error:
        print('\terror: ', packet.error)
    print('========================================')


def print_game_command_packet(packet):
    print('Game Command Packet.')
    print('\t game_command: ', packet.game_command)
    print('========================================')


loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = playground.create_server(EchoServerClientProtocol, "localhost", 1111)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
