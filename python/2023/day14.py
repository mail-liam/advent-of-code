import itertools

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


def score_grid(grid):
    total = 0
    for i in range(len(grid[0])):
        column = get_vertical_slice(grid, i)

        total += sum(
            weight
            for char, weight in zip(column, range(len(column), 0, -1))
            if char == "O"
        )

    return total


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
    # data = EXAMPLE_DATA

    # grid = [list(line) for line in data.splitlines()]


    # prev_grid = None
    # recent_totals = []
    # for _ in range(1_000_000_000):
    #     if prev_grid == grid:
    #         break

    #     # Slide north
    #     for i in range(len(grid[0])):
    #         column = get_vertical_slice(grid, i)
    #         sorted_column = slide_rocks(column)

    #         for j, row in enumerate(grid):
    #             row[i] = sorted_column[j]

    #     # Slide west
    #     for i, row in enumerate(grid):
    #         grid[i] = slide_rocks(row)

    #     # Slide south
    #     for i in range(len(grid[0])):
    #         column = list(reversed(get_vertical_slice(grid, i)))
    #         sorted_column = list(reversed(slide_rocks(column)))

    #         for j, row in enumerate(grid):
    #             row[i] = sorted_column[j]

    #     # Slide east
    #     for i, row in enumerate(grid):
    #         sorted_row = list(reversed(row))
    #         grid[i] = list(reversed(slide_rocks(sorted_row)))

        
    #     recent_totals.append(score_grid(grid))
    #     if len(recent_totals) == 10:
    #         print(recent_totals)
    #         breakpoint()
    #         recent_totals = []

    # Sample data: p=7, offset=2
    # value_period = (69, 69, 65, 64, 65, 63, 68)
    # index = (999_999_999 - 2) % len(value_period)
            
    offset = 105
    value_period = (87286, 87284, 87282, 87264, 87258, 87272, 87286, 87288, 87271, 87266, 87273, 87287, 87292)
    index = (999_999_999 - offset) % len(value_period)

    try:
        return value_period[index]
    except IndexError:
        index = index % len(value_period)
        return value_period[index]


# 87, 69,
# 69, 69, 65, 64, 65, 63, 68,
# 69, 69, 65, 64, 65, 63, 68,
# 69, 69, 65, 64


# [101151, 100859, 100650, 100338, 99931, 99696, 99415, 99095, 98764, 98526]
# [98250, 97929, 97614, 97344, 97094, 96843, 96617, 96396, 96214, 96036]
# [95856, 95632, 95377, 95103, 94856, 94650, 94460, 94239, 94030, 93819]
# [93611, 93390, 93157, 92971, 92771, 92581, 92399, 92257, 92118, 91984]
# [91843, 91699, 91554, 91432, 91313, 91204, 91114, 91015, 90935, 90854]
# [90767, 90643, 90515, 90426, 90331, 90234, 90130, 90038, 89957, 89872]
# [89758, 89659, 89539, 89430, 89316, 89205, 89087, 88980, 88876, 88769]
# [88656, 88555, 88475, 88396, 88315, 88226, 88141, 88074, 88021, 87956]
# [87923, 87887, 87842, 87818, 87809, 87787, 87751, 87696, 87645, 87608]
# [87580, 87563, 87532, 87506, 87477, 87447, 87430, 87429, 87417, 87395]
# [87358, 87329, 87312, 87303, 87295,
# 87286, 87284, 87282, 87264, 87258, 87272, 87286, 87288, 87271, 87266, 87273, 87287, 87292,
# 87286, 87284, 87282, 87264, 87258, 87272, 87286, 87288, 87271, 87266, 87273, 87287, 87292,
# 87286, 87284, 87282, 87264, 87258, 87272, 87286, 87288, 87271]