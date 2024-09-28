from domain.enum.user_action_type import UserActionType
from domain.enum.user_position_type import UserPositionType
from domain.enum.user_style_type import UserStyleType
from domain.model.card import Card


class User:
    def __init__(self, chips):
        self.hands: list(Card) = []
        self.chips = chips
        self.action: UserActionType = UserActionType.WAIT
        self.position: UserPositionType = None
        self.style: UserStyleType = None
        self.current_bet = 0
        self.total_bet = 0
        self.index = 0

    def init_hands(self):
        self.hands = []
        self.action = ''
        self.position = UserPositionType()

    def add_hand(self, card: Card):
        self.hands.append(card)

    def increase_chips(self, amount: int):
        self.chips += amount

    def decrease_chips(self, amount: int):
        if self.chips < amount:
            raise ValueError('Chips cannot be decreased')
        self.chips -= amount

    def increase_current_bet(self, amount: int):
        self.current_bet += amount

    def increase_total_bet(self, amount: int):
        self.total_bet += amount
