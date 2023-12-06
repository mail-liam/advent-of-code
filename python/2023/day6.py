import operator
import re
from functools import reduce

from common.parsing import parse_numbers

EXAMPLE_DATA = """Time:      7  15   30
Distance:  9  40  200"""

def part1(data):
    # data = EXAMPLE_DATA

    times, records = data.splitlines()

    race_times = parse_numbers(times)
    race_records = parse_numbers(records)
    races = zip(race_times, race_records)

    win_options = []
    for time, record in races:
        has_won = False
        possible_wins = 0

        for hold_time in range(time):
            remaining_time = time - hold_time
            distance = hold_time * remaining_time

            if distance > record:
                has_won = True
                possible_wins += 1
            elif has_won:
                win_options.append(possible_wins)
                break

    print(win_options)
    return reduce(operator.mul, win_options)


def part2(data):
    # data = EXAMPLE_DATA

    times, records = data.splitlines()

    time = int("".join(time for time in re.findall(r"\d+", times)))
    record = int("".join(record for record in re.findall(r"\d+", records)))

    has_won = False
    possible_wins = 0

    for hold_time in range(time):
        remaining_time = time - hold_time
        distance = hold_time * remaining_time

        if distance > record:
            has_won = True
            possible_wins += 1
        elif has_won:
            return possible_wins
