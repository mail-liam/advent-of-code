from collections import deque

from common.grid import CARDINAL_ADJACENT, DistancePoint

EXAMPLE_DATA = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
SCALE = "abcdefghijklmnopqrstuvwxyz"


def find_target_point(grid: list[str], start: DistancePoint, target: DistancePoint):
    seen = set()
    to_visit = deque()
    to_visit.append(start)
    seen.add(start)

    while len(to_visit):
        point = to_visit.popleft()

        if point == target:
            return point
        
        for direction in CARDINAL_ADJACENT:
            next_point = point + direction

            if next_point in seen or next_point.x < 0 or next_point.y < 0:
                continue

            try:
                point_height = grid[point.x][point.y]
                next_height = grid[next_point.x][next_point.y]
            except IndexError:
                continue

            if SCALE.index(next_height) <= SCALE.index(point_height) + 1:
                seen.add(next_point)
                to_visit.append(next_point)

    # Start with no valid path
    return DistancePoint(-1, -1, distance=999_999_999)


def part1(data):
    # data = EXAMPLE_DATA

    GRID = [line for line in data.splitlines()]

    start = None
    target = None
    for i, row in enumerate(GRID):
        for j, location in enumerate(row):
            if location == "S":
                start = DistancePoint(i, j)

            if location == "E":
                target = DistancePoint(i, j)

    GRID[start.x] = GRID[start.x].replace("S", "a")
    GRID[target.x] = GRID[target.x].replace("E", "z")

    target_with_distance = find_target_point(GRID, start, target)

    return target_with_distance.distance


def part2(data):
    # data = EXAMPLE_DATA

    GRID = [line for line in data.splitlines()]

    possible_starts = []
    target = None
    start_row = None
    for i, row in enumerate(GRID):
        for j, location in enumerate(row):
            if location == "S":
                start = DistancePoint(i, j)
                possible_starts.append(start)
                start_row = i

            if location == "E":
                target = DistancePoint(i, j)

            if location == "a":
                start = DistancePoint(i, j)
                possible_starts.append(start)

    GRID[start_row] = GRID[start_row].replace("S", "a")
    GRID[target.x] = GRID[target.x].replace("E", "z")

    return min(find_target_point(GRID, start, target).distance for start in possible_starts)