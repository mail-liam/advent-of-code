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

# # 10R5L5R10L4R5L5"""



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

POINT_TRANSFORM = {
    **{(old_row, 149, 0): (Point(new_row, 99), 2) for old_row, new_row in zip(range(50), range(149, 99, -1))},          # A2 -> A5
    **{(old_row, 99, 0): (Point(new_row, 149), 2) for old_row, new_row in zip(range(100, 150), range(49, -1, -1))},     # A5 -> A2
    **{(149, old_col, 1): (Point(new_row, 49), 2) for old_col, new_row in zip(range(50, 100), range(150, 200))},        # B5 -> B6
    **{(old_row, 49, 0): (Point(149, new_col), 3) for old_row, new_col in zip(range(150,200), range(50, 100))},         # B6 -> B5
    **{(0, old_col, 3): (Point(199, new_col), 3) for old_col, new_col in zip(range(100, 150), range(50))},              # C2 -> C6
    **{(199, old_col, 1): (Point(0, new_col), 1) for old_col, new_col in zip(range(50), range(100, 150))},              # C6 -> C2
    **{(0, old_col, 3): (Point(new_row, 0), 0) for old_col, new_row in zip(range(50, 100), range(150,200))},            # D1 -> D6
    **{(old_row, 0 , 2): (Point(0, new_col), 1) for old_row, new_col in zip(range(150, 200), range(50, 100))},          # D6 -> D1
    **{(old_row, 50, 2): (Point(new_row, 0), 0) for old_row, new_row in zip(range(50), range(149, 99, -1))},            # E1 -> E4
    **{(old_row, 0, 2): (Point(new_row, 50), 0) for old_row, new_row in zip(range(100, 150), range(49, -1, -1))},       # E4 -> E1
    **{(old_row, 50, 2): (Point(100, new_col), 1) for old_row, new_col in zip(range(50, 100), range(50))},              # F3 -> F4
    **{(100, old_col, 3): (Point(new_row, 50), 0) for old_col, new_row in zip(range(50), range(50, 100))},              # F4 -> F3
    **{(49, old_col, 1): (Point(new_row, 99), 2) for old_col, new_row in zip(range(100, 150), range(50, 100))},         # G2 -> G3
    **{(old_row, 99, 0): (Point(49, new_col), 3) for old_row, new_col in zip(range(50, 100), range(100, 150))},         # G3 -> G2
}


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
        match direction:
            case "R":
                dir_num = 1
            case "L":
                dir_num = -1
            case _:
                raise ValueError(f"Unexpected direction: {direction}")

        self.facing = (self.facing + dir_num) % 4
        # print(f"Updated facing to {self.facing}")

    def score(self):
        row_num, col_num = self.point.x + 1, self.point.y + 1  # Ew 1-based indexing
        return row_num * 1000 + col_num * 4 + self.facing

    def take_step(self) -> bool:
        """Take a step toward the current facing. Return False if could not take a step."""

        desired_target = self.point + self.FACING_MAP[self.facing]
        point_data = self._grid[desired_target.coordinate]
        new_facing = None

        # Check for wrap around
        if point_data == " ":
            # print("Getting new position from cube map")
            desired_target, new_facing = POINT_TRANSFORM[(self.point.x, self.point.y, self.facing)]
            point_data = self._grid[desired_target.coordinate]

        if point_data == "#":
            # print("Unable to take step.")
            return False

        if point_data == ".":
            # print(f"Moving to {desired_target}")
            self.point = desired_target
            if new_facing is not None:
                self.facing = new_facing
                # print(f"Facing is now {self.facing}")
            return True

        raise ValueError(f"Invalid point_data found: {point_data}")


grid = Grid()
for row_num, row_data in enumerate(data.splitlines()):
    if not row_data.strip():
        break

    for col_num, grid_section in enumerate(row_data):
        grid.add_point(row_num, col_num, grid_section)

instructions = re.findall("\d+\w?", data.splitlines()[-1])
grid.initialize()

for instruction in instructions:
    # print("---------------------------")
    try:
        step_count, facing_change = int(instruction[:-1]), instruction[-1]
    except ValueError:  # Final step with no facing change
        step_count, facing_change = int(instruction), None

    # print(step_count, facing_change)
    for _ in range(step_count):
        if not grid.take_step():
            break

    if facing_change:
        grid.update_facing(facing_change)


print(grid.score())
# submit(total, part="b", day=22, year=2022)