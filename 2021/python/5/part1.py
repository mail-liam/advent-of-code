from collections import Counter

def parse_line(line):
    first, second = line.split(' -> ')
    start = tuple(int(n) for n in first.split(','))
    end = tuple(int(n) for n in second.split(','))
    return {'start': start, 'end': end}


with open('input.txt') as file:
    lines = [parse_line(line) for line in file.readlines()]

counter = Counter()

for line in lines:
    start = line['start']
    end = line['end']
    if start[0] != end[0] and start[1] != end[1]:
        continue

    length = None
    replace_val = None
    if start[1] == end[1]:
        # y's match, so travelling horizontally
        replace_val = 0
        if start[0] > end[0]:
            length = range(end[0], start[0] + 1)
        else:
            length = range(start[0], end[0] + 1)
    else:
        # x's match
        replace_val = 1
        if start[1] > end[1]:
            length = range(end[1], start[1] + 1)
        else:
            length = range(start[1], end[1] + 1)

    for n in length:
        tmp = list(start)
        tmp[replace_val] = n
        counter.update([tuple(tmp)])
print(counter)
result = filter(lambda n: n >= 2, counter.values())
print(len(list(result)))


