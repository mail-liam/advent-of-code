import math
import typing as t
from itertools import count, cycle

EXAMPLE_DATA = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

def part1(data):
    # data = EXAMPLE_DATA

    data_gen = iter(data.splitlines())

    step_order = next(data_gen)
    step_gen = cycle(step_order)
    next(data_gen)

    state_map = {}
    for line in data_gen:
        state, next_state = line.split(" = ")

        state_map[state] = next_state[1:4], next_state [6:9]


    current_state = "AAA"
    for i in count(1):
        step = 0 if next(step_gen) == "L" else 1

        current_state = state_map[current_state][step]

        if current_state == "ZZZ":
            break

    return i


def part2(data):
#     data = """LR

# 11A = (11B, XXX)
# 11B = (XXX, 11Z)
# 11Z = (11B, XXX)
# 22A = (22B, XXX)
# 22B = (22C, 22C)
# 22C = (22Z, 22Z)
# 22Z = (22B, 22B)
# XXX = (XXX, XXX)"""

    data_gen = iter(data.splitlines())

    step_order = next(data_gen)
    next(data_gen)

    STATE_MAP = {}
    for line in data_gen:
        state, next_state = line.split(" = ")

        STATE_MAP[state] = next_state[1:4], next_state [6:9]


    class Ghost:
        def __init__(self, state):
            self.state = state

        def update(self, step: t.Literal["L", "R"]):
            step = 0 if step == "L" else 1
            self.state = STATE_MAP[self.state][step]


    GHOSTS = []
    for state in STATE_MAP:
        if state[-1] == "A":
            GHOSTS.append(Ghost(state))


    def find_first_ghost_z_point(ghost: Ghost, step_order):
        count = 0
        step_gen = iter(step_order)
        direction = next(step_gen)

        while True:
            try:
                if ghost.state[-1] == "Z":
                    print(f"Found Z state at step {count}")
                    return count

                ghost.update(direction)
                count += 1
                direction = next(step_gen)
            except StopIteration:
                step_gen = iter(enumerate(step_order))
                direction = next(step_gen)


    ghost_z_times = [find_first_ghost_z_point(ghost, step_order) for ghost in GHOSTS]

    return math.lcm(*ghost_z_times)
