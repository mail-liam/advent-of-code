from aocd import get_data, submit

data = get_data(day=1, year=2023)
data = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

VALID_DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

total = []

for line in data.splitlines():
    tokens = []
    end = len(line)
    for i, char in enumerate(line):
        if char.isdigit():
            tokens.append(char)
            continue

        for n in range(1, 6):
            substr = line[i:i+n]
            if substr in VALID_DIGITS:
                tokens.append(VALID_DIGITS[substr])
                break

    print(tokens)

    total.append(int(f"{tokens[0]}{tokens[-1]}"))


print(total)
result = sum(total)


print(result)
# submit(result, part="b", day=1, year=2023)