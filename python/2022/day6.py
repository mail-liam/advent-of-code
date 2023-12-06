from collections import deque


def get_first_unique_length_index(data, length):
    queue = deque(maxlen=length)
    total = 0
    for char in data:
        total += 1
        queue.append(char)

        if len(set(queue)) == length:
            break

    return total


def part1(data):
    return get_first_unique_length_index(data, 4)


def part2(data):
    return get_first_unique_length_index(data, 14)
