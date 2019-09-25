from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER

class MyPacket(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.student_x.MyPacket"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("counter1", UINT32),
        ("counter2", UINT32),
        ("name", STRING),
        ("data", BUFFER)
        ]

packet1 = MyPacket()
packet1.counter1 = 100
packet1.counter2 = 200
packet1.name = "Dr. Nielson"
# packet1.data = 'This may look like a string but it’s actually a sequence of bytes.'.encode()


packetBytes = packet1.__serialize__()
packet2 = PacketType.Deserialize(packetBytes)
if packet1 == packet2:
    print("These two packets are the same!")
  
  
deserializer = PacketType.Deserializer()
deserilaizer.update(data)
for packet in deserializer.nextPackets():
    print(packet)
  # now I have a packet!

  
packet1 = MyPacket()
	# fill in packet1 fields
packet2 = MyPacket()
	# fill in packet2 fields
packet3 = MyPacket()
	# fill in packet3 fields
pktBytes = packet1.__serialize__() + packet2.__serialize__() + packet3.__serialize__()


deserializer = PacketType.Deserializer()
print("Starting with {} bytes of data".format(len(pktBytes)))
while len(pktBytes) > 0:
  # let’s take of a 10 byte chunk
  chunk, pktBytes = pktBytes[:10], pktBytes[10:]
  deserializer.update(chunk)
  print("Another 10 bytes loaded into deserializer. Left={}".format(len(pktBytes)))
  for packet in deserializer.nextPackets():
      print("got a packet!")
      if packet == packet1: 
          print("It’s packet 1!")
      elif packet == packet2: print("It’s packet 2!")
      elif packet == packet3: print("It’s packet 3!")