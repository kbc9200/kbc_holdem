import json
import os
import random
import time

import openai

from domain.enum.user_action_type import UserActionType
from domain.model.game import Game

openai.api_key = os.getenv('OPENAI_API_KEY')


def request_openai(messages):
    response = openai.chat.completions.create(  # 새 메서드 사용
        model="gpt-4o-2024-08-06",
        messages=messages,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content  # 응답 형식도 변경됨


def request_ai_action(game: Game, current_index, stage_round):
    users = game.users
    content_json = {
        "hands": str(users[current_index].hands),
        "position": users[current_index].position.value,
        "style": users[current_index].style.value,
        "chips": users[current_index].chips,
        "current_bet": users[current_index].current_bet,
        "stage_round": stage_round,
        "blind": game.blind,
        "pot": game.pot,
        "last_raise_bet": game.current_max_bet,
        "board": [str(card) for card in game.board_cards],
        "another_players_action": [{
            "position": user.position.value,
            "last_action": user.action.value,
            "chips": user.chips,
            "current_bet": user.current_bet
        } for i, user in enumerate(users) if i != current_index]
    }

    action_msg = json.dumps(content_json, ensure_ascii=False)
    reply_format = json.dumps({"action": 1, "bet": 0}, ensure_ascii=False)
    system_msg = (f"너는 프로 홀덤 플레이어야.\n"
                  f"another_players_action은 상대방의 정보고, 나머지는 너와 게임해 대한 정보야\n"
                  f"주어진 정보를 최대한 분석해서 최적의 플레이를 진행해줘.\n"
                  f"action은 1일 땐 Check or Call, 2일 땐 Raise, 3일 땐 All in, 4일 땐 Fold 야.\n"
                  f"답변을 다음 JSON 형식으로만 제공해\n{reply_format}")
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": action_msg},
    ]

    response = request_openai(messages)
    response = response.replace("```json\n", "").replace("\n```", "")
    response = json.loads(response)
    if response["action"] == 2:
        if users[current_index].action == UserActionType.RAISE:
            response["action"] = 1
        if response["bet"] < game.current_max_bet * 2:
            response["action"] = 1
        if response["bet"] >= users[current_index].chips + users[current_index].current_bet:
            response["action"] = 3

    # 대기 시간 적용
    delay = random.uniform(0.5, 2)
    time.sleep(delay)

    return response["action"], response["bet"]
