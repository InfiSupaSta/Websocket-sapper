from typing import Union

from backend.sapper.player.exceptions import OtherPlayerTurnException, PlayerCantJoinException
from backend.utils.validator.core import QuantityValidator


class Player:

    def __init__(self, username: str):

        self.username = username
        self.is_player_turn = False

    def check_if_player_can_make_a_turn(self):
        if self.is_player_turn is False:
            return False
        return True

    def register_player_move(self):
        if self.check_if_player_can_make_a_turn():
            self.is_player_turn = False
            return
        raise OtherPlayerTurnException

    def take_turn(self):
        self.is_player_turn = True


class PlayersContainer:
    amount_of_players = QuantityValidator()

    def __init__(self, amount_of_players: Union[int, None]):
        self.amount_of_players = amount_of_players
        self.players = []

    def _check_if_player_can_join(self):
        if len(self.players) < self.amount_of_players:
            return True
        return False

    def add_player(self, player: Player):
        if self._check_if_player_can_join() is False:
            raise PlayerCantJoinException
        self.players.append(player)

    def __len__(self):
        return len(self.players)
