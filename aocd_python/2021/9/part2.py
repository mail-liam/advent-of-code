from collections import Counter, deque

class BasinScanner:
    def __init__(self, grid):
        self.basins = None
        self.GRID = grid
        self.seen = set()

    @property
    def grid_height(self) -> int:
        return len(self.GRID)

    @property
    def grid_width(self) -> int:
        return len(self.GRID[0])

    def find_basins(self):
        if self.basins is not None:
            return self.basins

        self.basins = []

        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if (row, col) not in self.seen and self.GRID[row][col] != 9:
                    self._create_new_basin(row, col)
        return self.basins

    def _create_new_basin(self, row, col):
        queue = deque()
        queue.append((row, col))
        self.seen.add((row, col))
        size = 0

        while len(queue) != 0:
            new_point = queue.pop()
            size += 1
            new_neighbours = self._get_unseen_neighbours(*new_point)
            queue.extend(new_neighbours)
            self.seen.update(set(new_neighbours))
        self.basins.append(size)    

    def _get_unseen_neighbours(self, row, col):
        neighbours = []

        if row > 0:
            neighbours.append((row - 1, col))

        if col > 0:
            neighbours.append((row, col - 1))

        if row < self.grid_height - 1:
            neighbours.append((row + 1, col))

        if col < self.grid_width - 1:
            neighbours.append((row, col + 1))

        return [
            neighbour
            for neighbour in neighbours
            if neighbour not in self.seen
            and self.GRID[neighbour[0]][neighbour[1]] != 9
        ]


with open('input.txt') as file:
    GRID = [
        [int(char) for char in line.strip()]
        for line in file.readlines()
    ]

scanner = BasinScanner(GRID)
basins = scanner.find_basins()
top_three = sorted(basins, reverse=True)[:3]

result = 1
for size in top_three:
    result *= size
print(result)
