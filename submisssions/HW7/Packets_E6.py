from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT8, STRING, BUFFER, UINT16, BOOL


class GameCommandPacket(PacketType):
    DEFINITION_IDENTIFIER = "20194.e6.gamecommand"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("cmd", STRING)
    ]

    @classmethod
    def create_game_command_packet(cls, cmd):
        return cls(cmd=cmd)

    def command(self):
        # MUST RETURN A STRING!
        return self.cmd


class GameResponsePacket(PacketType):
    DEFINITION_IDENTIFIER = "20194,e6,gameResponse"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("res", STRING),
        ("sta", STRING)
    ]

    @classmethod
    def create_game_response_packet(cls, response, status):
        return cls(res=response, sta=status)

    def game_over(self):
        # MUST RETURN A BOOL
        return self.sta != "playing"

    def status(self):
        # MUST RETURN game.status (as a string)
        return self.sta

    def response(self):
        # MUST return game response as a string
        return self.res
