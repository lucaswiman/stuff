#!/usr/bin/env python

import asyncio
from websockets import connect
import aioconsole


async def hello(uri):
    value = await aioconsole.ainput('Query? ')
    async with connect(f"{uri}?foo={value}") as websocket:
        while True:
            line = await aioconsole.ainput('Input? ')
            await websocket.send(line.encode())
            print(await websocket.recv())


if __name__ == "__main__":
    asyncio.run(hello("ws://localhost:8000/ws"))