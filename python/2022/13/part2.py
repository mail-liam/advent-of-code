from functools import cmp_to_key
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

TWO_PACKET = [[2]]
SIX_PACKET = [[6]]

clean_data = [eval(line) for line in data.splitlines() if line.strip()]
clean_data.append(TWO_PACKET)
clean_data.append(SIX_PACKET)

DEBUG = False


def compare_packets(left, right):
    for l_item, r_item in zip_longest(left, right):
        if DEBUG:
            print(f"Comparing {l_item} to {r_item}")

        if l_item is None and r_item is not None:
            print(f"Left list ran out of items before right list")
            return -1

        if r_item is None and l_item is not None:
            print(f"ERROR: Right list ran out of items before left list")
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
            print(f"Left item {l_item} is less than right item {r_item}")
            return -1
        if l_item == r_item:
            continue

        print(f"ERROR: Left item {l_item} is not less than right item {r_item}")
        return 1
    return 0

sorted_data = sorted(clean_data, key=cmp_to_key(compare_packets))
for item in sorted_data:
    print(item)
result = (sorted_data.index(TWO_PACKET) + 1) * (sorted_data.index(SIX_PACKET) + 1)
print(result)
# breakpoint()

submit(result, part="b", day=13, year=2022)