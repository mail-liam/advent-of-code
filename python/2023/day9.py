import itertools
import typing as t

from common.parsing import parse_numbers

EXAMPLE_DATA = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def predict_sequence_element(sequence: t.Iterable[int], start: bool = False) -> int:
    next_sequence = [larger - smaller for smaller, larger in itertools.pairwise(sequence)]

    if all(elem == 0 for elem in next_sequence):
        return 0

    if start:
        return next_sequence[0] - predict_sequence_element(next_sequence, start=start)
    return next_sequence[-1] + predict_sequence_element(next_sequence, start=start)


def part1(data):
    # data = EXAMPLE_DATA

    parsed_data = (parse_numbers(line) for line in data.splitlines())

    return sum(sequence[-1] + predict_sequence_element(sequence) for sequence in parsed_data)


def part2(data):
    # data = EXAMPLE_DATA

    parsed_data = (parse_numbers(line) for line in data.splitlines())

    return sum(sequence[0] - predict_sequence_element(sequence, start=True) for sequence in parsed_data)
