#!/usr/bin/env python

import asyncio
import aioconsole


async def foo():
    while True:
        line = await aioconsole.ainput('Input? ')
        print(f"received {line!r}")
        print(f"received {await aioconsole.ainput('Input2? ')!r}")


if __name__ == "__main__":
    asyncio.run(foo())