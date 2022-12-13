from collections import deque
from aocd import get_data, submit

data = get_data(day=12, year=2022)
# data = """Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi"""

SCALE = "abcdefghijklmnopqrstuvwxyz"

GRID = [[char for char in line] for line in data.splitlines()]

class Point:
    def __init__(self, x, y, distance):
        self.x = x
        self.y = y
        self.distance = distance

    def __repr__(self):
        return f"Point ({self.x}, {self.y}). Distance: {self.distance}"

    @property
    def coordinate(self):
        return self.x, self.y

possible_starts = []
distances = []
target = None
for i, row in enumerate(GRID):
    for j, location in enumerate(row):
        if location == "S":
            start = Point(i, j, 0)
            possible_starts.append(start)
            GRID[i][j] = "a"

        if location == "E":
            target = i, j
            GRID[i][j] = "z"

        if location == "a":
            start = Point(i, j, 0)
            possible_starts.append(start)


for n, start in enumerate(possible_starts):
    seen = set()
    to_visit = deque()

    def queue_if_reachable(point: Point, target: Point):
        if target.coordinate in seen:
            return

        point_height = GRID[point.x][point.y]
        target_height = GRID[target.x][target.y]

        if SCALE.index(target_height) <= SCALE.index(point_height) + 1:
            seen.add(target.coordinate)
            to_visit.append(target)


    def get_adjacent(point):
        x, y = point.x, point.y
        if x > 0:
            target = Point(x - 1, y, point.distance + 1)
            queue_if_reachable(point, target)

        if x < len(GRID) - 1:
            target = Point(x + 1, y, point.distance + 1)
            queue_if_reachable(point, target)

        if y > 0:
            target = Point(x, y - 1, point.distance + 1)
            queue_if_reachable(point, target)

        if y < len(GRID[0]) - 1:
            target = Point(x, y + 1, point.distance + 1)
            queue_if_reachable(point, target)

    points = []
    
    to_visit.append(start)
    seen.add(start.coordinate)

    while len(to_visit):
        point = to_visit.popleft()

        points.append(point)
        get_adjacent(point)


    for point in points:
        if point.coordinate == target:
            break
    else:
        continue

    distances.append(point.distance)

print(distances)
print(min(distances))
# submit(min_distances, part="b", day=12, year=2022)