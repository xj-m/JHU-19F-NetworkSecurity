# Lab 1 Milestone 2: Error-Free Delivery

|          |            |
| -------- | ---------- |
| Assigned | 10/14/2019 |
| Due      | 10/21/2019 |
| Points   | 75         |

## Overview

> OK, continuing on with our reliable layer which you guys have named "POOP" (Playground Overlay Operational Protocol).
> You need to extend your protocol to transmit data during error-free conditions.

## Transmission Requirements.

As you create your protocol, it must provide the following.

1. FULL DUPLEX COMMUNICATIONS
2. Confirmation that the data was received correctly and in-order (it will be, but you should **confirm** it)
3. Error handling if an **unexpected packet**(e.g., handshake packet) is received during data transmission

## More info about packets

This means that `PacketType.Deserializer` cannot deserialize them.

> I forgot to tell you that when packets are imported as part of a connecgtor, they are "siloed". That means that they are not available in the general packet management.
> As you are creating at least two different types of packets, here is how you **create a deserializer** that can deserialize all of them.

'''

    class PoopPacketType(PacketType):
        DEFINITION_IDENTIFIER = "poop"
        DEFINITON_VERSION = "1.0"

    class PoopHandshakePacket(PoopPacketType):
        # your definition here

    class PoopDataPacket(PoopPacketType):
        # your definition here

'''
To deserialize either a handshake or data packet

    deserializer = PoopPacketType.Deserializer()

## Writing the PRFC and Standardizing by the Due Date

Each team will be taking their own approach to this. At any time you can start to propose to other teams how you think the class should do the assignment. But you will be more persuasive if you have a working prototype. As you get your lab working, you need to discuss over slack how you think the PRFC should be written and what should be the standard. Unlike the Escape Room exercise, this will involve protocol design and not just packets.
The PETF can vote, at any time, on any proposal. BUT the handshake must be standardized and the whole class conforming to it by the due date (10/21/2019).

## Grading

On the due date, I will post an auto-grader on the **SAFE NETWORK**that conforms to the proposed PRFC. I will provide you with the auto-grade client and you will not need to write it yourself. But it will require that the connector for your network layer is installed in your own personal playground with the **name assigned** by the PETF.

The address and port of the autograder will be:

**20194.0.0.19100 and port 19101**

The **auto-grader** will test handshakes in both directions. You will be graded as follows

- 25 points for "small" transmissions in 1 direction
- 25 points for "large" transmissions in 1 direction
- 25 points for full duplex
