from aocd import get_data, submit

data = get_data(day=18, year=2022)
# data = """2,2,2
# 1,2,2
# 3,2,2
# 2,1,2
# 2,3,2
# 2,2,1
# 2,2,3
# 2,2,4
# 2,2,6
# 1,2,5
# 3,2,5
# 2,1,5
# 2,3,5"""

LAVA = set()

def get_visible_sides(cube):
    score = 6
    if (cube[0], cube[1], cube[2] + 1) in LAVA:
        score -= 1

    if (cube[0], cube[1], cube[2] - 1) in LAVA:
        score -= 1

    if (cube[0], cube[1] + 1, cube[2]) in LAVA:
        score -= 1

    if (cube[0], cube[1] - 1, cube[2]) in LAVA:
        score -= 1

    if (cube[0] + 1, cube[1], cube[2]) in LAVA:
        score -= 1

    if (cube[0] - 1, cube[1], cube[2]) in LAVA:
        score -= 1

    return score

for cube in data.splitlines():
    x, y, z = [int(dim) for dim in cube.split(",")]
    LAVA.add((x, y, z))

total = 0
for cube in LAVA:
    total += get_visible_sides(cube)

print(total)
submit(total, part="a", day=18, year=2022)