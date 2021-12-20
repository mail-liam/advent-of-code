def get_expensive_cost(start, end):
    upper = max(start, end) + 1
    lower = min(start, end)
    return sum(range(abs(upper - lower)))


def get_cost_to_align_at(num, positions):
    return sum(get_expensive_cost(pos, num) for pos in positions)


with open('input.txt') as file:
    initial_positions = [int(value) for value in file.readline().split(',')]

max_pos = max(initial_positions)
min_pos = min(initial_positions)

costs = [get_cost_to_align_at(align_pos, initial_positions) for align_pos in range(min_pos, max_pos + 1)]
print(min(costs))