from backend.sapper.field.core import Field
from backend.sapper.player.exceptions import PlayerCantJoinException
from backend.sapper.field.exceptions import GameOverException
from backend.sapper.player.core import PlayersContainer, Player


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
        self.is_game_finished = False

    def start_game(self):
        if self.is_game_finished is not True and len(self.players) == self.expected_amount_of_players:
            self.start_game_without_players_requirement()

    def start_game_without_players_requirement(self):
        self.field.get_field_to_show_for_user()
        self.field.get_ready_for_game_field()
        self.is_game_started = True

    def finish_game(self):
        if self.is_game_started is True and self.is_player_lost is True:
            self.is_game_finished = True

    def finish_game_without_players_requirement(self):
        self.is_game_finished = True

    def wait_for_player_move(self):
        """
            Method for testing game in terminal.
            Waiting for coordinates input from user
            and redraw field according to received info.
        """
        while True:
            self.field.redraw_field()
            x, y = input("\nPlease type y and x coordinates separated by whitespace(like 3 5).\n\n").split(" ")

            try:
                x, y = int(x) - 1, int(y) - 1
                self.field.update_player_field(x_coordinate=x, y_coordinate=y)
            except GameOverException:
                print("GAME OVER!")
                break
            except Exception as exception:
                print(f"{str(exception)}\n")
                continue

    def register_player(self, player: Player):
        self.players.add_player(player)
