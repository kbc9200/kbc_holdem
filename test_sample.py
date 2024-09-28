from application.service import game_console_usecase
from domain.model.card import Card
from domain.model.game import Game
from domain.model.user import User
from domain.service import card_service

suits = ['♠', '♥', '♣', '♦']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


def test_get_hand_ranks():
    cards = [Card('10', '♥'), Card('9', '♣'), Card('8', '♥'),
             Card('9', '♥'), Card('6', '♣'), Card('6', '♥'), Card('4', '♥')]
    card_service.get_hand_ranks(cards)
    cards = [Card('10', '♦'), Card('A', '♣'), Card('3', '♥'),
             Card('7', '♥'), Card('2', '♣'), Card('5', '♦'), Card('4', '♥')]
    card_service.get_hand_ranks(cards)

    game = Game()
    game.board_cards = make_card_list("8 ♥,9 ♥,6 ♣,6 ♥,4 ♥")
    alive_users = make_alive_users(["10 ♥,9 ♣", "5 ♦,6 ♦"])
    game_console_usecase.finalize_pot_result(game, alive_users)

    pass


def test_reassign_positions():
    game = Game()
    game_console_usecase.initialize_game(game, 6, 10000)
    game.users[1].chips = 0
    game_console_usecase.initialize_pot(game)


def make_alive_users(str_list: list[str]):
    alive_users = []

    for i, my_str in enumerate(str_list):
        cards = my_str.split(',')
        user = User(10000)
        user.index = i

        for j in range(2):
            rank, suit = cards[j].split(' ')
            user.hands.append(Card(rank, suit))

        alive_users.append(user)

    return alive_users


def make_card_list(my_str: str):
    cards = []
    my_str_cards = my_str.split(',')
    for my_str_card in my_str_cards:
        rank, suit = my_str_card.split(' ')
        cards.append(Card(rank, suit))
    return cards
