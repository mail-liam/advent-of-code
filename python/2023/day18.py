import re

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

INPUT_RE = re.compile(r"(\w) (\d+) \((#[\w|\d]+)\)")

DIRECTION_TO_POINT = {"U": NORTH, "L": WEST, "D": SOUTH, "R": EAST}


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

    all_x = [point.x for point in edge_points]
    grid_min_x = min(all_x)
    grid_max_x = max(all_x)

    all_y = [point.y for point in edge_points]
    grid_min_y = min(all_y)
    grid_max_y = max(all_y)

    visualize_grid(edge_points, grid_min_x, grid_max_x, grid_min_y, grid_max_y)
    breakpoint()

    interior_points = set()
    for i in range(grid_min_x, grid_max_x + 1):
        for j in range(grid_min_y, grid_max_y + 1):
            test_point = Point(i, j)

            if test_point in edge_points:
                debug_print(f"Skipping {test_point} as it is an edge")
                continue

            next_point = test_point
            debug_print(f"Testing {test_point}")
            edge_found = True
            for direction in CARDINAL_ADJACENT:
                if not edge_found:
                    debug_print("Skipping remaining directions")
                    break

                while True:
                    next_point = next_point + direction
                    debug_print(f"Taking step {next_point} from direction {direction}")

                    if next_point in edge_points:
                        debug_print(f"Found edge {next_point} for {test_point} from direction {direction}")
                        next_point = test_point
                        break

                    if (
                        next_point.x < grid_min_x
                        or next_point.x > grid_max_x
                        or next_point.y < grid_min_y
                        or next_point.y > grid_max_y
                    ):
                        debug_print(f"Encountered external point: {test_point}")
                        edge_found = False
                        break
            
            if edge_found:
                debug_print(f"{test_point} is internal")
                interior_points.add(test_point)
            # breakpoint()

    return len(interior_points.union(edge_points))


def part2(data):
    data = EXAMPLE_DATA



    return data
