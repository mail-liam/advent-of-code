import re
from collections import deque
from aocd import get_data, submit

N_COLS = 10  # Plus 1 because no zero-indexed

data = get_data(day=5, year=2022)

COL_MAP = {}

for i in range(1, N_COLS):
    COL_MAP[i] = deque()

def print_cols():
    for value in COL_MAP.values():
        print(value)

data_gen = (line for line in data.split("\n"))

for line in data_gen:
    if line[1] == "1":
        break

    for i in range(1, N_COLS):
        index = 4 * (i - 1) + 1

        if line[index] != " ":
            COL_MAP[i].appendleft(line[index])

INSTRUCTION = re.compile("move (\d*) from (\d) to (\d)")
next(data_gen)  # Remove blank line

buffer = deque()
while True:
    # print_cols()
    # breakpoint()
    try:
        next_move = next(data_gen)
        amount, take_from, move_to = map(int, INSTRUCTION.match(next_move).groups())

        source_col = COL_MAP[take_from]
        target_col = COL_MAP[move_to]

        for _ in range(amount):
            buffer.append(source_col.pop())

        for _ in range(amount):
            target_col.append(buffer.pop())

    except StopIteration:
        break

for value in COL_MAP.values():
    print(value.pop())



# print(total)
# submit(total, part="b", day=4, year=2022)