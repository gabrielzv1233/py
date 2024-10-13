import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        print(f"Received: {message}")

start_server = websockets.serve(echo, "localhost", 10768)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server started on ws://localhost:10768")
asyncio.get_event_loop().run_forever()
