from common.grid import get_vertical_slice

EXAMPLE_DATA = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


def get_patterns(data):
    all_patterns = []

    current_pattern = []
    for line in data.splitlines():
        if line:
            current_pattern.append(line)
        else:
            all_patterns.append(current_pattern)
            current_pattern = []
    
    all_patterns.append(current_pattern)

    return all_patterns


def get_pattern_value(grid):
    for i in range(len(grid)):
        upper = i
        lower = i + 1

        while True:
            try:
                if grid[upper] != grid[lower]:
                    break

                upper -= 1
                lower += 1

                if upper < 0:
                    return 100 * (i + 1)
                    
            except IndexError:
                if i == len(grid) - 1:
                    # Don't match the last row against nothing
                    break
                return 100 * (i + 1)
    
    for i in range(len(grid[0])):
        left = i
        right = i + 1

        while True:
            try:
                if get_vertical_slice(grid, left) != get_vertical_slice(grid, right):
                    break
                
                left -= 1
                right += 1

                if left < 0:
                    return i + 1
                    
            except IndexError:
                return i + 1

    raise ValueError("No reflection detected")



def compare_lines(a, b):
    return sum(int(ela != elb) for ela, elb in zip(a, b))


def get_pattern_value_with_error(grid):
    for i in range(len(grid)):
        upper = i
        lower = i + 1
        found_error = False

        while True:
            try:
                value = compare_lines(grid[upper], grid[lower])
                if value > 2:
                    break

                if value == 1:
                    if found_error:
                        break
                    found_error = True

                upper -= 1
                lower += 1

                if upper < 0:
                    if not found_error:
                        break
                    return 100 * (i + 1)
                    
            except IndexError:
                if i == len(grid) - 1:
                    # Don't match the last row against nothing
                    break

                if not found_error:
                    break
                return 100 * (i + 1)
    
    for i in range(len(grid[0])):
        left = i
        right = i + 1
        found_error = False

        while True:
            try:
                value = compare_lines(get_vertical_slice(grid, left), get_vertical_slice(grid, right))
                if value > 2:
                    break

                if value == 1:
                    if found_error:
                        break
                    found_error = True
                
                left -= 1
                right += 1

                if left < 0:
                    if not found_error:
                        break
                    return i + 1
                    
            except IndexError:
                if not found_error:
                    break
                return i + 1

    raise ValueError("No reflection detected")


def part1(data):
    # data = EXAMPLE_DATA

    print([get_pattern_value(pattern) for pattern in get_patterns(data)])
    return sum(get_pattern_value(pattern) for pattern in get_patterns(data))


def part2(data):
    # data = EXAMPLE_DATA

    print([get_pattern_value_with_error(pattern) for pattern in get_patterns(data)])
    return sum(get_pattern_value_with_error(pattern) for pattern in get_patterns(data))
