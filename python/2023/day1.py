def part1(data):
    # data = """1abc2
    # pqr3stu8vwx
    # a1b2c3d4e5f
    # treb7uchet"""

    total = []
    for line in data.splitlines():
        digits = [char for char in line if char.isdigit()]
        total.append(int(f"{digits[0]}{digits[-1]}"))

    # print(total)
    return sum(total)


def part2(data):
    # data = """two1nine
    # eightwothree
    # abcone2threexyz
    # xtwone3four
    # 4nineeightseven2
    # zoneight234
    # 7pqrstsixteen"""

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
        for i, char in enumerate(line):
            if char.isdigit():
                tokens.append(char)
                continue

            for n in range(1, 6):
                substr = line[i:i+n]
                if substr in VALID_DIGITS:
                    tokens.append(VALID_DIGITS[substr])
                    break

        # print(tokens)

        total.append(int(f"{tokens[0]}{tokens[-1]}"))

    # print(total)
    return sum(total)
