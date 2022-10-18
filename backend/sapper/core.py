from game.core import Game
from backend.sapper.player.core import Player

if __name__ == "__main__":
    game = Game(
        players=1,
        field_width=7,
        field_height=10,
        bombs_on_the_field=70
    )

    player = Player(username="Ivan")

    game.register_player(player)
    game.start_game()

    game.wait_for_player_move()

