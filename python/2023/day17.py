from common.grid import Point, CARDINAL_ADJACENT

DEBUG = False
EXAMPLE_DATA = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

OPPOSITE = {
    CARDINAL_ADJACENT[0]: CARDINAL_ADJACENT[2],
    CARDINAL_ADJACENT[1]: CARDINAL_ADJACENT[3],
    CARDINAL_ADJACENT[2]: CARDINAL_ADJACENT[0],
    CARDINAL_ADJACENT[3]: CARDINAL_ADJACENT[1],
}


def debug_print(message):
    if DEBUG:
        print(message)


class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.seen = set()

    def next(self):
        return self.queue.pop()

    def enqueue(self, value):
        point, _, prev_direction, distance_limit = value
        seen_metric = point, prev_direction, distance_limit
        if (point, prev_direction, distance_limit) not in self.seen:
            debug_print(f"Enqueuing: {value}")
            self.queue.append(value)
            self.queue = sorted(self.queue, key=lambda x: x[1], reverse=True)
            self.seen.add(seen_metric)


def part1(data):
    # data = EXAMPLE_DATA

    grid = data.splitlines()

    queue = PriorityQueue()
    start = Point(0, 0)
    target = Point(len(grid) - 1, len(grid[0]) - 1)
    queue.enqueue((start, 0, None, 0))

    while True:
        point, loss_value, prev_direction, distance_limit = queue.next()
        debug_print(f"Processing: {point, loss_value, prev_direction, distance_limit}")

        if point == target:
            break

        for direction in CARDINAL_ADJACENT:
            next_point = point + direction
            debug_print(f"Testing {next_point}")

            if prev_direction:
                if direction == OPPOSITE[prev_direction]:
                    debug_print("Skipping: cannot U-turn")
                    continue
            
                if distance_limit == 3 and prev_direction == direction:
                    debug_print("Skipping: maximum distance reached")
                    continue

            next_distance = distance_limit + 1 if prev_direction and prev_direction == direction else 1
            

            if next_point.x < 0 or next_point.y < 0:
                debug_print("Skipping: off grid")
                continue

            try:
                next_loss = int(grid[next_point.x][next_point.y])
            except IndexError:
                debug_print("Skipping: off grid")
                continue

            queue.enqueue((next_point, loss_value + next_loss, direction, next_distance))
        # breakpoint()

    return loss_value


def part2(data):
    # data = EXAMPLE_DATA

    grid = data.splitlines()

    queue = PriorityQueue()
    start = Point(0, 0)
    target = Point(len(grid) - 1, len(grid[0]) - 1)
    queue.enqueue((start, 0, None, 0))

    while True:
        point, loss_value, prev_direction, distance_limit = queue.next()
        debug_print(f"Processing: {point, loss_value, prev_direction, distance_limit}")

        if point == target:
            break

        if distance_limit < 4 and prev_direction:
            next_point = point + prev_direction

            try:
                next_loss = int(grid[next_point.x][next_point.y])
            except IndexError:
                debug_print("Skipping: off grid")
                continue

            queue.enqueue((next_point, loss_value + next_loss, prev_direction, distance_limit + 1))
            continue


        for direction in CARDINAL_ADJACENT:
            next_distance = distance_limit + 1
            if prev_direction is not None:
                if direction == OPPOSITE[prev_direction]:
                    debug_print("Skipping: cannot U-turn")
                    continue
            
                if distance_limit == 10 and prev_direction == direction:
                    debug_print("Skipping: maximum distance reached")
                    continue

                if prev_direction != direction:
                    next_distance = 1

            next_point = point + direction
            debug_print(f"Testing {next_point}")

            if next_point.x < 0 or next_point.y < 0:
                debug_print("Skipping: off grid")
                continue

            try:
                next_loss = int(grid[next_point.x][next_point.y])
            except IndexError:
                debug_print("Skipping: off grid")
                continue

            queue.enqueue((next_point, loss_value + next_loss, direction, next_distance))
        # breakpoint()

    return loss_value
