from itertools import combinations

from common.grid import Point

EXAMPLE_DATA = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
EXPANSION_CONSTANT = 1_000_000


def get_vertical_slice(grid, col: int):
    return [row[col] for row in grid]


def get_manhatten_distance(a: Point, b: Point):
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_adjusted_manhatten_distance(grid, a: Point, b: Point):
    # print(f"Calculating distance between {a} and {b}")
    distance = get_manhatten_distance(a, b)
    # print(f"base distance: {distance}")

    min_x = min(a.x, b.x)
    max_x = max(a.x, b.x)

    extra_col_space = get_vertical_slice(grid, 0)[min_x:max_x].count("X")
    # print(f"col_slice for {min_x}, {max_x}: {get_vertical_slice(grid, 0)[min_x:max_x]}")
    distance += extra_col_space * (EXPANSION_CONSTANT - 1)

    min_y = min(a.y, b.y)
    max_y = max(a.y, b.y)

    extra_row_space = grid[0][min_y:max_y].count("X")
    # print(f"row_slice for {min_y}, {max_y}: {grid[0][min_y:max_y]}")
    distance += extra_row_space * (EXPANSION_CONSTANT - 1)
    # print(distance)
    # print("-------------------------------")
    # breakpoint()

    return distance



def part1(data):
    # data = EXAMPLE_DATA

    initial_grid = data.splitlines()
    expanded_grid = []

    for row in initial_grid:
        expanded_grid.append(list(row))
        if "#" not in row:
            expanded_grid.append(list(row))

    offset = 0
    for col_no in range(len(initial_grid[0])):
        col = get_vertical_slice(initial_grid, col_no)
        if "#" not in col:
            for row in expanded_grid:
                row.insert(col_no + offset, ".")
            offset += 1

    points = []
    for i, row in enumerate(expanded_grid):
        for j, col in enumerate(row):
            if col == "#":
                points.append(Point(i, j))

    return sum(get_manhatten_distance(a, b) for a, b in combinations(points, 2))


def part2(data):
    # data = EXAMPLE_DATA

    initial_grid = data.splitlines()
    adjusted_grid = []

    for row in initial_grid:
        if "#" not in row:
            new_row = row.replace(".", "X")
            adjusted_grid.append(list(new_row))
        else:
            adjusted_grid.append(list(row))

    for col_no in range(len(initial_grid[0])):
        col = get_vertical_slice(initial_grid, col_no)
        if "#" not in col:
            for row in adjusted_grid:
                row[col_no] = "X"

    # for row in adjusted_grid:
    #     print(row)

    points = []
    for i, row in enumerate(initial_grid):
        for j, col in enumerate(row):
            if col == "#":
                points.append(Point(i, j))

    return sum(get_adjusted_manhatten_distance(adjusted_grid, a, b) for a, b in combinations(points, 2))

# 82000210