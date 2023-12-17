EXAMPLE_DATA = """A Y
B X
C Z"""

def part1(data):
    # data = EXAMPLE_DATA

    SCORE_MAP = {
        "A X": 4,  # Rock draw - 3 + 1
        "A Y": 8,
        "A Z": 3,
        "B X": 1,
        "B Y": 5,
        "B Z": 9,
        "C X": 7,
        "C Y": 2,
        "C Z": 6,
    }

    return sum(SCORE_MAP[match] for match in data.split("\n"))


def part2(data):
    # data = EXAMPLE_DATA

    SCORE_MAP = {
        "A X": 3,  # Rock lose - 3 + 0
        "A Y": 4,  # Rock draw - 1 + 3
        "A Z": 8,  # Rock win - 2 + 6
        "B X": 1,  # Paper lose - 1 + 0
        "B Y": 5,  # Paper draw - 2 + 3
        "B Z": 9,  # Paper win - 3 + 6
        "C X": 2,  # Scissors lose - 2 + 0
        "C Y": 6,  # Scissors draw - 3 + 3
        "C Z": 7,  # Scissors win - 1 + 6
    }

    return sum(SCORE_MAP[match] for match in data.split("\n"))