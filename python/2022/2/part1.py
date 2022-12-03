from aocd import get_data, submit

data = get_data(day=2, year=2022)

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

score = 0
for match in data.split("\n"):
    score += SCORE_MAP[match]

print(score)
submit(score, part="a", day=2, year=2022)