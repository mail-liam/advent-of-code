import re
from aocd import get_data, submit

data = get_data(day=2, year=2023)
# data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

MAXIMUMS = {"red": 12, "green": 13, "blue": 14}

valid_ids = []

for row in data.splitlines():
    game_no, game_data = row.split(":")
    game_id = int(re.search("\d+", game_no)[0])
    # print(f"Parsing game: {game_id}")
    valid = True
    
    for game in game_data.split(";"):
        if not valid:
            break
        for colour, maximum in MAXIMUMS.items():
            total_shown = re.search(f"(\d+) {colour}", game)

            if total_shown is not None and int(total_shown[1]) > maximum:
                # print(f"Discarding game {game_id}")
                valid = False
                break

    if valid:
        valid_ids.append(game_id)


result = sum(valid_ids)
print(result)
submit(result, part="a", day=2, year=2023)