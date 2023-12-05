from aocd import get_data, submit

data = get_data(day=2, year=2022)

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

score = 0
for match in data.split("\n"):
    score += SCORE_MAP[match]

print(score)
submit(score, part="b", day=2, year=2022)