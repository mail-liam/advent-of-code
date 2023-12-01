from aocd import get_data, submit

data = get_data(day=1, year=2023)
# data = """1abc2
# pqr3stu8vwx
# a1b2c3d4e5f
# treb7uchet"""

total = []

for line in data.splitlines():
    digits = [char for char in line if char.isdigit()]
    total.append(int(f"{digits[0]}{digits[-1]}"))

print(total)
result = sum(total)


print(result)
submit(result, part="a", day=2, year=2023)