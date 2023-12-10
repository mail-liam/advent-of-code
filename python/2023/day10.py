from collections import deque

from common.grid import NORTH, SOUTH, EAST, WEST, DistancePoint

EXAMPLE_DATA = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""


ADJACENT_POINTS = (NORTH, EAST, SOUTH, WEST)
DIRECTION_TO_PIPE = {
    NORTH.coordinate: ("|", "F", "7"),
    EAST.coordinate: ("J", "-", "7"),
    SOUTH.coordinate: ("L", "|", "J"),
    WEST.coordinate: ("L", "F", "-"),
}
PIPE_TO_DIRECTION = {
    "L": (NORTH, EAST),
    "|": (NORTH, SOUTH),
    "J": (NORTH, WEST),
    "F": (EAST, SOUTH),
    "-": (EAST, WEST),
    "7": (SOUTH, WEST),
}

def part1(data):
    # data = EXAMPLE_DATA

    grid = [line for line in data.splitlines()]

    start = None
    for row_num, row in enumerate(grid):
        if "S" not in row:
            continue

        col_num = row.index("S")

        start = DistancePoint(x=row_num, y=col_num, distance=0)
        break

    seen = set()
    seen.add(start)
    to_check = deque()
    # Find pipes pointing to start
    for direction in ADJACENT_POINTS:
        new_point = start + direction

        if new_point.x < 0 or new_point.y < 0:
            continue

        if grid[new_point.x][new_point.y] in DIRECTION_TO_PIPE[direction.coordinate]:
            to_check.append(new_point)

    # Walk the pipe
    while to_check:
        current_point = to_check.popleft()

        seen.add(current_point)
        pipe = grid[current_point.x][current_point.y]

        for direction in PIPE_TO_DIRECTION[pipe]:
            new_point = current_point + direction
            if new_point not in seen:
                to_check.append(new_point)

    furthest_point = sorted(seen, key=lambda p: p.distance, reverse=True)[0]
    return furthest_point.distance


def part2(data):
    data = EXAMPLE_DATA

    return data
