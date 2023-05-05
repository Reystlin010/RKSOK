import asyncio
from handle_requests import handle_request
from loguru import logger

logger.add("debug.log", format="{time} {level} {message}",
level="DEBUG", rotation="10 KB", compression="zip")
# test_bd = {}


# async def parse_request(message):
#     parsed_request = message.split(" ")[0]
#     test_bd.append(parsed_request)

async def handle_client(reader, writer):
    """Establishing connection with a client"""
    try:
        data = await reader.readuntil(separator=b'\r\n\r\n')
    except asyncio.IncompleteReadError:
        print("There was no correct data recieved")
    message = data.decode()
    raw_request = message.replace("\r\n\r\n","")

    # addr = writer.get_extra_info("peername")
    # print(f"New client connected from {addr!r}")

    # print(f"Send: {message!r}")
    await handle_request(raw_request)
    print(await handle_request(raw_request))
    writer.write(data)
    await writer.drain()

    # print("Connection closed")
    writer.close()
    await writer.wait_closed()

async def start_rksok():
    server = await asyncio.start_server(
        handle_client,
        "195.135.253.40",
        8000
    )
    # addrs = " ,".join(str(sock.getsockname()) for sock in server.sockets)
    # print(f"Serving on {addrs}")
    

    async with server:
        await server.serve_forever()

asyncio.run(start_rksok())
