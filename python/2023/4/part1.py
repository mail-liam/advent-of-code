import math
from aocd import get_data, submit

data = get_data(day=4, year=2023)
# data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


CARDS = []

def parse_numbers(numbers):
    res = []
    for n in numbers.split(" "):
        try:
            res.append(int(n))
        except ValueError:
            continue

    return res


class Card:
    def __init__(self, winning, numbers):
        self.winning = winning
        self.numbers = numbers

    def get_score(self):
        score = 0
        for num in self.numbers:
            if num in self.winning:
                score += 1

        return max(0, math.pow(2, score - 1))

for line in data.splitlines():
    card_no, cards = line.split(": ")
    
    winning, entries = cards.split(" | ")

    winning_nums, entry_nums = parse_numbers(winning), parse_numbers(entries)

    CARDS.append(Card(winning_nums, entry_nums))



result = sum(card.get_score() // 1 for card in CARDS)
print(result)
submit(result, part="a", day=4, year=2023)