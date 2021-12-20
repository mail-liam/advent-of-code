from collections import Counter

def get_children_bucket(day):
    return (day + 2) % 7

with open('input.txt') as file:
    initial_state = [int(char) for char in file.readline().split(',')]

population = Counter(initial_state)
DAY_TOTAL = 80
prev_day_births = 0
prev_two_day_births = 0

for day in range(DAY_TOTAL):
    # print(population)
    index = day % 7
    # print(f'{index=}')
    new_births = population[index]

    # print(f'Adding {prev_two_day_births} births to day bucket {index}')
    population.update({index: prev_two_day_births})
    
    # print(f'Storing {new_births} new births for bucket {get_children_bucket(index)}')
    prev_two_day_births, prev_day_births = prev_day_births, new_births
    
    # print(f'DAY {day + 1}:\n{new_births=}\nFish count: {sum(population.values()) + prev_day_births + prev_two_day_births}')
print(f'Total after {DAY_TOTAL} days: {sum(population.values()) + prev_day_births + prev_two_day_births}')