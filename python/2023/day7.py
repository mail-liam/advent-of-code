from collections import Counter

EXAMPLE_DATA = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""



class Hand:
    def __init__(self, cards, bid, priority):
        self.cards = cards
        self.bid = bid
        self.priority = priority

    def __repr__(self):
        return f"Hand <{self.cards}, {self.bid}>"
    
    def __lt__(self, other):
        if not isinstance(other, Hand):
            raise ValueError(f"Comparison not supported between Hand and {type(other)}")
        
        return self.strength < other.strength
    
    def __gt__(self, other):
        return not self.__lt__(other)
    
    def get_hand_rank(self, cards):
        match len(set(cards)):
            case 1:
                return 7
            case 2:
                max_count = Counter(cards).most_common(1)[0][1]
                return 6 if max_count == 4 else 5
            case 3:
                max_count = Counter(cards).most_common(1)[0][1]
                return 4 if max_count == 3 else 3
            case 4:
                return 2
            case 5:
                return 1
    
    @property
    def strength(self):
        tiebreaker = [self.priority.index(card) for card in self.cards]

        if self.priority[0] != "J" or "J" not in self.cards:
            return self.get_hand_rank(self.cards), *tiebreaker

        card_options = set(self.cards)
        card_options.remove("J")

        if not card_options:  # Hand of all Jokers is a five of a kind
            return 7, *tiebreaker

        max_rank = 0

        for option in card_options:
            new_hand = self.cards.replace("J", option)
            new_rank = self.get_hand_rank(new_hand)

            if new_rank > max_rank:
                max_rank = new_rank

        return max_rank, *tiebreaker


def create_hands(data, priority):
    hands = []
    for line in data.splitlines():
        cards, bid = line.split(" ")
        hands.append(Hand(cards, int(bid), priority))
    hands.sort(key=lambda h: h.strength)

    return hands


def part1(data):
    # data = EXAMPLE_DATA

    hands = create_hands(data, "23456789TJQKA")

    return sum((i + 1) * hand.bid for i, hand in enumerate(hands))


def part2(data):
    # data = EXAMPLE_DATA
    # data = """JJJJJ 765"""

    hands = create_hands(data, "J23456789TQKA")

    return sum((i + 1) * hand.bid for i, hand in enumerate(hands))
