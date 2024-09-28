from collections import Counter

from domain.model.card import Card

CARD_RANKS = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}


# 같은 무늬가 5개 이상인지 확인
def is_flush(cards: list[Card]):
    suits = [card.suit for card in cards]
    counter = Counter(suits)
    for c in counter:
        if counter[c] >= 5:
            kicker = [card for card in cards if card.suit == c]
            kicker = sorted(kicker, key=lambda card: CARD_RANKS[card.rank], reverse=True)[:5]
            return c, kicker
    return False


# 스트레이트 여부 확인
def is_straight(cards: list[Card]):
    kicker = list()
    flag = set()
    for card in cards:
        if card.rank not in flag:
            kicker.append(card)
            flag.add(card.rank)

    kicker = sorted(kicker, key=lambda card: CARD_RANKS[card.rank], reverse=True)
    for i in range(len(kicker) - 4):
        if CARD_RANKS[kicker[i].rank] - CARD_RANKS[kicker[i + 4].rank] == 4:
            return True, kicker[i:i + 5]
    if kicker[0].rank == 'A' and all([card.rank in ['2', '3', '4', '5'] for card in kicker[-4:]]):  # A-2-3-4-5 스트레이트
        return True, [kicker[0]] + kicker[-4:]
    return False


def get_same_rank_cards(cards: list[Card]) -> list[list]:
    rank_set = set([card.rank for card in cards])
    same_rank_cards = [None for _ in range(len(rank_set))]
    for i, rank in enumerate(rank_set):
        same_rank_cards[i] = [card for card in cards if card.rank == rank]
        cards = [card for card in cards if card not in same_rank_cards[i]]

    same_rank_cards = sorted(same_rank_cards, key=lambda cards: (len(cards), CARD_RANKS[cards[0].rank]), reverse=True)

    return same_rank_cards


def get_hand_ranks(cards: list[Card]):
    same_rank_cards: list[list] = get_same_rank_cards(cards)

    if is_straight(cards) and is_flush(cards):
        return 9, is_flush(cards)[1]
    elif len(same_rank_cards[0]) == 4:
        return 8, same_rank_cards[0]
    elif len(same_rank_cards[0]) == 3 and len(same_rank_cards[1]) == 2:
        return 7, same_rank_cards[0] + same_rank_cards[1]
    elif is_flush(cards):
        return 6, is_flush(cards)[1]
    elif is_straight(cards):
        return 5, is_straight(cards)[1]
    elif len(same_rank_cards[0]) == 3:
        return 4, same_rank_cards[0]
    elif len(same_rank_cards[0]) == 2 and len(same_rank_cards[1]) == 2:
        return 3, same_rank_cards[0] + same_rank_cards[1]
    elif len(same_rank_cards[0]) == 2:
        return 2, same_rank_cards[0]
    else:
        return 1, same_rank_cards[0]

    pass
