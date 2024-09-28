from domain.enum.user_action_type import UserActionType
from domain.enum.user_position_type import UserPositionType
from domain.enum.user_style_type import UserStyleType
from domain.model.deck import Deck
from domain.model.game import Game
from domain.model.user import User
from domain.service import user_service, game_service, card_service
from interface import console_interface, openapi_interface


def initialize_game(game: Game, user_count: int, starting_chips: int):
    game.users = [User(starting_chips) for _ in range(user_count)]

    game.deck = Deck()
    game.deck.shuffle()

    print('게임을 시작하겠습니다.')

    user_service.assign_user_settings(game.users)

    import random
    for i in range(random.randint(1, 10)):
        user_service.rotate_positions(game.users)

    console_interface.display_users_positions(game.users)


def initialize_pot(game: Game):
    game.pot = 0
    game.current_max_bet = 0
    game.board_cards = []
    game.deck = Deck()
    game.deck.shuffle()

    reassign_position_flag = False
    for user in game.users:
        user.hands = []
        if user.chips == 0:
            reassign_position_flag = True
            game.users.remove(user)

    if reassign_position_flag:
        user_service.reassign_positions(game.users)
    else:
        user_service.rotate_positions(game.users)


def play_freflop(game: Game):
    user_service.set_status_wait(game.users, force=True)
    game_service.deal_hand(game)
    play_betting(game, "fre flop")
    alive_users = user_service.get_alive_players(game.users)
    if len(alive_users) == 1:
        finalize_pot_result(game, alive_users)
        return False

    return True


def play_flop(game: Game):
    user_service.set_status_wait(game.users)
    game_service.deal_flop(game)
    play_betting(game, "flop")
    alive_users = user_service.get_alive_players(game.users)
    if len(alive_users) == 1:
        finalize_pot_result(game, alive_users)
        return False

    return True


def play_turn(game: Game):
    user_service.set_status_wait(game.users)
    game_service.deal_turn(game)
    play_betting(game, "turn")
    alive_users = user_service.get_alive_players(game.users)
    if len(alive_users) == 1:
        finalize_pot_result(game, alive_users)
        return False

    return True


def play_river(game: Game):
    user_service.set_status_wait(game.users)
    game_service.deal_river(game)
    play_betting(game, "river")
    alive_users = user_service.get_alive_players(game.users)
    finalize_pot_result(game, alive_users)


def handle_user_action(game, action_count, bet, user, user_action):
    if user_action == 1:
        game_service.action_check_or_call(game, user)
    elif user_action == 2:
        game_service.action_bet(game, user, bet, UserActionType.RAISE)
        action_count = 0
    elif user_action == 3:
        game_service.action_all_in(game, user)
        action_count = 0
    elif user_action == 4:
        game_service.action_fold(game, user)
    elif user_action == 5:
        console_interface.display_current_game_state(game.pot, game.users)
    return action_count


def play_betting(game: Game, stage_round):
    console_interface.display_current_stage_round(stage_round, game.users, game)
    current_index = user_service.get_position_index(game.users, UserPositionType.SB)
    action_count = 0
    game.current_max_bet = 0

    while action_count < len(game.users):
        try:
            current_index = current_index % len(game.users)
            user = game.users[current_index]
            if len([user for user in game.users if user.action in [UserActionType.FOLD, UserActionType.ALL_IN]]) == len(game.users) - 1:
                continue
            if user.action == UserActionType.BLIND:
                if user.position == UserPositionType.SB:
                    game_service.action_bet(game, user, game.blind // 2)
                else:
                    game_service.action_bet(game, user, game.blind)
                action_count = -1
                continue
            if user.action == UserActionType.FOLD or user.action == UserActionType.ALL_IN:
                continue

            user_action = 0
            if user.style == UserStyleType.USER:
                available_actions = game_service.get_available_actions(game, user)
                while 1 > user_action or 4 < user_action:
                    user_action, bet = console_interface.input_user_action(user, available_actions, game, stage_round)
                    action_count = handle_user_action(game, action_count, bet, user, user_action)
            else:
                while 1 > user_action or 4 < user_action:
                    user_action, bet = openapi_interface.request_ai_action(game, current_index, stage_round)
                    action_count = handle_user_action(game, action_count, bet, user, user_action)

            console_interface.display_user_action(current_index, user.chips, user.position.value, user.action.value, user.current_bet, game.pot)
        finally:
            action_count += 1
            current_index += 1


def convert_rank_to_str(rank: int) -> str:
    rank_str = ['', '하이카드', '원페어', '투페어', '트리플', '스트레이트', '플러시', '풀하우스', '포카드', '스트레이트 플러시']
    return rank_str[rank]


def finalize_pot_result(game, alive_users):
    if len(alive_users) == 1:
        winner = alive_users[0]
        winner.increase_chips(game.pot)

        console_interface.display_msg(f"######## ALL FOLD 로 인해 {winner.index + 1}번 플레이어가 이번 팟에서 승리했습니다. ########")
        console_interface.display_msg(f"{winner.index + 1}번 플레이어는 {game.pot} 획득했습니다.")
        console_interface.display_users_chips(game.users)
    else:
        console_interface.display_msg(f"######## Show Down ########")
        console_interface.display_msg(f"보드의 카드 : {[str(card) for card in game.board_cards]}")

        assessment_data_list = []
        for user in alive_users:
            rank, hands = card_service.get_hand_ranks(game.board_cards + user.hands)
            console_interface.display_msg(f" - {user.index + 1}번 플레이어 핸드 ({[str(card) for card in user.hands]}) : {convert_rank_to_str(rank)} ({[str(card) for card in hands]})")
            assessment_data_list.append([user, rank, hands])

        assessment_data_list.sort(key=lambda data: [[data[1]] + [card.rank for card in data[2]]], reverse=True)
        winner = assessment_data_list[0][0]
        rank, hands = assessment_data_list[0][1], assessment_data_list[0][2]
        winner.increase_chips(game.pot)

        console_interface.display_msg(f"######## 쇼다운 결과 {winner.index + 1}번 플레이어가 {convert_rank_to_str(rank)} ({[str(card) for card in hands]})로 이번 팟에서 승리했습니다. ########")
        console_interface.display_msg(f"{winner.index + 1}번 플레이어는 {game.pot} 획득했습니다.")
        console_interface.wait_for_key("c")
        console_interface.display_users_chips(game.users)
