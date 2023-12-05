from collections import deque

from aocd import get_data, submit

data = get_data(day=18, year=2022)
# data = """2,2,2
# 1,2,2
# 3,2,2
# 2,1,2
# 2,3,2
# 2,2,1
# 2,2,3
# 2,2,4
# 2,2,6
# 1,2,5
# 3,2,5
# 2,1,5
# 2,3,5"""

LAVA = set()

def is_out_of_bounds(space):
    return (
        space[0] < MIN_X
        or space[0] > MAX_X
        or space[1] < MIN_Y
        or space[1] > MAX_Y
        or space[2] < MIN_Z
        or space[2] > MAX_Z
    )

def get_empty_adjacent(cube):
    adjacent_spaces = set()

    if (space := (cube[0], cube[1], cube[2] + 1)) not in LAVA:
        adjacent_spaces.add(space)

    if (space := (cube[0], cube[1], cube[2] - 1)) not in LAVA:
        adjacent_spaces.add(space)

    if (space := (cube[0], cube[1] + 1, cube[2])) not in LAVA:
        adjacent_spaces.add(space)

    if (space := (cube[0], cube[1] - 1, cube[2])) not in LAVA:
        adjacent_spaces.add(space)

    if (space := (cube[0] + 1, cube[1], cube[2])) not in LAVA:
        adjacent_spaces.add(space)

    if (space := (cube[0] - 1, cube[1], cube[2])) not in LAVA:
        adjacent_spaces.add(space)

    return adjacent_spaces

def count_lava_adjacent(cube):
    score = 0
    if (cube[0], cube[1], cube[2] + 1) in LAVA:
        score += 1

    if (cube[0], cube[1], cube[2] - 1) in LAVA:
        score += 1

    if (cube[0], cube[1] + 1, cube[2]) in LAVA:
        score += 1

    if (cube[0], cube[1] - 1, cube[2]) in LAVA:
        score += 1

    if (cube[0] + 1, cube[1], cube[2]) in LAVA:
        score += 1

    if (cube[0] - 1, cube[1], cube[2]) in LAVA:
        score += 1

    return score

def check_is_outside(space):
    seen = set()
    seen.add(space)
    to_visit = deque()
    to_visit.append(space)

    while to_visit:
        current_space = to_visit.popleft()

        for next_space in get_empty_adjacent(current_space):
            if next_space in seen:
                continue

            if is_out_of_bounds(next_space):
                return True

            to_visit.append(next_space)
            seen.add(next_space)
    return False


MIN_X, MAX_X, MIN_Y, MAX_Y, MIN_Z, MAX_Z = 100, 0, 100, 0, 100, 0
for cube in data.splitlines():
    x, y, z = [int(dim) for dim in cube.split(",")]
    MIN_X = min(x, MIN_X)
    MAX_X = max(x, MAX_X)
    MIN_Y = min(y, MIN_Y)
    MAX_Y = max(y, MAX_Y)
    MIN_Z = min(z, MIN_Z)
    MAX_Z = max(z, MAX_Z)
    LAVA.add((x, y, z))
# print(MIN_X, MAX_X, MIN_Y, MAX_Y, MIN_Z, MAX_Z)

ADJACENT_EMPTY = set()
for cube in LAVA:
    ADJACENT_EMPTY = ADJACENT_EMPTY.union(get_empty_adjacent(cube))

total = 0
for space in ADJACENT_EMPTY:
    if check_is_outside(space):
        total += count_lava_adjacent(space)

print(total)
# submit(total, part="b", day=18, year=2022)