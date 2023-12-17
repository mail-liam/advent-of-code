from collections import defaultdict
from itertools import pairwise


EXAMPLE_DATA = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def process_data(data):
    SOLID_MAP = defaultdict(bool)
    for line in data.splitlines():
        segments = [
            (int(col), int(row))
            for col, row in (
                tuple(point.split(",")) for point in line.split(" -> ")
            )
        ]

        for seg_pair in pairwise(segments):
            fill_rock_line(SOLID_MAP, *seg_pair)

    return SOLID_MAP


def fill_rock_line(area, start, end):
    index = 1 if start[0] == end[0] else 0
    mag = 1 if start[index] < end[index] else -1

    area[end] = True  # While loop won't catch this!

    next_chunk = start
    while next_chunk != end:
        area[next_chunk] = True
        if index:
            next_chunk = next_chunk[0], next_chunk[1] + mag
        else:
            next_chunk = next_chunk[0] + mag, next_chunk[1]


def part1(data):
    # data = EXAMPLE_DATA

    SOLID_MAP = process_data(data)
    MAX_FALL = max(point[1] for point in SOLID_MAP)
    print(f"MAX_FALL: {MAX_FALL}")

    sand_count = -1
    def drop_sand(current_pos=(500, 0), initial=False):
        below = current_pos[0], current_pos[1] + 1

        if below[1] > MAX_FALL:  # Gone too far!
            return False

        if initial:
            nonlocal sand_count
            sand_count += 1

        if not SOLID_MAP[below]:  # Not solid, move into it
            return drop_sand(below)

        # Now try bottom left
        below_left = current_pos[0] - 1, current_pos[1] + 1
        if not SOLID_MAP[below_left]:
            return drop_sand(below_left)

        # Now try bottom right
        below_right = current_pos[0] + 1, current_pos[1] + 1
        if not SOLID_MAP[below_right]:
            return drop_sand(below_right)

        # print(f"Placing sand at {current_pos}")
        SOLID_MAP[current_pos] = True
        return True
    

    while drop_sand(initial=True):
        pass

    return sand_count


def part2(data):
    # data = EXAMPLE_DATA

    SOLID_MAP = process_data(data)
    MAX_FALL = max(point[1] for point in SOLID_MAP) + 2
    print(f"MAX_FALL: {MAX_FALL}")


    def get_solidity(pos):
        if pos[1] == MAX_FALL:
            return True

        return SOLID_MAP[pos]
    

    def drop_sand(current_pos=(500, 0)):
        below = current_pos[0], current_pos[1] + 1
        if not get_solidity(below):  # Not solid, move into it
            return drop_sand(below)

        # Now try bottom left
        below_left = current_pos[0] - 1, current_pos[1] + 1
        if not get_solidity(below_left):
            return drop_sand(below_left)

        # Now try bottom right
        below_right = current_pos[0] + 1, current_pos[1] + 1
        if not get_solidity(below_right):
            return drop_sand(below_right)

        # print(f"Placing sand at {current_pos}")
        SOLID_MAP[current_pos] = True


    sand_count = 0
    while True:
        drop_sand()
        sand_count += 1

        if get_solidity((500, 0)):
            break

    return sand_count