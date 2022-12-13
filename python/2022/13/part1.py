from itertools import zip_longest
from aocd import get_data, submit

data = get_data(day=13, year=2022)
# data = """[1,1,3,1,1]
# [1,1,5,1,1]

# [[1],[2,3,4]]
# [[1],4]

# [9]
# [[8,7,6]]

# [[4,4],4,4]
# [[4,4],4,4,4]

# [7,7,7,7]
# [7,7,7]

# []
# [3]

# [[[]]]
# [[]]

# [1,[2,[3,[4,[5,6,7]]]],8,9]
# [1,[2,[3,[4,[5,6,0]]]],8,9]"""


def compare_packets(left, right):
    for l_item, r_item in zip_longest(left, right):
        if l_item is None and r_item is not None:
            print(f"Left list ran out of items before right list")
            return True

        if r_item is None and l_item is not None:
            print(f"ERROR: Right list ran out of items before left list")
            return False

        if isinstance(l_item, list) and not isinstance(r_item, list):
            r_item = [r_item]
        elif isinstance(r_item, list) and not isinstance(l_item, list):
            l_item = [l_item]

        if isinstance(l_item, list) and isinstance(r_item, list):
            result = compare_packets(l_item, r_item)
            if result is None:
                continue
            return result

        #  Both ints at this point
        if l_item < r_item:
            print(f"Left item {l_item} is less than right item {r_item}")
            return True
        if l_item == r_item:
            continue

        print(f"ERROR: Left item {l_item} is not less than right item {r_item}")
        return False
    return None

data_gen = (line for line in data.splitlines())
indices = []
index = 0

while True:
    index += 1
    try:
        left_packet = eval(next(data_gen))
        right_packet = eval(next(data_gen))

        if compare_packets(left_packet, right_packet):
            indices.append(index)

        next(data_gen)  # Remove blank line
    except StopIteration:
        break

submit(sum(indices), part="a", day=13, year=2022)