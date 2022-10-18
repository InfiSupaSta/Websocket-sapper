import asyncio

from backend.server.core import Server

server = Server(host="localhost",
                port=8765,
                expected_amount_of_clients=None)

if __name__ == "__main__":
    asyncio.run(
        server.start_server()
    )
