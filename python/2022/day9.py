# EXAMPLE_DATA = """R 4
# U 4
# L 3
# D 1
# R 4
# D 1
# L 5
# R 2"""
EXAMPLE_DATA = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


def in_range(head, tail):
    return abs(head[0] - tail[0]) < 2 and abs(head[1] - tail[1]) < 2

def update_tail(head, tail):
    row_mag = abs(head[0] - tail[0])
    col_mag = abs(head[1] - tail[1])

    if row_mag == 1:
        tail[0] = head[0]
    elif row_mag == 2:
        tail[0] += 1 if tail[0] < head[0] else -1

    if col_mag == 1:
        tail[1] = head[1]
    elif col_mag == 2:
        tail[1] += 1 if tail[1] < head[1] else -1


def part1(data):
    # data = EXAMPLE_DATA

    head_pos = [0, 0]
    tail_pos = [0, 0]
    visited_tail = set()
    visited_tail.add(tuple(tail_pos))

    for move in data.splitlines():
        dir, dist = move.split(" ")
        axis = 1 if dir == "U" or dir == "D" else 0
        magnitude = -1 if dir =="L" or dir == "D" else 1

        for _ in range(int(dist)):
            head_pos[axis] = head_pos[axis] + magnitude
            
            if not in_range(head_pos, tail_pos):
                update_tail(head_pos, tail_pos)

            visited_tail.add(tuple(tail_pos))
                
    return len(visited_tail)


def part2(data):
    # data = EXAMPLE_DATA

    N_KNOTS = 10
    POS_MAP = {}

    for i in range(N_KNOTS):
        POS_MAP[i] = [0, 0]

    visited_tail = set()
    visited_tail.add(tuple(POS_MAP[N_KNOTS - 1]))

    for move in data.split("\n"):
        dir, dist = move.split(" ")
        axis = 1 if dir == "U" or dir == "D" else 0
        magnitude = -1 if dir =="L" or dir == "D" else 1

        for _ in range(int(dist)):
            head_pos = POS_MAP[0]
            head_pos[axis] = head_pos[axis] + magnitude
            
            for i in range(N_KNOTS - 1):
                head_pos, tail_pos = POS_MAP[i], POS_MAP[i+1]
                if not in_range(head_pos, tail_pos):
                    update_tail(head_pos, tail_pos)

            visited_tail.add(tuple(POS_MAP[N_KNOTS - 1]))
                
    return len(visited_tail)
