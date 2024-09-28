import time

from application.service import game_console_usecase
from domain.model.game import Game
from interface.console_interface import input_game_settings


# messages = [
#     {"role": "system", "content": "You are a helpful assistant."}
# ]


def main():
    starting_chips, user_count = input_game_settings()

    game = Game()
    game_console_usecase.initialize_game(game, user_count, starting_chips)
    blind_count = 0

    while True:
        if blind_count == 5:
            game.blind_up()
            blind_count = 0

        if game_console_usecase.play_freflop(game):
            if game_console_usecase.play_flop(game):
                if game_console_usecase.play_turn(game):
                    game_console_usecase.play_river(game)
        time.sleep(2)
        game_console_usecase.initialize_pot(game)

        blind_count += 1

    pass


# 메인 진입점
if __name__ == "__main__":
    main()
# 대화 반복
