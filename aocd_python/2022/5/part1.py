import re

from collections import deque
from aocd import get_data, submit

data = get_data(day=5, year=2022)
COL_MAP = {}

for i in range(1, 10):
    COL_MAP[i] = deque()

def print_cols():
    for value in COL_MAP.values():
        print(value)

data_gen = (line for line in data.split("\n"))

for line in data_gen:
    if line[1] == "1":
        break

    for i in range(1, 10):
        index = 4 * (i - 1) + 1

        if line[index] != " ":
            COL_MAP[i].appendleft(line[index])

INSTRUCTION = re.compile("move (\d*) from (\d) to (\d)")
next(data_gen)  # Remove blank line

while True:
    try:
        next_move = next(data_gen)
        amount, take_from, move_to = map(int, INSTRUCTION.match(next_move).groups())

        source_col = COL_MAP[take_from]
        target_col = COL_MAP[move_to]

        for _ in range(amount):
            target_col.append(source_col.pop())

    except StopIteration:
        break

for value in COL_MAP.values():
    print(value.pop())


# print(total)
# submit(total, part="a", day=5, year=2022)