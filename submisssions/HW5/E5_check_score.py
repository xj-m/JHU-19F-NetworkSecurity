from E5_client import ClientProtocol, asyncio, sys
import playground
E3_check_socre_strings = 'RESULT,e26a6fc8609118c1b06dbab6e33531a947fadec9dfe392dd3c0d2bd93de8ea02'


def main(args):
    loop = asyncio.get_event_loop()
    core = playground.create_connection(lambda: ClientProtocol(
        loop=loop, message=E3_check_socre_strings), "20194.0.0.19000", 19005)

    loop.run_until_complete(core)
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main(sys.argv[1:])
