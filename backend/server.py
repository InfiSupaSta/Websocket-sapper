import asyncio
import collections
import logging

from websockets import serve, WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from backend.sapper.game.game import Game


class Server:
    GAME_INIT_PREFIX = "__sapper_init_field_size"
    MAX_LIMIT_OF_CONNECTIONS_PREFIX = "__server_exceeded_limit_of_connections"
    GAME_CELL_CLICK_PREFIX = "__sapper_cell_clicked"
    GAME_SERVER_RESPONSE_PREFIX = "__sapper_server_response_with_cell_info"
    GAME_DRAW_TABLE_PREFIX = "__sapper_draw_table_for_other_clients"
    GAME_TABLE_DELETE_PREFIX = "__sapper_game_table_delete"

    def __init__(self, *, host: str, port: int, expected_amount_of_clients: int = None):
        self.host: str = host
        self.port: int = port

        self.expected_amount_of_clients = expected_amount_of_clients
        if self.expected_amount_of_clients is not None:
            self.clients = ClientHandler(expected_amount_of_clients=self.expected_amount_of_clients)
        else:
            self.clients = ClientHandler()

        self.message_handler = MessageHandler()
        self.game = None

    async def start_server(self):
        async with serve(self.websocket_handler, self.host, self.port):
            print(f"\nServer started successfully! Available at >>> ws://{self.host}:{self.port} <<<\n")
            await asyncio.Future()

    async def websocket_handler(self, websocket_connection: WebSocketServerProtocol):
        try:
            self.clients.register_new_client(websocket_connection)
        except ClientCantJoinException as error:
            print(error.message)
            await websocket_connection.send(self.MAX_LIMIT_OF_CONNECTIONS_PREFIX)
            return

        await self.send_stored_messages_to_new_client(websocket_connection)

        while True:
            try:
                new_message: str = await websocket_connection.recv()

                # if self.game:
                #     x_coordinate = self.game.field.size_x
                #     y_coordinate = self.game.field.size_y
                #     message = f"{self.GAME_DRAW_TABLE_PREFIX} {x_coordinate} {y_coordinate}"
                #     await self.send_message_to_websocket_clients(message)
                #     continue

                if new_message.startswith(self.GAME_DRAW_TABLE_PREFIX):
                    print(">>> trying to REDRAW")
                    width = self.game.field.size_x
                    height = self.game.field.size_y
                    message = f"{self.GAME_DRAW_TABLE_PREFIX} {width} {height}"
                    for client in self.clients.active_clients:
                        await client.send(message)
                    continue

                if new_message.startswith(self.GAME_TABLE_DELETE_PREFIX):
                    self.game = None
                    print("game deleted", self.game)
                    continue

                if new_message.startswith(self.GAME_INIT_PREFIX):
                    print("game trying to start")
                    if self.game is None:
                        prefix, width, height = new_message.split()
                        print(f"Width: {width}, height: {height}")

                        self.game = Game(field_width=int(width),
                                         field_height=int(height),
                                         bombs_on_the_field=int(int(width) * int(height) * 0.1),
                                         # players=self.expected_amount_of_clients)
                                         players=1)
                        self.game.register_player(websocket_connection)
                        self.game.start_game()
                    else:
                        pass
                    continue

                if new_message.startswith(self.GAME_CELL_CLICK_PREFIX):
                    prefix, coordinates = new_message.split()
                    print(coordinates)

                    x_coordinate, y_coordinate = [int(coordinate) for coordinate in coordinates.split("_")]

                    actual_cell_info = self.game.field.get_field()[x_coordinate][y_coordinate]
                    message = self.GAME_SERVER_RESPONSE_PREFIX + " " + coordinates + " " + actual_cell_info
                    await self.send_message_to_websocket_clients(message)

                    continue

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


class ClientCantJoinException(Exception):
    message = "Max amount of clients on this server."

    def __repr__(self):
        return self.message


class ClientHandler:

    def __init__(self, *, expected_amount_of_clients: int = None):
        self.expected_amount_of_clients = expected_amount_of_clients
        self.active_clients = []

    def register_new_client(self, websocket_connection: WebSocketServerProtocol):
        if self._check_client_can_join():
            self.active_clients.append(websocket_connection)
            print(f"+ New client! {websocket_connection}")
        else:
            raise ClientCantJoinException

    def unregister_client(self, websocket_connection: WebSocketServerProtocol):
        self.active_clients.remove(websocket_connection)
        print(f"- User {websocket_connection} disconnected.")

    def _check_client_can_join(self):
        if self.expected_amount_of_clients is not None:
            return len(self.active_clients) < self.expected_amount_of_clients
        return True
