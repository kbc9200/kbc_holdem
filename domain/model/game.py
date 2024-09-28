from domain.model.card import Card
from domain.model.deck import Deck
from domain.model.user import User


class Game:
    def __init__(self):
        self.users: list[User] = []
        self.board_cards: list[Card] = []
        self.deck: Deck = None
        self.pot: int = 0
        self.blind: int = 200
        self.current_max_bet = 0
        self.current_index = 0

    def blind_up(self):
        blind = {200: 400, 400: 600, 600: 1000, 1000: 2000, 2000: 4000, 4000: 6000, 6000: 10000, 10000: 10000}
        self.blind = blind[self.blind]
