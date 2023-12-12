import math
import re
import itertools
import typing as t

from common.parsing import parse_numbers

EXAMPLE_DATA = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def find_springs(data):
    return re.findall("(#+)", data)


def get_possible_arrangements(data):
    springs, nums = data.split(" ")
    numbers = parse_numbers(nums)
    count_nums = len(numbers)

    damaged = springs.count("?")

    arrangement_count = 0
    for option in itertools.product(".#", repeat=damaged):
        springs_copy = springs

        for replacement in option:
            springs_copy = springs_copy.replace("?", replacement, 1)

        spring_groups = find_springs(springs_copy)
        if len(spring_groups) != count_nums:
            continue

        for spring_group, count in zip(spring_groups, numbers):
            if len(spring_group) != count:
                break
        else:
            arrangement_count += 1
            # print(f"{springs_copy} is valid")

    return arrangement_count


def part1(data):
    # data = EXAMPLE_DATA

    return sum(get_possible_arrangements(line) for line in data.splitlines())


def unfold_data(data, joiner):
    return joiner.join([data, data, data, data, data])


def apply_logic(data):
    return data


def get_possible_states(data: str) -> int:
    cleaned_data = apply_logic(data)

    print(cleaned_data)


    return fit_blocks_to_space((2, 1), 7) * fit_blocks_to_space((2, 1), 8) ** 4
    # return fit_blocks_to_space((1,), 4) * math.pow(fit_blocks_to_space((1,), 5), 4)


def part2(data):
    data = EXAMPLE_DATA.splitlines()[4]

    assert fit_blocks_to_space((5,), 5) == 1
    assert fit_blocks_to_space((4,), 5) == 2
    assert fit_blocks_to_space((3,), 5) == 3
    assert fit_blocks_to_space((1, 1), 3) == 1
    assert fit_blocks_to_space((1, 1), 4) == 3
    assert fit_blocks_to_space((1, 1), 5) == 6
    assert fit_blocks_to_space((2, 1), 5) == 3
    assert fit_blocks_to_space((3, 3), 9) == 6
    assert fit_blocks_to_space((1, 1, 1), 6) == 4
    assert fit_blocks_to_space((1, 1, 1), 7) == 10
    assert fit_blocks_to_space((2, 1, 1), 7) == 4


    total = 0
    # for line in data.splitlines():
    springs, nums = data.split(" ")
    unfolded = f"{unfold_data(springs, "?")} {unfold_data(nums, ",")}"

    total += get_possible_states(unfolded)

    # total += get_possible_arrangements(unfolded)

    return total


def fit_blocks_to_space(blocks: t.Iterable, space: int):
    return math.comb(space - sum(blocks) + 1, len(blocks))


    