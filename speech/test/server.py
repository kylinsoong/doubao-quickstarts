import asyncio
import websockets

async def handler(websocket):
    print("Client connected")
    for header, value in websocket.connection.request_headers.items():
        print(f"{header}: {value}")

    try:
        async for message in websocket:
            print(f"Received from client: {message}")
            response = f"Echo: {message}"
            await websocket.send(response)
    except websockets.ConnectionClosed:
        print("Client disconnected")

async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

asyncio.run(main())

