from backend.sapper.field.field import Field
from backend.sapper.player.exceptions import PlayerCantJoinException
from backend.sapper.field.exceptions import GameOverException
from backend.sapper.player.player import PlayersContainer, Player


class Game:

    """
    Functionality according to websockets will be added soon
    """

    def __init__(self, *, field_width: int, field_height: int, bombs_on_the_field: int, players: int):
        self.field = Field(size_x=field_width, size_y=field_height, amount_of_bombs=bombs_on_the_field)
        self.expected_amount_of_players = players
        self.players = PlayersContainer(amount_of_players=self.expected_amount_of_players)
        self.is_game_started = False
        self.is_player_lost = False
        self.is_game_finished = None

    def start_game(self):
        if self.is_game_finished is not True and len(self.players) == self.expected_amount_of_players:
            self.field.get_field_to_show_for_user()
            self.field.get_ready_for_game_field()
            self.is_game_started = True

    def finish_game(self):
        if self.is_game_started is True and self.is_player_lost is True:
            self.is_game_finished = True

    def wait_for_player_move(self):
        """
            method for testing game, will be deleted
        """
        while True:
            for row in self.field.field_to_show_for_user:
                print(row)
            x, y = input("\nPlease type x and y coordinates separated by whitespace(like 3 5).\n\n").split(" ")
            x, y = int(x) - 1, int(y) - 1
            try:
                self.field.update_player_field(x_coordinate=x, y_coordinate=y)
            except GameOverException:
                print("GAME OVER!")
                break
            except Exception as exception:
                print(exception)
                continue

    def register_player(self, player: Player):
        self.players.add_player(player)
