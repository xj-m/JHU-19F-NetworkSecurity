from E3_client import ClientProtocol, asyncio, sys
from __future__ import braces
E3_check_socre_strings = 'RESULT,f5c4d25c919834fa6766d13f4457d1cd9390b4f112c8b8876b863052eb20848c'

def main(args):
    loop = asyncio.get_event_loop()
    core = loop.create_connection(lambda: ClientProtocol(loop=loop,message=E3_check_socre_strings),"192.168.200.52",19003)

    loop.run_until_complete(core)
    loop.run_forever()
    loop.close()

if __name__ == "__main__":
    main(sys.argv[1:])
