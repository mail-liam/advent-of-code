from collections import deque
from itertools import chain

from common.grid import Point, NORTH, EAST, SOUTH, WEST

DEBUG = False
EXAMPLE_DATA = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""

def debug_print(message):
    if DEBUG:
        print(message)


DIRECTION_TO_POINT = {"N": NORTH, "E": EAST, "S": SOUTH, "W": WEST}
SPLITTER_MAP = {
    ("/", "N"): ("E",),
    ("/", "W"): ("S",),
    ("/", "S"): ("W",),
    ("/", "E"): ("N",),
    ("\\", "N"): ("W",),
    ("\\", "W"): ("N",),
    ("\\", "S"): ("E",),
    ("\\", "E"): ("S",),
    ("|", "N"): ("N",),
    ("|", "W"): ("N", "S"),
    ("|", "S"): ("S",),
    ("|", "E"): ("N", "S"),
    ("-", "N"): ("W", "E"),
    ("-", "W"): ("W"),
    ("-", "S"): ("W", "E"),
    ("-", "E"): ("E"),
}

def get_new_directions(map_point, direction):
    if map_point == ".":
        return direction
    
    return SPLITTER_MAP[(map_point, direction)]


class DirectionPoint(Point):
    def __init__(self, x, y, direction):
        super().__init__(x, y)
        self.direction = direction

    def __repr__(self):
        return f"DirectionPoint ({self.x}, {self.y}) [{self.direction}]"
    
    def __hash__(self):
        return hash((self.x, self.y, self.direction))
    
    @classmethod
    def from_point(cls, point, direction):
        return cls(point.x, point.y, direction)
    

def energize_grid(grid, start_point):
    visited_with_direction = set()
    queue = deque()
    queue.append(start_point)

    while queue:
        # breakpoint()
        current_point = queue.popleft()
        debug_print(f"Coming from: {current_point}")
        next_point = current_point + DIRECTION_TO_POINT[current_point.direction]
        debug_print(f"Arriving at: {next_point}")

        if next_point.x < 0 or next_point.y < 0:
            debug_print("Skipping as outside grid")
            continue

        try:
            map_point = grid[next_point.x][next_point.y]
        except IndexError:
            debug_print("Skipping as outside grid")
            continue

        debug_print(f"Found {map_point}")
        for direction in get_new_directions(map_point, current_point.direction):
            point_to_queue = DirectionPoint.from_point(next_point, direction)
            if point_to_queue not in visited_with_direction:
                debug_print(f"Queuing {point_to_queue}")
                queue.append(point_to_queue)
                visited_with_direction.add(point_to_queue)
            else:
                debug_print("Skipping as already visited from this direction")

    return len({(point.x, point.y) for point in visited_with_direction})


def part1(data):
    # data = EXAMPLE_DATA

    grid = data.splitlines()

    return energize_grid(grid, DirectionPoint(0, -1, "E"))


def part2(data):
    # data = EXAMPLE_DATA

    grid = data.splitlines()

    grid_h_size = len(grid[0])
    grid_v_size = len(grid)

    north_starts = [DirectionPoint(-1, i, "S") for i in range(grid_h_size)]
    east_starts = [DirectionPoint(i, grid_v_size, "W") for i in range(grid_v_size - 1, -1, -1)]
    south_starts = [DirectionPoint(grid_h_size, i, "N") for i in range(grid_h_size - 1, -1, -1)]
    west_starts = [DirectionPoint(i, -1, "E") for i in range(grid_v_size)]

    return max(energize_grid(grid, start_point) for start_point in chain(north_starts, east_starts, south_starts, west_starts))
