import asyncio
import os

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncpg

app = FastAPI()


@app.get("/")
async def get():
    with open("./index.html", "r") as f:
        return HTMLResponse(f.read())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await LISTENING.wait()
    channel_messages = asyncio.Queue()
    subscribers.append(channel_messages)
    async def recv_websocket():
        while True:
            msg = await channel_messages.get()
            await websocket.send_text(msg)
    recv_task = asyncio.create_task(recv_websocket())
    try:
        while True:
            data = await websocket.receive_text()
            messages.put_nowait(data)
    finally:
        recv_task.cancel()


subscribers = []
messages = asyncio.Queue()
LISTENING = asyncio.Event()

async def listen_to_channel(connection, pid, channel, payload):
    for subscriber in list(subscribers):
        subscriber.put_nowait(payload)

async def listen():
    conn = await asyncpg.connect(os.environ["DATABASE_URL"])
    LISTENING.set()
    async def recv():
        while True:
            msg = await messages.get()
            await conn.execute("SELECT pg_notify('mychannel', $1)", msg)
    recv_task = asyncio.create_task(recv())
    await conn.add_listener('mychannel', listen_to_channel)
    try:
        while True:
            await conn.execute('select 1')
            await asyncio.sleep(60)
    finally:
        recv_task.cancel()

@app.on_event("startup")
async def startup_event():
    _ = asyncio.create_task(listen())
