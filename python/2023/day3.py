from common.grid import ADJACENT_SQUARES, Point


EXAMPLE_DATA = """467..114..
...*......
..35...633
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def part1(data):
    # data = EXAMPLE_DATA

    INVALID_SYMBOLS = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."}
    class GridNumber:
        def __init__(self, points, value):
            self.points = points
            self.value = value

        def __repr__(self):
            return f"GridNumber: {self.value}"

    grid = data.splitlines()

    ALL_NUMS = []
    for row_num, row in enumerate(grid):
        current_numbers = []
        current_points = []
        for col_num, char in enumerate(row):
            if char.isdigit():
                current_numbers.append(char)
                current_points.append(Point(row_num, col_num))
            else:
                if current_numbers:
                    num_value = int("".join(current_numbers))
                    ALL_NUMS.append(GridNumber(points=current_points, value=num_value))
                current_numbers = []
                current_points = []

        if current_numbers:
            num_value = int("".join(current_numbers))
            ALL_NUMS.append(GridNumber(points=current_points, value=num_value))


    VALID_NUMBERS = []
    for num in ALL_NUMS:
        valid = False
        for point in num.points:
            if valid:
                break
            for neighbor in ADJACENT_SQUARES:
                grid_loc = point + neighbor
                row, col = grid_loc.coordinate

                if row < 0 or col < 0:
                    continue

                try:
                    symbol = grid[row][col]
                except IndexError:
                    continue

                if symbol not in INVALID_SYMBOLS:
                    VALID_NUMBERS.append(num)
                    valid = True
                    break

    return sum(num.value for num in VALID_NUMBERS)


def part2(data):
    # data = EXAMPLE_DATA
    grid = data.splitlines()

    class GridNumber:
        def __init__(self, points, value):
            self.points = points
            self.value = value
            self.gear = None

        def __repr__(self):
            return f"GridNumber: {self.value}"


    ALL_NUMS = []
    for row_num, row in enumerate(grid):
        current_numbers = []
        current_points = []
        for col_num, char in enumerate(row):
            if char.isdigit():
                current_numbers.append(char)
                current_points.append(Point(row_num, col_num))
            else:
                if current_numbers:
                    num_value = int("".join(current_numbers))
                    ALL_NUMS.append(GridNumber(points=current_points, value=num_value))
                current_numbers = []
                current_points = []

        if current_numbers:
            num_value = int("".join(current_numbers))
            ALL_NUMS.append(GridNumber(points=current_points, value=num_value))


    GEAR_NUMS = []
    GEARS = set()
    for num in ALL_NUMS:
        valid = False
        for point in num.points:
            if valid:
                break
            for neighbor in ADJACENT_SQUARES:
                grid_loc = point + neighbor
                row, col = grid_loc.coordinate

                if row < 0 or col < 0:
                    continue

                try:
                    symbol = grid[row][col]
                except IndexError:
                    continue

                if symbol == "*":
                    num.gear = grid_loc
                    GEAR_NUMS.append(num)
                    GEARS.add(grid_loc)
                    valid = True
                    break

    gear_ratios = []
    for gear in GEARS:
        nums_for_gear = [num for num in GEAR_NUMS if num.gear == gear]
        if len(nums_for_gear) != 2:
            continue
        gear_ratios.append(nums_for_gear[0].value * nums_for_gear[1].value)

    return sum(gear_ratios)