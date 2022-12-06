from collections import deque
from aocd import get_data, submit

data = get_data(day=6, year=2022)

recent = deque(maxlen=4)

total = 0
for char in data:
    total += 1
    recent.append(char)

    if len(recent) == 4:
        if len(set(recent)) == 4:
            break

print(total)
submit(total, part="a", day=6, year=2022)