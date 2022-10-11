import asyncio

from server import Server

server = Server(host="localhost",
                port=8765,
                expected_amount_of_clients=2)

if __name__ == "__main__":
    asyncio.run(
        server.start_server()
    )
