from itertools import combinations

from common.grid import Point, get_vertical_slice

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


def get_manhatten_distance(a: Point, b: Point):
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_adjusted_manhatten_distance(grid, a: Point, b: Point, penalty=1):
    distance = get_manhatten_distance(a, b)

    min_x = min(a.x, b.x)
    max_x = max(a.x, b.x)
    extra_col_space = get_vertical_slice(grid, 0)[min_x:max_x].count("X")
    distance += extra_col_space * (penalty - 1)

    min_y = min(a.y, b.y)
    max_y = max(a.y, b.y)
    extra_row_space = grid[0][min_y:max_y].count("X")
    distance += extra_row_space * (penalty - 1)

    return distance


def find_expanded_space(grid):
    new_grid = []
    for row in grid:
        if "#" not in row:
            new_row = row.replace(".", "X")
            new_grid.append(list(new_row))
        else:
            new_grid.append(list(row))

    for col_no in range(len(grid[0])):
        col = get_vertical_slice(grid, col_no)
        if "#" not in col:
            for row in new_grid:
                row[col_no] = "X"

    return new_grid


def find_galaxies(grid):
    return [
        Point(i, j)
        for i, row in enumerate(grid)
        for j, col in enumerate(row)
        if col == "#"
    ]


def part1(data):
    # data = EXAMPLE_DATA
    initial_grid = data.splitlines()
    adjusted_grid = find_expanded_space(initial_grid)
    galaxies = find_galaxies(initial_grid)

    return sum(get_adjusted_manhatten_distance(adjusted_grid, a, b, penalty=2) for a, b in combinations(galaxies, 2))


def part2(data):
    # data = EXAMPLE_DATA
    initial_grid = data.splitlines()
    adjusted_grid = find_expanded_space(initial_grid)
    galaxies = find_galaxies(initial_grid)

    return sum(get_adjusted_manhatten_distance(adjusted_grid, a, b, penalty=1_000_000) for a, b in combinations(galaxies, 2))
