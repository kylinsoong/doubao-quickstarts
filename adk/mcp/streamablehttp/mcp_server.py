import asyncio
import sys

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Test MCP Server", host="localhost", port=9000)

@mcp.tool(description="Get the weather of a city")
def get_city_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

async def shutdown(signal, loop):
    print(f"\nReceived exit signal {signal.name}...")
    
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    print(f"Cancelling {len(tasks)} outstanding tasks")
    
    loop.stop()
    
    print("Shutdown complete.")

if __name__ == "__main__":
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully...")
        print("Server has been shut down.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        print("Thank you for using the Test MCP Server!")
