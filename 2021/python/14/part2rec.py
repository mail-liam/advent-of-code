from collections import Counter
from itertools import pairwise
from datetime import datetime

start = datetime.now()


RULES = {}
SEPERATOR = ' -> '
ITER_NUM = 22

counter = Counter()

def update_pair_counts(pair, iter_num):
    first, second = pair
    new_item = RULES[f'{first}{second}']
    counter.update(new_item)

    next_num = iter_num - 1
    if next_num == 0:
        return
    update_pair_counts((first, new_item), next_num)
    update_pair_counts((new_item, second), next_num)


with open('input.txt') as file:
    initial_sequence = file.readline().strip()

    for line in file.readlines():
        if SEPERATOR in line:
            key, value = line.split(SEPERATOR)
            RULES[key] = value.strip()

counter.update(initial_sequence)

pairs = pairwise(initial_sequence)
for pair in pairs:
    update_pair_counts(pair, ITER_NUM)

totals = counter.most_common()
print(totals[0][1] - totals[-1][1])

finish = datetime.now()
print(f'Execution took {finish - start}')