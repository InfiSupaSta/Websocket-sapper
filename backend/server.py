import asyncio
import collections
import logging

from websockets import serve, WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError


class Server:

    def __init__(self, *, host: str, port: int):
        self.host: str = host
        self.port: int = port

        self.clients = ClientHandler()

        self.message_handler = MessageHandler()

    async def start_server(self):
        async with serve(self.websocket_handler, self.host, self.port):
            print(f"\nServer started successfully! Available at >>> ws://{self.host}:{self.port} <<<\n")
            await asyncio.Future()

    async def websocket_handler(self, websocket_connection: WebSocketServerProtocol):

        self.clients.register_new_client(websocket_connection)
        await self.send_stored_messages_to_new_client(websocket_connection)

        while True:
            try:
                new_message = await websocket_connection.recv()
                self.message_handler.messages_container.append(new_message)
            except ConnectionClosedError:
                continue
            except ConnectionClosedOK:
                self.clients.unregister_client(websocket_connection)
                break
            await self.send_message_to_websocket_clients(new_message)

    async def send_message_to_websocket_clients(self, message: str):
        for client in self.clients.active_clients:
            await client.send(message)

    async def send_stored_messages_to_new_client(self, websocket_connection: WebSocketServerProtocol):

        messages: collections.deque = self.message_handler.messages_container

        if messages:
            for message in self.message_handler.messages_container:
                await websocket_connection.send(message)


class MessageHandler:

    """
        Object for storing some amount of most recent messages that
        will be sent to new client after connection for the sake of
        saving chat history (I hope :) ).
    """

    def __init__(self, *, amount_of_messages_to_store: int = 50):
        self.messages_container = collections.deque(maxlen=amount_of_messages_to_store)

    def store_message_to_container(self, message: str):
        self.messages_container.append(message)


class ClientHandler:

    def __init__(self):
        self.active_clients = []

    def register_new_client(self, websocket_connection: WebSocketServerProtocol):
        self.active_clients.append(websocket_connection)
        print(f"+ New client! {websocket_connection}")

    def unregister_client(self, websocket_connection: WebSocketServerProtocol):
        self.active_clients.remove(websocket_connection)
        print(f"- User {websocket_connection} disconnected.")
