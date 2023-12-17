from collections import defaultdict, deque

from common.grid import NORTH, SOUTH, EAST, WEST, CARDINAL_ADJACENT, DistancePoint, Point

EXAMPLE_DATA = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""


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


def get_pipe_segments(grid, start):
    seen = set()
    seen.add(start)
    to_check = deque()
    # Find pipes pointing to start
    for direction in CARDINAL_ADJACENT:
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

    return seen


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

    pipes = get_pipe_segments(grid, start)

    furthest_point = sorted(pipes, key=lambda p: p.distance, reverse=True)[0]
    return furthest_point.distance


# def part2_trace(data):
#     data = EXAMPLE_DATA
#     grid = [line for line in data.splitlines()]

#     start = None
#     for row_num, row in enumerate(grid):
#         if "S" not in row:
#             continue

#         col_num = row.index("S")

#         start = DistancePoint(x=row_num, y=col_num, distance=0)
#         break

#     pipes = get_pipe_segments(grid, start)
#     enclosed_spaces = set()

#     ROW_MAX = len(grid) - 1
#     COL_MAX = len(grid[0]) - 1
#     for i, row in enumerate(grid):
#         for j, _ in enumerate(row):
#             initial_point = Point(i, j)
#             current_point = initial_point
#             if current_point in pipes:
#                 continue

#             x_min = current_point.x
#             x_max = ROW_MAX - x_min
#             y_min = current_point.y
#             y_max = COL_MAX - y_min
#             min_distance_to_edge = min((x_min, x_max, y_min, y_max))

#             if min_distance_to_edge == x_min:
#                 direction = NORTH
#                 attribute = "x"
#                 target = 0
#             elif min_distance_to_edge == x_max:
#                 direction = SOUTH
#                 attribute = "x"
#                 target = ROW_MAX
#             elif min_distance_to_edge == y_min:
#                 direction = WEST
#                 attribute = "y"
#                 target = 0
#             else:
#                 direction = EAST
#                 attribute = "y"
#                 target = COL_MAX

#             total_pipes_crossed = 0
#             print(f"Target is: {attribute}={target}")
#             while getattr(current_point, attribute) != target:
#                 print(f"Currently at {current_point}")
                
#                 current_point = current_point + direction
#                 print(f"Moved to {current_point}")
#                 if current_point in pipes:
#                     print(f"{current_point} is a pipe crossing")
#                     total_pipes_crossed += 1

#                 print("-----------------")
#                 breakpoint()

#             if total_pipes_crossed % 2 != 0:
#                 enclosed_spaces.add(initial_point)

#     return len(enclosed_spaces)


ZOOM_AND_ENHANCE = {
    ".": [
        "...",
        "...",
        "...",
    ],
    "|": [
        ".#.",
        ".#.",
        ".#.",
    ],
    "-": [
        "...",
        "###",
        "...",
    ],
    "L": [
        ".#.",
        ".##",
        "...",
    ],
    "J": [
        ".#.",
        "##.",
        "...",
    ],
    "7": [
        "...",
        "##.",
        ".#.",
    ],
    "F": [
        "...",
        ".##",
        ".#.",
    ],
    "S": [
        ".#.",
        "###",
        ".#.",
    ],
}


def part2(data):
    # data = EXAMPLE_DATA

    grid = [line for line in data.splitlines()]

    start = None
    for row_num, row in enumerate(grid):
        if "S" not in row:
            continue

        col_num = row.index("S")

        start = DistancePoint(x=row_num, y=col_num, distance=0)
        break

    pipes = get_pipe_segments(grid, start)

    all_points = set()
    enhanced_grid = defaultdict(str)
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            all_points.add(Point(i, j))

            enhanced_segment = ZOOM_AND_ENHANCE[col]
            for k in range(3):
                enhanced_grid[3*i+k] += enhanced_segment[k]

    # for row in enhanced_grid.values():
    #     print(row)

    seen = set()
    seen_enhanced = set()
    seen_enhanced.add(Point(0, 0))
    to_check = deque()
    to_check.append(Point(0, 0))
    while to_check:
        current_point = to_check.popleft()
        seen.add(Point(current_point.x // 3, current_point.y // 3))

        for direction in ADJACENT_POINTS:
            new_point = current_point + direction

            if new_point.x < 0 or new_point.y < 0:
                continue

            try:
                point_data = enhanced_grid[new_point.x][new_point.y]
            except IndexError:
                continue

            if point_data == "." and new_point not in seen_enhanced:
                to_check.append(new_point)
                seen_enhanced.add(new_point)

        # print(f"Global seen: {seen}")
        # print(f"Enhanced seen: {seen_enhanced}")
        # print(f"Queue: {to_check}")
        # print("------------")
        # breakpoint()

    return len(all_points - pipes - seen)
