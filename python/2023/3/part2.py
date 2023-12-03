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

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point ({self.x}, {self.y})"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash(self.coordinate)

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

result = sum(gear_ratios)
print(result)
submit(result, part="b", day=3, year=2023)