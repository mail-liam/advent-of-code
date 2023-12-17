import re
import typing as t
from collections import deque

INSTRUCTION = re.compile("move (\d*) from (\d) to (\d)")
N_COLS = 10  # Plus 1 because no zero-indexed


def get_initial_state(data: t.Generator) -> dict[int, deque]:
    COL_MAP = {i: deque() for i in range(1, N_COLS)}

    for line in data:
        if line[1] == "1":
            return COL_MAP

        for i in range(1, N_COLS):
            index = 4 * (i - 1) + 1

            if line[index] != " ":
                COL_MAP[i].appendleft(line[index])


def part1(data):
    data_gen = (line for line in data.splitlines())
    COL_MAP = get_initial_state(data_gen)
    
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

    return "".join(value.pop() for value in COL_MAP.values())


def part2(data):
    data_gen = (line for line in data.splitlines())
    COL_MAP = get_initial_state(data_gen)
    
    next(data_gen)  # Remove blank line

    buffer = deque()
    while True:
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

    return "".join(value.pop() for value in COL_MAP.values())
