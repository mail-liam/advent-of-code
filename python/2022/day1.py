EXAMPLE_DATA = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

def parse_input(data):
    groups = []
    current_group = []

    for line in data.splitlines():
        if not line.strip():
            groups.append(current_group)
            current_group = []
        else:
            current_group.append(int(line))
    groups.append(current_group)
    
    return groups

def part1(data):
    # data = EXAMPLE_DATA

    largest = 0
    for group in parse_input(data):
        total = sum(group)
        if total > largest:
            largest = total

    return largest


def part2(data):
    # data = EXAMPLE_DATA

    summed_groups = [sum(group) for group in parse_input(data)]
    sorted_groups = sorted(summed_groups)

    return sum(sorted_groups[-3:])