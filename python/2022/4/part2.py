from aocd import get_data, submit

data = get_data(day=4, year=2022)

def check_partial_overlap(num_range: str) -> bool:
    first, second = num_range.split(",")
    l1, l2 = [int(n) for n in first.split("-")]
    r1, r2 = [int(n) for n in second.split("-")]

    return l2 >= r1 and r2 >= l1

total = 0
for pair in data.split("\n"):
    if check_partial_overlap(pair):
        total += 1

print(total)
submit(total, part="b", day=4, year=2022)