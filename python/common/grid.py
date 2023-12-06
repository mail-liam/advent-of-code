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
    

class DistancePoint(Point):
    def __init__(self, *args, distance=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.distance = distance

    def __repr__(self):
        return f"DistancePoint ({self.x}, {self.y}) [{self.distance}]"

    def __add__(self, other):
        return DistancePoint(self.x + other.x, self.y + other.y, distance=self.distance + 1)


NORTH_WEST = Point(-1, -1)
NORTH = Point(-1, 0)
NORTH_EAST = Point(-1, 1)
WEST = Point(0, -1)
EAST = Point(0, 1)
SOUTH_WEST = Point(1, -1)
SOUTH = Point(1, 0)
SOUTH_EAST = Point(1, 1)

CARDINAL_ADJACENT = (NORTH, EAST, SOUTH, WEST)
ADJACENT_SQUARES = (
    NORTH_WEST, NORTH, NORTH_EAST, WEST, EAST, SOUTH_WEST, SOUTH, SOUTH_EAST
)
CARDINAL_TO_POINTS = {
    "N": [NORTH_WEST, NORTH, NORTH_EAST],
    "S": [SOUTH_WEST, SOUTH, SOUTH_EAST],
    "W": [NORTH_WEST, WEST, SOUTH_WEST],
    "E": [NORTH_EAST, EAST, SOUTH_EAST],
}


def get_vertical_slice(grid, col: int):
    return [row[col] for row in grid]
