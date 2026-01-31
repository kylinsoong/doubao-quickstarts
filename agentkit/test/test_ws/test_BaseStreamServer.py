import asyncio
import json
import traceback
import websockets
from websockets.exceptions import ConnectionClosed

# 你自己的 logger（如果没有就先用 print 代替）
import logging
stream_logger = logging.getLogger("stream_server")
logging.basicConfig(level=logging.INFO)


class BaseStreamServer:
    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = port
        self.active_connections = {}  # Store client connections

    async def start_server(self):
        stream_logger.info(f"Starting stream server on {self.host}:{self.port}")
        async with websockets.serve(self.manage_connection, self.host, self.port):
            await asyncio.Future()  # Run forever

    async def manage_connection(self, websocket):
        """Handle a new client connection"""
        connection_id = id(websocket)
        stream_logger.info(f"New connection established: {connection_id}")

        # Store active connection
        self.active_connections[connection_id] = websocket

        # Send ready message to client
        await websocket.send(json.dumps({"type": "ready"}))

        try:
            # Start processing the stream for this client
            await self.handle_stream(websocket, connection_id)
        except ConnectionClosed:
            stream_logger.info(f"Connection closed: {connection_id}")
        except Exception as e:
            stream_logger.error(f"Error handling connection {connection_id}: {e}")
            stream_logger.error(traceback.format_exc())
        finally:
            # Clean up
            if connection_id in self.active_connections:
                del self.active_connections[connection_id]

    async def handle_stream(self, websocket, client_id):
        raise NotImplementedError("Subclasses must implement handle_stream")


class EchoStreamingService(BaseStreamServer):
    async def handle_stream(self, websocket, client_id):
        stream_logger.info(f"[Echo] start streaming for client_id={client_id}")

        async for message in websocket:
            # message 可能是 str 或 bytes
            if isinstance(message, bytes):
                stream_logger.info(f"[Echo] recv binary len={len(message)} from {client_id}")
                # 原样回传 binary
                await websocket.send(message)
            else:
                stream_logger.info(f"[Echo] recv text='{message}' from {client_id}")

                # 尝试当 JSON 解析（可选）
                try:
                    payload = json.loads(message)
                    resp = {
                        "type": "echo",
                        "client_id": client_id,
                        "payload": payload,
                    }
                except json.JSONDecodeError:
                    resp = {
                        "type": "echo",
                        "client_id": client_id,
                        "data": message,
                    }

                await websocket.send(json.dumps(resp, ensure_ascii=False))

        stream_logger.info(f"[Echo] stream ended for client_id={client_id}")


if __name__ == "__main__":
    service = EchoStreamingService(host="0.0.0.0", port=8765)
    asyncio.run(service.start_server())

