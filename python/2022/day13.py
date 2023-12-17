from functools import cmp_to_key
from itertools import zip_longest

EXAMPLE_DATA = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def compare_packets(left, right):
    for l_item, r_item in zip_longest(left, right):
        if l_item is None and r_item is not None:
            # print(f"Left list ran out of items before right list")
            return -1

        if r_item is None and l_item is not None:
            # print(f"ERROR: Right list ran out of items before left list")
            return 1

        if isinstance(l_item, list) and not isinstance(r_item, list):
            r_item = [r_item]
        elif isinstance(r_item, list) and not isinstance(l_item, list):
            l_item = [l_item]

        if isinstance(l_item, list) and isinstance(r_item, list):
            result = compare_packets(l_item, r_item)
            if result == 0:
                continue
            return result

        #  Both ints at this point
        if l_item < r_item:
            # print(f"Left item {l_item} is less than right item {r_item}")
            return -1
        if l_item == r_item:
            continue

        # print(f"ERROR: Left item {l_item} is not less than right item {r_item}")
        return 1
    return 0


def part1(data):
    # data = EXAMPLE_DATA

    data_gen = (line for line in data.splitlines())
    indices = []
    index = 0

    while True:
        index += 1
        try:
            left_packet = eval(next(data_gen))
            right_packet = eval(next(data_gen))

            if compare_packets(left_packet, right_packet) == -1:
                indices.append(index)

            next(data_gen)  # Remove blank line
        except StopIteration:
            break

    return sum(indices)


def part2(data):
    # data = EXAMPLE_DATA

    TWO_PACKET = [[2]]
    SIX_PACKET = [[6]]

    clean_data = [eval(line) for line in data.splitlines() if line.strip()]
    clean_data.append(TWO_PACKET)
    clean_data.append(SIX_PACKET)

    sorted_data = sorted(clean_data, key=cmp_to_key(compare_packets))
    # for item in sorted_data:
    #     print(item)
    return (sorted_data.index(TWO_PACKET) + 1) * (sorted_data.index(SIX_PACKET) + 1)
