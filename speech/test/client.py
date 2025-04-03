# client.py
import asyncio
import websockets

headers = [
    ("X-Api-Resource-Id", "volc.bigasr.sauc.duration"),
    ("X-Api-Request-Id", "test")
]

async def send_message():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri, max_size=1000000000) as websocket:
        await websocket.send("Hello, WebSocket!")
        response = await websocket.recv()
        print(f"Received from server: {response}")

asyncio.run(send_message())
