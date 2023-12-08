import re
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
    step_gen = cycle(step_order)
    next(data_gen)

    STATE_MAP = {}
    for line in data_gen:
        state, next_state = line.split(" = ")

        STATE_MAP[state] = next_state[1:4], next_state [6:9]


    class Ghost:
        def __init__(self, state):
            self.state = state

        def update(self, step):
            self.state = STATE_MAP[self.state][step]


    GHOSTS = []
    for state in STATE_MAP:
        if state[-1] == "A":
            GHOSTS.append(Ghost(state))

    ghost = GHOSTS[0]
    seen_states = set()
    valid_states = []

    MAX_STATES = 2 * len(STATE_MAP)
    print(MAX_STATES)
    for i in count(1):
        step = 0 if next(step_gen) == "L" else 1
        seen_states.add((ghost.state, step))
        ghost.update(step)

        if (ghost.state, step) in seen_states:
            print(ghost.state, step)
            break
        
        if ghost.state[-1] == "Z":
            print(f"Found Z state at step {i}")
            valid_states.append(i)

    print(valid_states)
    breakpoint()


    for i in count(1):
        step = 0 if next(step_gen) == "L" else 1
        for ghost in GHOSTS:
            ghost.update(step)

        if all(ghost.state[-1] == "Z" for ghost in GHOSTS):
            break

    return i
