from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT8, STRING, BUFFER, UINT16, BOOL
# whatever field types you need

# 1. fill in all the parts that are comments.
# so long as you can construct the packet with a single command string for the command packet
# and a response string and status string for the response packet.


class GameCommandPacket(PacketType):
    DEFINITION_IDENTIFIER = "20194.e6.gamecommand"  # whatever you want
    DEFINITION_VERSION = "1.0"  # whatever you want

    FIELDS = [
        ("cmd", STRING)
    ]

    @classmethod
    def create_game_command_packet(cls, cmd):
        # whatever arguments needed to construct the packet)
        return cls(cmd=cmd)

    def command(self):
        # MUST RETURN A STRING!
        # whatever you need to get the command for the game.
        return self.cmd


class GameResponsePacket(PacketType):
    DEFINITION_IDENTIFIER = "20194,e6,gameResponse"  # whatever you want
    DEFINITION_VERSION = "1.0"  # whatever you want

    FIELDS = [
        ("res", STRING),
        ("sta", STRING)
    ]

    @classmethod
    def create_game_response_packet(cls, response, status):
        # whatever you need to construct the packet )
        return cls(res=response, sta=status)

    def game_over(self):
        # MUST RETURN A BOOL
        # whatever you need to do to determine if the game is over
        return self.sta != "playing"

    def status(self):
        # MUST RETURN game.status (as a string)
        return self.sta  # whatever you need to do to return the status

    def response(self):
        # MUST return game response as a string
        return self.res  # whatever you need to do to return the response
