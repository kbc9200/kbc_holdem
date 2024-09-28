import random

from domain.enum.user_action_type import UserActionType
from domain.enum.user_position_type import UserPositionType
from domain.enum.user_style_type import UserStyleType
from domain.model.user import User


def assign_positions(users: list[User]):
    num_players = len(users)
    unassigned_positions = ['SB', 'BB', 'UTG', 'MP', 'MP', 'MP', 'HJ', 'CO']
    assigned_positions = [None] * num_players

    for i in range(0, num_players if num_players < 3 else 3):
        assigned_positions[i] = unassigned_positions.pop(0)

    for j in range(num_players - 2, i, -1):
        assigned_positions[j] = unassigned_positions.pop()

    if num_players > 2:
        assigned_positions[num_players - 1] = 'BTN'

    mp_count = 1

    for i in range(0, num_players):
        if assigned_positions[i] == 'MP':
            assigned_positions[i] += str(mp_count)
            mp_count += 1

        users[i].position = UserPositionType(assigned_positions[i])
        users[i].index = i


def reassign_positions(users: list[User]):
    lowest_position_index = min(range(len(users)), key=lambda i: int(users[i].position))
    assign_positions(users)
    for _ in range(lowest_position_index + 1):
        rotate_positions(users)
    pass


def assign_styles(users: list[User]):
    styles = list(UserStyleType)
    styles.remove(UserStyleType.USER)

    for user in users:
        user.style = UserStyleType(random.choice(styles))

    users[0].style = UserStyleType(UserStyleType.USER)


def rotate_positions(users: list[User]):
    num_players = len(users)
    temp_position = users[num_players - 1].position

    for i in range(num_players - 1, 0, -1):
        users[i].position = users[i - 1].position

    users[0].position = temp_position


def assign_user_settings(users: list[User]):
    assign_positions(users)
    assign_styles(users)
    pass


def get_position_index(users: list[User], position: UserPositionType):
    for i, user in enumerate(users):
        if user.position == position:
            return i
    return -1  # 해당 포지션이 없으면 -1 반환


def set_status_wait(users: list[User], force: bool = False):
    for user in users:
        user.current_bet = 0
        if (user.action != UserActionType.FOLD and user.action != UserActionType.ALL_IN) or force:
            user.action = UserActionType.WAIT

        if force:
            user.total_bet = 0
            if user.position == UserPositionType.SB or user.position == UserPositionType.BB:
                user.action = UserActionType.BLIND


def get_alive_players(users: list[User]):
    alive_users = []
    for user in users:
        if user.action != UserActionType.FOLD:
            alive_users.append(user)
    return alive_users
