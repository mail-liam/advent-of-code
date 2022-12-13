from aocd import get_data, submit

data = get_data(day=8, year=2022)
# data = """30373
# 25512
# 65332
# 33549
# 35390"""
DEBUG = False

def get_vertical_slice(grid, col: int):
    return [row[col] for row in grid]

def is_visible(series, pos):
    pos_height = series[pos]
    left = series[:pos]
    right = series[pos + 1:]

    left_v = all(height < pos_height for height in left)
    right_v = all(height < pos_height for height in right)

    if DEBUG:
        print(f"Call: {series}, {pos}")
        print(f"left: {left}, visible: {left_v}")
        print(f"right: {right}, visible: {right_v}")
        print(f"result: {left_v or right_v}")
    return left_v or right_v

grid = []
for line in data.split("\n"):
    grid.append([int(i) for i in line])

results = []
for row in range(len(grid)):
    for col in range(len(grid[0])):
        vis_h = is_visible(grid[row], col)
        vis_c = is_visible(get_vertical_slice(grid, col), row)
        if DEBUG:
            print(f"Is not visible: {not vis_h and not vis_c}")
            breakpoint()
        results.append(vis_h or vis_c)

# print(results)
total = len(list(filter(None, results)))
print(total)
# submit(total, part="a", day=8, year=2022)