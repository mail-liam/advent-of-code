import itertools
import typing as t

from common.parsing import parse_numbers

EXAMPLE_DATA = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def predict_next_sequence(sequence: t.Iterable[int]) -> int:
    next_sequence = [larger - smaller for smaller, larger in itertools.pairwise(sequence)]

    if all(elem == 0 for elem in next_sequence):
        return 0

    return next_sequence[-1] + predict_next_sequence(next_sequence)


def predict_next_sequence_start(sequence: list[int]) -> int:
    return sequence[-1] + predict_next_sequence(sequence)


def predict_prev_sequence(sequence: t.Iterable[int]) -> int:
    next_sequence = [larger - smaller for smaller, larger in itertools.pairwise(sequence)]

    if all(elem == 0 for elem in next_sequence):
        return 0

    return next_sequence[0] - predict_prev_sequence(next_sequence)


def predict_prev_sequence_start(sequence: list[int]) -> int:
    return sequence[0] - predict_prev_sequence(sequence)


def part1(data):
    # data = EXAMPLE_DATA

    return sum(predict_next_sequence_start(parse_numbers(sequence)) for sequence in data.splitlines())


def part2(data):
    # data = EXAMPLE_DATA

    return sum(predict_prev_sequence_start(parse_numbers(sequence)) for sequence in data.splitlines())
