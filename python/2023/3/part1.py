from aocd import get_data, submit

data = get_data(day=3, year=2023)
# data = """467..114..
# ...*......
# ..35...633
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598.."""

grid = data.splitlines()

ALL_NUMS = []


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point ({self.x}, {self.y})"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __hash__(self):
        return self.coordinate

    @property
    def coordinate(self):
        return self.x, self.y

NORTH_WEST = Point(-1, -1)
NORTH = Point(-1, 0)
NORTH_EAST = Point(-1, 1)
WEST = Point(0, -1)
EAST = Point(0, 1)
SOUTH_WEST = Point(1, -1)
SOUTH = Point(1, 0)
SOUTH_EAST = Point(1, 1)
ADJACENT_SQUARES = [
    NORTH_WEST,
    NORTH,
    NORTH_EAST,
    WEST,
    EAST,
    SOUTH_WEST,
    SOUTH,
    SOUTH_EAST,
]

INVALID_SYMBOLS = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."}
    

class GridNumber:
    def __init__(self, points, value):
        self.points = points
        self.value = value

    def __repr__(self):
        return f"GridNumber: {self.value}"


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

result = sum(num.value for num in VALID_NUMBERS)
print(result)
submit(result, part="a", day=3, year=2023)