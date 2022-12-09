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

def next_tallest(series, height):
    total = 0
    for h in series:
        total += 1
        if h >= height:
            return total
        
    return total  # Empty series

def view_distance(series, pos):
    height = series[pos]
    left = list(reversed(series[:pos]))
    right = series[pos + 1:]

    left_score = next_tallest(left, height)
    right_score = next_tallest(right, height)

    if DEBUG:
        print(f"Call: {series}, {pos}")
        print(f"left: {left}, visible: {left_v}")
        print(f"right: {right}, visible: {right_v}")
        print(f"result: {left_v or right_v}")
    return left_score * right_score

grid = []
for line in data.split("\n"):
    grid.append([int(i) for i in line])

results = []
for row in range(len(grid)):
    for col in range(len(grid[0])):
        h_score = view_distance(grid[row], col)
        v_score = view_distance(get_vertical_slice(grid, col), row)
        if DEBUG:
            print(f"Is not visible: {not vis_h and not vis_c}")
            breakpoint()
        results.append(h_score * v_score)

print(results)
total = max(results)
print(total)
submit(total, part="b", day=8, year=2022)