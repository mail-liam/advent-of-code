from collections import defaultdict, deque

from common.grid import DistancePoint, CARDINAL_ADJACENT

EXAMPLE_DATA = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


def get_manhatten_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def part1(data):
    # data = EXAMPLE_DATA
    DISTANCE_REQUIRED = 64

    grid = data.splitlines()

    start_point = None
    for i, row in enumerate(grid):
        if (j := row.find("S")) != -1:
            start_point = DistancePoint(i, j)
            break

    seen_for_distance = defaultdict(set)
    queue = deque()
    queue.append(start_point)
    final_positions = set()
    seen_for_distance[start_point.distance].add(start_point)
    while queue:
        current_point = queue.popleft()

        for direction in CARDINAL_ADJACENT:
            next_point = current_point + direction

            if next_point in seen_for_distance[next_point.distance]:
                continue

            if grid[next_point.x][next_point.y] == "#":
                continue

            if next_point.distance == DISTANCE_REQUIRED:
                final_positions.add(next_point)
                continue

            seen_for_distance[next_point.distance].add(next_point)
            queue.append(next_point)

    return len(final_positions)


def extrapolate_grid(extra_gardens, odd_value, even_value):
    if extra_gardens % 2 == 0:
        odd_count = extra_gardens
        even_count = extra_gardens + 1
    else:
        odd_count = extra_gardens + 1
        even_count = extra_gardens
    
    return odd_count ** 2 * odd_value + even_count ** 2 * even_value


def part2(data):
    # data = EXAMPLE_DATA
    DISTANCE_REQUIRED = 100

    grid = data.splitlines()
    X_MAX = len(grid)
    Y_MAX = len(grid[0])

    start_point = None
    for i, row in enumerate(grid):
        if (j := row.find("S")) != -1:
            start_point = DistancePoint(i, j)
    
    seen = set()
    seen.add(start_point)
    queue = deque()
    queue.append(start_point)
    evens = set()
    while queue:
        current_point = queue.popleft()

        if current_point.distance % 2 == 0:
            evens.add(current_point)

        for direction in CARDINAL_ADJACENT:
            next_point = current_point + direction

            if next_point in seen:
                continue

            if next_point.x < 0 or next_point.y < 0:
                continue

            try:
                if grid[next_point.x][next_point.y] == "#":
                    continue
            except IndexError:
                continue

            seen.add(next_point)
            queue.append(next_point)

    odd_value, even_value = len(seen - evens), len(evens)
    print(odd_value, even_value)
    print("------------")
    print(extrapolate_grid(0, odd_value, even_value))
    print(extrapolate_grid(1, odd_value, even_value))
    

    adjusted_base = DISTANCE_REQUIRED - get_manhatten_distance(start_point, DistancePoint(0, start_point.y))
    full_gardens, extra_steps = divmod(adjusted_base, X_MAX)  # Or y, we start in the center
    extra_steps -= full_gardens + 1  # Stepping from 1 garden to the next

    return adjusted_base, full_gardens, extra_steps
