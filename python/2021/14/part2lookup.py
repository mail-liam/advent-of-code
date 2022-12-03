from collections import Counter
from itertools import pairwise
from math import ceil


RULES = {}
SEPERATOR = ' -> '
ITER_NUM = 40

def update_pair_counts(prev_counts):
    new_counts = Counter()
    for pair, new in RULES.items():
        prev_total = prev_counts[pair]
        first, second = pair
        left_pair = f'{first}{new}'
        right_pair = f'{new}{second}'
        new_counts.update({left_pair: prev_total, right_pair: prev_total})
    return new_counts


with open('input.txt') as file:
    initial_sequence = file.readline().strip()

    for line in file.readlines():
        if SEPERATOR in line:
            key, value = line.split(SEPERATOR)
            RULES[key] = value.strip()

pairs = pairwise(initial_sequence)
pair_counts = Counter(f'{pair[0]}{pair[1]}' for pair in pairs)
for _ in range(ITER_NUM):
    pair_counts = update_pair_counts(pair_counts)
    

total = Counter()
for pair, value in pair_counts.items():
    for letter in pair:
        total.update({letter: value})
adjusted_total = Counter({letter: ceil(count / 2) for letter, count in total.items()})

ordered_total = adjusted_total.most_common()
print(ordered_total)
print(ordered_total[0][1] - ordered_total[-1][1])

