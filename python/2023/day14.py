import itertools
from copy import deepcopy

from common.grid import get_vertical_slice

EXAMPLE_DATA = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def slide_rocks(row):
    adjusted = True

    while adjusted:
        adjusted = False

        for i, j in itertools.pairwise(range(len(row))):
            if row[i] == "." and row[j] == "O":
                row[i], row[j] = "O", "."
                adjusted = True

    return row


def part1(data):
    # data = EXAMPLE_DATA

    grid = data.splitlines()

    total = 0
    for i in range(len(grid[0])):
        column = get_vertical_slice(grid, i)
        sorted_column = slide_rocks(column)

        total += sum(
            weight
            for char, weight in zip(sorted_column, range(len(sorted_column), 0, -1))
            if char == "O"
        )

    return total


def part2(data):
    data = EXAMPLE_DATA

    grid = [list(line) for line in data.splitlines()]


    prev_grid = None
    for _ in range(1_000_000_000):
        if prev_grid == grid:
            break
        prev_grid = deepcopy(grid)

        # Slide north
        for i in range(len(grid[0])):
            column = get_vertical_slice(grid, i)
            sorted_column = slide_rocks(column)

            for j, row in enumerate(grid):
                row[i] = sorted_column[j]

        # Slide west
        for i, row in enumerate(grid):
            grid[i] = slide_rocks(row)

        # Slide south
        for i in range(len(grid[0])):
            column = list(reversed(get_vertical_slice(grid, i)))
            sorted_column = list(reversed(slide_rocks(column)))

            for j, row in enumerate(grid):
                row[i] = sorted_column[j]

        # Slide east
        for i, row in enumerate(grid):
            sorted_row = list(reversed(row))
            grid[i] = list(reversed(slide_rocks(sorted_row)))


    total = 0
    for i in range(len(grid[0])):
        column = get_vertical_slice(grid, i)
        sorted_column = slide_rocks(column)

        total += sum(
            weight
            for char, weight in zip(sorted_column, range(len(sorted_column), 0, -1))
            if char == "O"
        )

    return total


def print_grid(grid):
    for row in grid:
        print(row)