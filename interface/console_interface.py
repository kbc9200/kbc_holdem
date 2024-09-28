import os
import sys
import time

from domain.enum.user_action_type import UserActionType
from domain.model.game import Game
from domain.model.user import User


def input_int_within_range(min_value, max_value):
    while True:
        try:
            value = int(input())
            if min_value <= value <= max_value:
                break
            else:
                print(f"{min_value}~{max_value} 사이의 값을 입력하세요.")
        except ValueError:
            print("정수 값을 입력하세요.")
    return value


def input_game_settings():
    print("\n플레이 유저수를 입력하세요.(2~9) : ")
    user_count = input_int_within_range(2, 9)

    print("스타팅 칩의 크기를 입력하세요.(10000~50000) : ")
    starting_chips = input_int_within_range(10000, 50000)

    return starting_chips, user_count


def input_user_action(user: User, available_actions: list[UserActionType], game: Game, stage_round):
    print("\n######## 나의 차례 ########")
    display_user_hands(user)
    print(f"가장 최근 Bet {game.current_max_bet}, 팟 사이즈 {game.pot}")
    print(f"현재 Board({stage_round}) : ({[str(card) for card in game.board_cards]})")
    print("User의 액션을 정해주세요. (1~5, 1: Check or Call, 2: Raise, 3: All in, 4: Fold, 5: 현재상태표시)")
    print("유저가 할 수 있는 동작")
    convert_action_str = {UserActionType.CHECK: "1.Check", UserActionType.CALL: "1.Call", UserActionType.RAISE: "2.Raise",
                          UserActionType.ALL_IN: "3.AllIn", UserActionType.FOLD: "4.Fold"}
    for i, action in enumerate(available_actions):
        print(f"  - {convert_action_str[action]}", end='')
    print("  - 5.현재상태표시")
    lines = 9
    bet = 0
    user_action = int(input())
    if user_action == 2:
        bet = int(input(f"Raise 할 금액을 입력해주세요. ({max(game.current_max_bet * 2, game.blind)}~{user.current_bet + user.chips})"))
        lines += 1
    clear_display(lines)
    return user_action, bet


def display_current_game_state(pot, users):
    print("######## 현재 게임 상태를 표시합니다. ########")
    print(f"현재 팟 : {pot}")
    print(f"나의 핸드 : {' '.join(str(card) for card in users[0].hands)}")
    print(f"플레이어 정보: ")
    lines = 5
    for i, user in enumerate(users):
        print(
            f"\t- {i + 1}번 플레이어{'(User)' if i == 0 else ''} {user.position.value} : 칩 {user.chips}, 현재 베팅 {user.current_bet}, 마지막 액션 {user.action.value}")
        lines += 1
    print(f"################")
    time.sleep(5)
    clear_display(lines)


def display_users_chips(users):
    print("######## 현재 Chip을 표시합니다. ########")
    for i, user in enumerate(users):
        print(
            f"\t- {i + 1}번 플레이어{'(User)' if i == 0 else ''} : 칩 {user.chips}")
    print(f"################")


def display_user_hands(user: User):
    print("당신의 핸드는 : " + ' '.join(str(card) for card in user.hands) + f" ({user.position.value})")


def display_users_positions(users: list[User]):
    print("랜덤으로 배정된 현재 포지션은 아래와 "
          "같습니다.")
    print(f'\t- 1번 플레이어(User) : {users[0].position.value}')
    for i in range(1, len(users)):
        print(f'\t- {i + 1}번 플레이어 : {users[i].position.value}')


def display_user_action(current_index, user_chip, user_position, user_action, user_bet, pot):
    print(f" {current_index + 1}번 플레이어 {user_position} : 칩 {user_chip}, 현재 액션 {user_action}, 현재 배팅 {user_bet}, 팟 {pot}")
    pass


def display_available_user(users: list[User], stage_round):
    print(f"######## 살아있는 플레이어 ########")
    for user in users:
        if user.action != UserActionType.FOLD:
            print(f"\t- {user.index + 1}번 플레이어 {user.position.value} : 칩 {user.chips}")


def display_current_stage_round(stage_round, users, game):
    clear_display_all()
    display_available_user(users, stage_round)
    print(f"######## {stage_round} 시작합니다. ########")
    display_user_hands(users[0])
    print(f"보드 위 카드 : {[str(card) for card in game.board_cards]}")


def display_msg(msg):
    print(msg)
    pass


def clear_display_all():
    time.sleep(3)
    if os.name == 'nt':
        _ = os.system('cls')  # Windows 용
    else:
        _ = os.system('clear')  # MacOS/Linux 용


def clear_display(n=0):
    for _ in range(n):
        clear_last_line()
    sys.stdout.flush()


def clear_last_line():
    sys.stdout.write('\x1b[1A')  # 커서를 한 줄 위로 이동
    sys.stdout.write('\x1b[2K')


def wait_for_key(target_key):
    while True:
        key = input("c 키 입력 대기중 c 키를 입력하면 이어서 진행됩니다.:")
        if key == target_key:
            print(f"{target_key} key pressed.")
            break
