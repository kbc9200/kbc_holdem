from domain.enum.user_action_type import UserActionType
from domain.model.game import Game
from domain.model.user import User


def deal_hand(game: Game):
    for user in game.users:
        user.hands = []

    for _ in range(2):
        for user in game.users:
            if user.action != UserActionType.FOLD:
                user.hands.append(game.deck.draw())


def deal_flop(game: Game):
    game.deck.draw()
    for _ in range(3):
        game.board_cards.append(game.deck.draw())


def deal_turn(game: Game):
    game.deck.draw()
    game.board_cards.append(game.deck.draw())


def deal_river(game: Game):
    game.deck.draw()
    game.board_cards.append(game.deck.draw())


def get_available_actions(game, user: User) -> list[UserActionType]:
    if user.action in [UserActionType.FOLD, UserActionType.ALL_IN]:
        raise Exception("FOLD, ALL_IN 상태인데 get_available_actions 사용했음.")

    available_actions = []
    if user.current_bet == game.current_max_bet:
        available_actions.append(UserActionType.CHECK)
    elif user.current_bet < game.current_max_bet:
        available_actions.append(UserActionType.CALL)

    if user.current_bet + user.chips >= game.current_max_bet * 2:
        available_actions.append(UserActionType.RAISE)

    if user.current_bet + user.chips > game.current_max_bet:
        available_actions.append(UserActionType.ALL_IN)

    available_actions.append(UserActionType.FOLD)

    return available_actions


# noinspection PyMethodMayBeStatic
def action_fold(game, user: User):
    if game.current_max_bet == user.current_bet:
        action_check_or_call(game, user)
    else:
        user.action = UserActionType.FOLD


def action_bet(game, user: User, amount: int, action_type: UserActionType = UserActionType.WAIT):
    user.action = action_type  # SB, BB 블라인드 금액 낼 때는 WAIT
    amount -= user.current_bet

    if amount >= user.chips:
        amount = user.chips
        user.action = UserActionType.ALL_IN

    user.increase_current_bet(amount)
    user.decrease_chips(amount)
    user.increase_total_bet(amount)

    game.current_max_bet = max(game.current_max_bet, user.current_bet)
    game.pot += amount


def action_check_or_call(game, user: User):
    if user.current_bet < game.current_max_bet:
        action_bet(game, user, game.current_max_bet, action_type=UserActionType.CALL)
    else:
        user.action = UserActionType.CHECK


def action_all_in(game, user: User):
    action_bet(game, user, user.chips + user.current_bet, action_type=UserActionType.ALL_IN)
