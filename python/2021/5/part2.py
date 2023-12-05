from collections import Counter
from itertools import zip_longest

def parse_line(line):
    first, second = line.split(' -> ')
    start = tuple(int(n) for n in first.split(','))
    end = tuple(int(n) for n in second.split(','))
    return {'start': start, 'end': end}

def create_range(start, end):
    if start < end:
        return range(start, end + 1)
    # Going backward
    return range(start, end - 1, -1)



with open('input.txt') as file:
    lines = [parse_line(line) for line in file.readlines()]

counter = Counter()

for line in lines:
    start = line['start']
    end = line['end']
    points = []
    if start[0] != end[0] and start[1] != end[1]:
        x_range = create_range(start[0], end[0])
        y_range = create_range(start[1], end[1])
        points = zip(x_range, y_range)
    elif start[1] == end[1]:
        # y's match, so travelling horizontally
        x_range = create_range(start[0], end[0])
        points = zip_longest(x_range, [], fillvalue=start[1])
    else:
        # x's match
        y_range = create_range(start[1], end[1])
        points = zip_longest([], y_range, fillvalue=start[0])

    counter.update(points)
# print(counter)
result = filter(lambda n: n >= 2, counter.values())
print(len(list(result)))


