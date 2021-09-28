#!/usr/bin/env python
from fastapi import FastAPI, WebSocket
from typing import Optional
import random

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, foo: Optional[str]):
    print('Accepting client connection...')
    await websocket.accept()
    while True:
        try:
            # text = await websocket.receive_text()
            b = await websocket.receive_bytes()
            # resp = {'value': random.uniform(0, 1), "text": text}
            resp = {"b": repr(b), "foo_query": foo}
            await websocket.send_json(resp)
        except Exception as e:
            print('error:', e)
            break
    print('Bye..')


if __name__ == "__main__":
    import os
    os.system('uvicorn app:app --reload')