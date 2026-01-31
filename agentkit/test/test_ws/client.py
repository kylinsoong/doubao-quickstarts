import asyncio
import websockets

async def test():
    uri = "ws://127.0.0.1:8765"
    async with websockets.connect(uri) as ws:
        print("server:", await ws.recv())  # ready

        await ws.send("hello")
        print("server:", await ws.recv())

        await ws.send('{"a": 1}')
        print("server:", await ws.recv())

asyncio.run(test())

