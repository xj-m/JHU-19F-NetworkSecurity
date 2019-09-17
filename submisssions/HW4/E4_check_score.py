from E4_client import ClientProtocol, asyncio, sys
E3_check_socre_strings = 'RESULT,9fd259ae4c96ccffe8a54fe691cf94978f2040a35c8d9cbde5985501bc7db20e'


def main(args):
    loop = asyncio.get_event_loop()
    core = loop.create_connection(lambda: ClientProtocol(
        loop=loop, message=E3_check_socre_strings), "192.168.200.52", 19004)

    loop.run_until_complete(core)
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main(sys.argv[1:])
