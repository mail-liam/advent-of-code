import re
from collections import deque

from common.grid import Point, NORTH, EAST, SOUTH, WEST, CARDINAL_ADJACENT

DEBUG = False
EXAMPLE_DATA = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

INPUT_RE = re.compile(r"(\w) (\d+) \(#([\w|\d]+)\)")

DIRECTION_TO_POINT = {"U": NORTH, "3": NORTH, "L": WEST, "2": WEST, "D": SOUTH, "1": SOUTH, "R": EAST, "0": EAST}


def debug_print(message):
    if DEBUG:
        print(message)


def visualize_grid(points, x_min, x_max, y_min, y_max):
    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            point = Point(i, j)
            symbol = "#" if point in points else "."
            print(symbol, end="")
        print("")


def part1(data):
    # data = EXAMPLE_DATA

    edge_points = set()
    current_point = Point(0, 0)
    edge_points.add(current_point)

    for line in data.splitlines():
        direction, distance, _ = INPUT_RE.match(line).groups()

        point_direction = DIRECTION_TO_POINT[direction]
        for _ in range(int(distance)):
            current_point = current_point + point_direction
            edge_points.add(current_point)

    # all_x = [point.x for point in edge_points]
    # grid_min_x = min(all_x)
    # grid_max_x = max(all_x)

    # all_y = [point.y for point in edge_points]
    # grid_min_y = min(all_y)
    # grid_max_y = max(all_y)

    # visualize_grid(edge_points, grid_min_x, grid_max_x, grid_min_y, grid_max_y)

    interior_points = set()
    queue = deque()
    # Below determined via min_x points: [Point (-199, 181), Point (-199, 180), Point (-199, 179), Point (-199, 178)]
    start_point = Point(-198, 180)
    queue.append(start_point)
    interior_points.add(start_point)

    while queue:
        current_point = queue.popleft()

        for direction in CARDINAL_ADJACENT:
            next_point = current_point + direction

            if next_point in edge_points:
                continue

            if next_point not in interior_points:
                interior_points.add(next_point)
                queue.append(next_point)

    return len(interior_points.union(edge_points))


def part2(data):
    # data = EXAMPLE_DATA

    edge_points = set()
    current_point = Point(0, 0)
    edge_points.add(current_point)

    for line in data.splitlines():
        _, _, hex_code = INPUT_RE.match(line).groups()
        hex_distance, direction = hex_code[:-1], hex_code[-1]
        distance = int(f"0x{hex_distance}", base=16)
        print(f"{direction} {distance}")

        # point_direction = DIRECTION_TO_POINT[direction]
        # for _ in range(distance):
        #     current_point = current_point + point_direction
        #     edge_points.add(current_point)



    return len(data.splitlines())
