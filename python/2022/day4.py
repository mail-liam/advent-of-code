from common.parsing import parse_numbers

EXAMPLE_DATA = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def get_range_ends(num_range):
    first, second = num_range.split(",")
    l1, l2 = parse_numbers(first)
    r1, r2 = parse_numbers(second)

    return l1, l2, r1, r2


def check_full_overlap(num_range: str) -> bool:
    l1, l2, r1, r2 = get_range_ends(num_range)

    return (l1 <= r1 and l2 >= r2) or (r1 <= l1 and r2 >= l2)


def check_partial_overlap(num_range: str) -> bool:
    l1, l2, r1, r2 = get_range_ends(num_range)

    return l2 >= r1 and r2 >= l1


def part1(data):
    # data = EXAMPLE_DATA

    return len([pair for pair in data.splitlines() if check_full_overlap(pair)])


def part2(data):
    # data = EXAMPLE_DATA

    return len([pair for pair in data.splitlines() if check_partial_overlap(pair)])
