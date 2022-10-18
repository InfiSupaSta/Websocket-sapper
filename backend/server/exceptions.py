class ClientCantJoinException(Exception):
    message = "Max amount of clients on this server."

    def __repr__(self):
        return self.message
