from collections import Counter, deque
from itertools import pairwise
from datetime import datetime

start = datetime.now()


RULES = {}
SEPERATOR = ' -> '
ITER_NUM = 22

counter = Counter()

def update_pair_counts(pair):
    first, second, iter_num = pair
    new_item = RULES[f'{first}{second}']
    counter.update(new_item)

    iter_num -= 1
    if iter_num == 0:
        return None
    return (first, new_item, iter_num), (new_item, second, iter_num)


with open('input.txt') as file:
    initial_sequence = file.readline().strip()

    for line in file.readlines():
        if SEPERATOR in line:
            key, value = line.split(SEPERATOR)
            RULES[key] = value.strip()

counter.update(initial_sequence)
pairs_with_iter_count = [(*pair, ITER_NUM) for pair in pairwise(initial_sequence)]

queue = deque(pairs_with_iter_count)
while True:
    try:
        next_pair = queue.pop()
    except IndexError:
        # queue is empty
        break
    else:
        next_items = update_pair_counts(next_pair)
        if next_items is not None:
            queue.extend(next_items)
    print(len(queue))
    

totals = counter.most_common()
print(totals[0][1] - totals[-1][1])

finish = datetime.now()
print(f'Execution took {finish - start}')