import asyncio
import websockets
import logging
import os
from dotenv import load_dotenv
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

# Load environment variables from .env file
load_dotenv()


# -------------------------- Configuration Parameters (modify as needed) --------------------------
WS_SERVER_URL = os.environ.get("WS_SERVER_URL", "")  # Read from environment variable
API_KEY = os.environ.get("API_KEY", "")  # Read from environment variable
PING_INTERVAL = 30  # Heartbeat interval (seconds), to prevent idle disconnection
PING_TIMEOUT = 10  # Heartbeat timeout (seconds), disconnect if no response after timeout
RECONNECT_INTERVAL = 5  # Reconnection interval (seconds)
MAX_RECONNECTS = 10  # Maximum number of reconnection attempts
# ------------------------------------------------------------------------

# Enable debug logging (for troubleshooting authentication/connection issues)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_auth_headers(api_key: str) -> dict:
    """Generate authentication headers (Bearer Token format)"""
    return {
        "Authorization": f"Bearer {api_key}",
        # Optional: Add other necessary headers (like Content-Type, Origin, etc., as required by the server)
        # "Content-Type": "application/json",
        # "Origin": "https://your-client-origin.com"
    }


async def handle_message(message: str | bytes):
    """Handle received server messages (modify logic as needed)"""
    if isinstance(message, bytes):
        logger.info(f"📥 Received binary message (length: {len(message)} bytes)")
        # If you need to save binary data (like files, images), you can handle it here
        # with open("received_data.bin", "wb") as f:
        #     f.write(message)
    else:
        logger.info(f"📥 Received text message: {message}")


async def websocket_client():
    """WebSocket client with authentication, heartbeat, and automatic reconnection"""
    reconnect_count = 0
    auth_headers = get_auth_headers(API_KEY)

    while reconnect_count < MAX_RECONNECTS:
        try:
            logger.debug(f"🔌 Attempting connection: {WS_SERVER_URL} (auth headers: {auth_headers})")

            # Core: Pass authentication headers when connecting (extra_headers parameter)
            async with websockets.connect(
                    WS_SERVER_URL,
                    additional_headers=auth_headers,  # Pass Bearer Token authentication header
                    ping_interval=PING_INTERVAL,  # Heartbeat to maintain connection
                    ping_timeout=PING_TIMEOUT,  # Heartbeat timeout threshold
                    close_timeout=5  # Connection close timeout
            ) as websocket:
                logger.info(f"✅ Connection successful! Server address: {WS_SERVER_URL}")
                reconnect_count = 0  # Reset reconnection count after successful connection

                # Asynchronous task: Continuously receive server messages
                async def receive_messages():
                    while True:
                        try:
                            message = await websocket.recv()
                            await handle_message(message)
                        except ConnectionClosedOK:
                            logger.info("❌ Connection closed normally")
                            break
                        except ConnectionClosedError as e:
                            logger.error(f"⚠️ Connection forcibly closed by server: {e}")
                            break
                        except Exception as e:
                            logger.error(f"⚠️ Failed to receive message: {type(e).__name__} - {str(e)}", exc_info=True)
                            break

                # Start receiving messages task
                receive_task = asyncio.create_task(receive_messages())

                # Loop to send user input messages (can be replaced with business logic)
                while True:
                    user_input = input("\nEnter message to send (type 'exit' to quit):")
                    if user_input.strip().lower() == "exit":
                        logger.info("🚪 Exiting client...")
                        await websocket.close(code=1000)  # Normal close (1000 is the standard success code)
                        receive_task.cancel()
                        await receive_task
                        return  # Exit client

                    # Send message (supports text/binary, modify as needed)
                    try:
                        await websocket.send(user_input)
                        logger.info(f"📤 Sent message: {user_input}")
                    except Exception as e:
                        logger.error(f"⚠️ Failed to send message: {str(e)}")
                        break

                await receive_task

        except Exception as e:
            reconnect_count += 1
            remaining_reconnects = MAX_RECONNECTS - reconnect_count
            logger.error(
                f"❌ Connection failed (remaining attempts: {remaining_reconnects}):"
                f"{type(e).__name__} - {str(e)}",
                exc_info=True
            )
            if remaining_reconnects <= 0:
                logger.error("❌ Maximum reconnection attempts reached, client exiting")
                break
            await asyncio.sleep(RECONNECT_INTERVAL)


if __name__ == "__main__":
    try:
        asyncio.run(websocket_client())
    except KeyboardInterrupt:
        logger.info("\n🛑 Client forcibly exited by user")








