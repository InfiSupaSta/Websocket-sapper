class OtherPlayerTurnException(Exception):

    def __repr__(self):
        return "This player can't move right now - it is not his turn."


class PlayerCantJoinException(Exception):

    def __repr__(self):
        return "All spots for players are taken."
