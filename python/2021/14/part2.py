from collections import Counter
from itertools import pairwise
from datetime import datetime

start = datetime.now()

RULES = {}
SEPERATOR = ' -> '
ITER_NUM = 23dir 15

current = ''
next_chain = ''


def get_next_sequence(sequence):
    pairs = pairwise(sequence)
    for index, pair in enumerate(pairs):
        first, second = pair
        if index == 0:
            yield first
        yield RULES[f'{first}{second}']
        yield second


with open('input.txt') as file:
    current = file.readline().strip()

    for line in file.readlines():
        if SEPERATOR in line:
            key, value = line.split(SEPERATOR)
            RULES[key] = value.strip()

for i in range(ITER_NUM):
    current = get_next_sequence(current)

totals = Counter(current).most_common()
print(totals[0][1] - totals[-1][1])

end = datetime.now()

print(f'Execution took {end - start} long to complete')