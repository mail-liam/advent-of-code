EXAMPLE_DATA = """30373
25512
65332
33549
35390"""
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


def part1(data):
    # data = EXAMPLE_DATA

    grid = [[int(i) for i in line] for line in data.splitlines()]

    results = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            vis_h = is_visible(grid[row], col)
            vis_c = is_visible(get_vertical_slice(grid, col), row)
            if DEBUG:
                print(f"Is not visible: {not vis_h and not vis_c}")
            results.append(vis_h or vis_c)

    return len(list(filter(None, results)))


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

    return next_tallest(left, height) * next_tallest(right, height)


def part2(data):
    # data = EXAMPLE_DATA

    grid = [[int(i) for i in line] for line in data.splitlines()]

    results = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            h_score = view_distance(grid[row], col)
            v_score = view_distance(get_vertical_slice(grid, col), row)

            results.append(h_score * v_score)

    return max(results)
