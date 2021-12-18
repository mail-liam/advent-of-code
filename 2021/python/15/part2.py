class PriorityQueue:
    def __init__(self):
        self.seen_points = set()
        self.queue = []

    def next(self):
        return self.queue.pop()

    def enqueue(self, value):
        point, _ = value
        if point not in self.seen_points:
            self.seen_points.add(point)
            self.queue.append(value)
            self.queue = sorted(self.queue, key=lambda x: x[1], reverse=True)
            


with open('input.txt') as file:
    GRID = [
        [int(value) for value in row.strip()]
        for row in file.readlines()
    ]

GRID_WIDTH = len(GRID[0])
GRID_HEIGHT = len(GRID)

def get_points_near(x, y):
    neighbours = []
    if x != 0:
        neighbours.append((x - 1, y))
    if x + 1 < GRID_WIDTH * 5:
        neighbours.append((x + 1, y))
    if y != 0:
        neighbours.append((x, y - 1))
    if y + 1 < GRID_HEIGHT * 5:
        neighbours.append((x, y + 1))
    return neighbours

def get_distance_increase(x, y):
    x_bonus = x // GRID_WIDTH
    x_point = x % GRID_WIDTH
    y_bonus = y // GRID_HEIGHT
    y_point = y % GRID_HEIGHT

    base = GRID[x_point][y_point]
    increase = (base + x_bonus + y_bonus) % 9
    if increase == 0:
        increase += 9
    return increase


destination = (GRID_WIDTH * 5 - 1, GRID_HEIGHT * 5 - 1)

queue = PriorityQueue()
point = (0, 0)
distance = 0
queue.enqueue((point, distance))


while True:
    point, distance = queue.next()
    if point == destination:
        break

    new_points = get_points_near(point[0], point[1])

    for x, y in new_points:
        distance_increase = get_distance_increase(x, y)
        queue.enqueue(((x, y), distance + distance_increase))

print(distance)