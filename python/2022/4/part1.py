from aocd import get_data, submit

data = get_data(day=4, year=2022)

def check_full_overlap(num_range: str) -> bool:
    first, second = num_range.split(",")
    l1, l2 = [int(n) for n in first.split("-")]
    r1, r2 = [int(n) for n in second.split("-")]

    print(l1, l2, r1, r2)

    return (l1 <= r1 and l2 >= r2) or (r1 <= l1 and r2 >= l2)


total = 0
for pair in data.split("\n"):
    if check_full_overlap(pair):
        total += 1

print(total)
submit(total, part="a", day=4, year=2022)