import asyncio
import collections
import logging
from typing import Optional

from websockets import serve, WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from backend.sapper.game.core import Game
from backend.server.exceptions import ClientCantJoinException
from backend.server.handlers import ClientHandler, MessageHandler
from backend.server.mixins import WebsocketMessagePrefixesMixin
from backend.utils.validator.core import QuantityValidator

logger = logging.basicConfig()


class Server(WebsocketMessagePrefixesMixin):

    """
    Class for handling websocket connections. Last 50 messages, current game
    field - if it exists - will be sent to new client. All websocket message
    prefixes for handling game actions are stored in WebsocketMessagePrefixesMixin.
    Use start_server method for starting the serve.
    """

    expected_amount_of_clients = QuantityValidator()

    def __init__(self, *, host: str, port: int, expected_amount_of_clients: Optional[int] = None):
        self.host = host
        self.port = port

        self.expected_amount_of_clients = expected_amount_of_clients

        self.clients = ClientHandler(expected_amount_of_clients=self.expected_amount_of_clients)
        self.messages = MessageHandler()
        self.game = None

    async def start_server(self):
        async with serve(self._websocket_handler, self.host, self.port):
            print(f"\nServer started successfully! Available at >>> ws://{self.host}:{self.port} <<<\n")
            await asyncio.Future()

    async def _check_if_client_can_join(self, websocket_connection: WebSocketServerProtocol):
        try:
            self.clients.register_new_client(websocket_connection)
            return True
        except ClientCantJoinException:
            return await websocket_connection.send(self.SERVER_MAX_LIMIT_OF_CONNECTIONS_PREFIX)

    async def _check_if_game_already_exists(self, websocket_connection: WebSocketServerProtocol):
        if self.game is not None:

            # if self.game.is_game_finished is True:
            #     return await websocket_connection.send(self.GAME_FINISH_PREFIX)

            width = self.game.field.size_x
            height = self.game.field.size_y
            message = f"{self.GAME_DRAW_TABLE_PREFIX} {width} {height}"
            if self.game.is_game_finished is True:
                message += " ended"
            else:
                message += " started"
            await websocket_connection.send(message)
            return await websocket_connection.send(self.GAME_STARTED_PREFIX)

        return False

    async def _websocket_handler(self, websocket_connection: WebSocketServerProtocol):

        if not await self._check_if_client_can_join(websocket_connection):
            return

        await self._check_if_game_already_exists(websocket_connection)
        await self._send_stored_messages_to_new_client(websocket_connection)

        while True:
            try:
                new_message: str = await websocket_connection.recv()

                if self._check_message_have_prefix(new_message):
                    await self._handle_messages_with_prefixes(new_message)
                    continue

                self.messages.messages_container.append(new_message)
            except ConnectionClosedError:
                continue
            except ConnectionClosedOK:
                self.clients.unregister_client(websocket_connection)
                break
            await self._send_message_to_websocket_clients(new_message)

    async def _send_message_to_websocket_clients(self, message: str):
        for client in self.clients.active_clients:
            await client.send(message)

    async def _send_stored_messages_to_new_client(self, websocket_connection: WebSocketServerProtocol):
        messages: collections.deque = self.messages.messages_container
        if messages:
            for message in self.messages.messages_container:
                await websocket_connection.send(message)

    async def _handle_messages_with_prefixes(self, new_message: str):

        if new_message.startswith(self.GAME_DRAW_TABLE_PREFIX):
            width = self.game.field.size_x
            height = self.game.field.size_y
            message = f"{self.GAME_DRAW_TABLE_PREFIX} {width} {height}"
            if self.game.is_game_finished is True:
                message += " ended"
            else:
                message += " started"
            await self._send_message_to_websocket_clients(message)

        elif new_message.startswith(self.GAME_FINISH_PREFIX) and self.game is not None:
            self.game.finish_game_without_players_requirement()

        elif new_message.startswith(self.GAME_TABLE_DELETE_PREFIX):
            self.game = None
            print("\n>>> Game dropped, new game can be started.\n")
            await self._send_message_to_websocket_clients(self.GAME_TABLE_DELETE_PREFIX)

        elif new_message.startswith(self.GAME_INIT_PREFIX) and self.game is None:
            prefix, width, height = new_message.split()
            bombs_on_the_field = int(int(width) * int(height) * 0.3)  # 30% of the field covered by bombs
            self.game = Game(field_width=int(width),
                             field_height=int(height),
                             bombs_on_the_field=bombs_on_the_field,
                             players=self.expected_amount_of_clients)
            self.game.start_game_without_players_requirement()
            await self._send_message_to_websocket_clients(self.GAME_INIT_PREFIX)

        elif new_message.startswith(self.GAME_CELL_CLICK_PREFIX):
            prefix, coordinates = new_message.split()
            x_coordinate, y_coordinate = [int(coordinate) for coordinate in coordinates.split("_")]
            actual_cell_info = self.game.field.get_field()[x_coordinate][y_coordinate]
            message = self.GAME_SERVER_RESPONSE_PREFIX + " " + coordinates + " " + actual_cell_info
            await self._send_message_to_websocket_clients(message)

    def _check_message_have_prefix(self, message: str):
        return any(message.startswith(prefix) for prefix in self.get_message_prefixes())
