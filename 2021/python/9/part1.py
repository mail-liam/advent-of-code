def check_low_point(row, col):
    neighbours = []

    if row > 0:
        neighbours.append(GRID[row - 1][col])

    if col > 0:
        neighbours.append(GRID[row][col - 1])

    if row < GRID_HEIGHT - 1:
        neighbours.append(GRID[row + 1][col])

    if col < GRID_WIDTH - 1:
        neighbours.append(GRID[row][col + 1])

    return all([num > GRID[row][col] for num in neighbours])


with open('input.txt') as file:
    GRID = [
        [int(char) for char in line.strip()]
        for line in file.readlines()
    ]

GRID_WIDTH = len(GRID[0])
GRID_HEIGHT = len(GRID)

low_sum = 0
for row in range(GRID_HEIGHT):
    for col in range(GRID_WIDTH):
        is_low = check_low_point(row, col)
        if is_low:
            low_sum += GRID[row][col] + 1
print(low_sum)