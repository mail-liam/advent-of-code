from collections import Counter, deque

RULES = {}
SEPERATOR = ' -> '
ITER_NUM = 20

current = ''
next_chain = ''

def get_new_sequence(pair):
    new_item = RULES[pair]
    return f'{pair[0]}{new_item}{pair[1]}'


with open('input.txt') as file:
    current = file.readline().strip()
    for line in file.readlines():
        if SEPERATOR in line:
            key, value = line.split(SEPERATOR)
            RULES[key] = value.strip()

for i in range(ITER_NUM):
    window = deque([], 2)
    for item in current:
        window.append(item)
        if len(window) != 2:
            continue

        next_sequence = get_new_sequence(''.join(window))
        if len(next_chain) == 0:
            next_chain += next_sequence
        else:
            next_chain += next_sequence[1:]
    current = next_chain
    next_chain = ''
    print(f'Completed iteration {i}')

totals = Counter(current).most_common()
print(totals[0][1] - totals[-1][1])
