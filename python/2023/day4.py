import math
import re

from common.parsing import parse_numbers


EXAMPLE_DATA = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


class Card:
    def __init__(self, id, winning, numbers):
        self.id = id
        self.winning = winning
        self.numbers = numbers

    def get_score(self):
        return sum(1 for num in self.numbers if num in self.winning)
    
    @classmethod
    def from_data(cls, data):
        card_no, cards = data.split(": ")
        card_number = parse_numbers(card_no)[0]
        winning, entries = cards.split(" | ")

        return Card(id=card_number, winning=parse_numbers(winning), numbers=parse_numbers(entries))


def part1(data):
    # data = EXAMPLE_DATA
    CARDS = [Card.from_data(line) for line in data.splitlines()]

    return sum(max(0, math.pow(2, card.get_score() - 1)) // 1 for card in CARDS)


def part2(data):
    # data = EXAMPLE_DATA
    CARDS = [Card.from_data(line) for line in data.splitlines()]
    CARD_COUNTS = {card.id: 1 for card in CARDS}
    MAX_COUNT = max(CARD_COUNTS)

    for card in CARDS:
        score = card.get_score()
        current_id = card.id
        count = CARD_COUNTS[current_id]

        for i in range(1, score + 1):
            next_card_id = current_id + i
            if next_card_id > MAX_COUNT:
                break
            CARD_COUNTS[next_card_id] += count

    return sum(CARD_COUNTS.values())
