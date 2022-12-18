from collections import defaultdict
from itertools import pairwise
from aocd import get_data, submit

data = get_data(day=14, year=2022)
# data = """498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9"""

SOLID_MAP = defaultdict(bool)

def fill_rock_line(start, end):
    index = 1 if start[0] == end[0] else 0
    mag = 1 if start[index] < end[index] else -1

    SOLID_MAP[end] = True  # While loop won't catch this!

    next_chunk = start
    while next_chunk != end:
        SOLID_MAP[next_chunk] = True
        if index:
            next_chunk = next_chunk[0], next_chunk[1] + mag
        else:
            next_chunk = next_chunk[0] + mag, next_chunk[1]

for line in data.splitlines():
    segments = [tuple(point.split(",")) for point in line.split(" -> ")]
    segments = [(int(col), int(row)) for col, row in segments]
    # print(segments)
    for seg_pair in pairwise(segments):
        fill_rock_line(*seg_pair)


MAX_FALL = max(point[1] for point in SOLID_MAP)
print(f"MAX_FALL: {MAX_FALL}")

sand_count = -1
def drop_sand(current_pos=(500, 0), initial=False):
    below = current_pos[0], current_pos[1] + 1

    if below[1] > MAX_FALL:  # Gone too far!
        return False

    if initial:
        global sand_count
        sand_count += 1

    if not SOLID_MAP[below]:  # Not solid, move into it
        return drop_sand(below)

    # Now try bottom left
    below_left = current_pos[0] - 1, current_pos[1] + 1
    if not SOLID_MAP[below_left]:
        return drop_sand(below_left)

    # Now try bottom left
    below_right = current_pos[0] + 1, current_pos[1] + 1
    if not SOLID_MAP[below_right]:
        return drop_sand(below_right)

    # print(f"Placing sand at {current_pos}")
    SOLID_MAP[current_pos] = True
    return True

while drop_sand(initial=True):
    pass

print(sand_count)
# submit(sand_count, part="a", day=14, year=2022)