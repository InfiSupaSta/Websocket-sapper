import collections

from websockets.legacy.server import WebSocketServerProtocol

from backend.server.exceptions import ClientCantJoinException
from backend.utils.validator.core import QuantityValidator


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
    """
        Class for storing active clients connections.
        Quantity of users may be limited by setting 'expected_amount_of_clients' attribute.
    """

    expected_amount_of_clients = QuantityValidator()

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
