import re
import typing as t
from collections import defaultdict

from aocd import get_data, submit

data = get_data(day=22, year=2022)
# data = """        ...#
#         .#..
#         #...
#         ....
# ...#.......#
# ........#...
# ..#....#....
# ..........#.
#         ...#....
#         .....#..
#         .#......
#         ......#.

# 10R5L5R10L4R5L5"""


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point ({self.x}, {self.y})"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    @property
    def coordinate(self):
        return self.x, self.y


class Grid:
    FACING_MAP = {
        0: Point(0, 1),
        1: Point(1, 0),
        2: Point(0, -1),
        3: Point(-1, 0),
    }

    def __init__(self):
        self._grid = defaultdict(lambda: " ")
        self.point = None
        self.col_max = None
        self.row_max = None
        self.facing = 0

    def add_point(self, row, col, data):
        self._grid[(row, col)] = data

    def get_point_data(self, row, col):
        return self._grid[(row, col)]

    def initialize(self):
        if not self._grid:
            raise ValueError("No grid data")

        self.row_max = max(key[0] for key in self._grid)
        self.col_max = max(key[1] for key in self._grid)

        for col in range(self.col_max + 1):
            if self.get_point_data(0, col) == ".":
                self.point = Point(0, col)
                break
    @property
    def coordinate(self):
        return self.point.coordinate

    def update_facing(self, direction: t.Literal["L", "R"]):
        dir_num = 1 if direction == "R" else -1
        self.facing = (self.facing + dir_num) % 4
        # print(f"Updated facing to {self.facing}")

    def score(self):
        row_num, col_num = self.point.x + 1, self.point.y + 1  # Ew 1-based indexing
        return row_num * 1000 + col_num * 4 + self.facing

    def take_step(self) -> bool:
        """Take a step toward the current facing. Return False if could not take a step."""

        desired_target = self.point + self.FACING_MAP[self.facing]
        point_data = self._grid[desired_target.coordinate]

        if point_data == "#":
            # print("Unable to take step.")
            return False

        if point_data == ".":
            self.point = desired_target
            # print(f"Moving to {desired_target}")
            return True

        # Wrap around
        if point_data == " ":
            # print("Wrapping around")
            match self.facing:
                case 0:
                    current_row = self.coordinate[0]
                    search_range = ((current_row, col) for col in range(self.col_max + 1))
                case 1:
                    current_col = self.coordinate[1]
                    search_range = ((row, current_col) for row in range(self.row_max + 1))
                case 2:
                    current_row = self.coordinate[0]
                    search_range = ((current_row, col) for col in range(self.col_max, -1, -1))  # start, stop, step
                case 3:
                    current_col = self.coordinate[1]
                    search_range = ((row, current_col) for row in range(self.row_max, -1, -1))
                case _:
                    raise ValueError(f"Unknown facing: {self.facing}")

            for coordinate in search_range:
                point_data = self.get_point_data(*coordinate)
                if point_data == "#":
                    # print("Unable to take step.")
                    return False

                if point_data == ".":
                    new_point = Point(*coordinate)
                    # print(f"Moving to {new_point}")
                    self.point = new_point
                    return True
            raise ValueError(f"Unable to wrap around on grid! (from {self.point})")

        raise ValueError(f"Invalid point_data found: {point_data}")


grid = Grid()
for row_num, row_data in enumerate(data.splitlines()):
    if not row_data.strip():
        break

    for col_num, grid_section in enumerate(row_data):
        grid.add_point(row_num, col_num, grid_section)

# print(data.splitlines()[-1])
instructions = re.findall("\d+\w?", data.splitlines()[-1])
grid.initialize()

for instruction in instructions:
    try:
        step_count, facing_change = int(instruction[:-1]), instruction[-1]
    except ValueError:  # Final step with no facing change
        step_count, facing_change = int(instruction), None

    for _ in range(step_count):
        if not grid.take_step():
            break

    if facing_change:
        grid.update_facing(facing_change)


print(grid.score())
submit(grid.score(), part="a", day=22, year=2022)