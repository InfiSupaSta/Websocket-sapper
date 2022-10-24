from game.core import Game
from backend.sapper.player.core import Player

"""

An example of game that starts in console. 
To choose coordinates for field exploring 
type it in terminal as x, y as ints like
>>> 3 5

"""


if __name__ == "__main__":
    game = Game(
        players=1,
        field_width=7,
        field_height=10,
        bombs_on_the_field=25
    )

    player = Player(username="Best sapper player in da world!")
    game.register_player(player)
    game.start_game()

    game.wait_for_player_move()

