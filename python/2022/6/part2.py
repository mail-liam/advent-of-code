from collections import deque
from aocd import get_data, submit

data = get_data(day=6, year=2022)

recent = deque(maxlen=14)

total = 0
for char in data:
    total += 1
    recent.append(char)

    if len(recent) == 14:
        if len(set(recent)) == 14:
            break

print(total)
submit(total, part="b", day=6, year=2022)