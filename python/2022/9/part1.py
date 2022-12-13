from aocd import get_data, submit

data = get_data(day=9, year=2022)

head_pos = [0, 0]
tail_pos = [0, 0]
visited_tail = set()
visited_tail.add(tuple(tail_pos))

def print_pos():
    print(head_pos)
    print(tail_pos)

def in_range(head, tail):
    return abs(head[0] - tail[0]) < 2 and abs(head[1] - tail[1]) < 2

def update_tail(head, tail):
    row_mag = abs(head[0] - tail[0])
    col_mag = abs(head[1] - tail[1])

    # print_pos()
    # breakpoint()

    if row_mag == 1:
        tail[0] = head[0]
    elif row_mag == 2:
        tail[0] += 1 if tail[0] < head[0] else -1

    if col_mag == 1:
        tail[1] = head[1]
    elif col_mag == 2:
        tail[1] += 1 if tail[1] < head[1] else -1

    # print("UPDATE")
    # print_pos()
    # breakpoint()

for move in data.split("\n"):
    dir, dist = move.split(" ")

    axis = 1 if dir == "U" or dir == "D" else 0
    dist = int(dist)
    magnitude = -1 if dir =="L" or dir == "D" else 1

    for _ in range(dist):
        head_pos[axis] = head_pos[axis] + magnitude
        # print_pos()
        
        if not in_range(head_pos, tail_pos):
            # breakpoint()
            update_tail(head_pos, tail_pos)

        visited_tail.add(tuple(tail_pos))
            
total = len(visited_tail)

# print(visited_tail)
print(total)
submit(total, part="a", day=9, year=2022)