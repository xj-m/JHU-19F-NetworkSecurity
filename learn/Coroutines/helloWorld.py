import asyncio, time
from formatter import *

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():

    printx("wait 1 sec example start")
    print('hello')
    # wait 1 second 
    await asyncio.sleep(1)
    print('world')
    printx('wait 1 sec example ends')

    printx('add def start')
    print(f"started at {time.strftime('%x')}")
    await say_after(1,'hello')
    await say_after(2,'world')
    print(f"finished at {time.strftime('%x')}")
    printx('add def ends')

    printx('add create task start')
    task1 = asyncio.create_task(
        say_after(1,'hello')
    )
    task2 = asyncio.create_task(
        say_after(2,'world')
    )
    await task1
    await task2
    printx('add create_task ends')


asyncio.run(main()) # NOTE: the way to call main
