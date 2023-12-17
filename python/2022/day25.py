import typing as t


def snafu_digit_to_decimal(digit: str) -> int:
    try:
        return int(digit)
    except ValueError:
        if digit == "=":
            return -2
        if digit == "-":
            return -1
        raise ValueError("Not a valid SNAFU digit")

def decimal_digit_to_snafu(digit: t.Literal[-2, -1, 0, 1, 2]) -> str:
    if digit >= 0:
        return str(digit)
    if digit == -1:
        return "-"
    if digit == -2:
        return "="
    raise ValueError("Invalid digit for SNAFU encoding")


def snafu_decode(number: str) -> int:
    total = []
    for i, digit in enumerate(reversed(number)):
        total.append(5 ** i * snafu_digit_to_decimal(digit))
    return sum(total)


def snafu_encode(number: int) -> str:
    i = 0
    next_number = number
    result = []

    while True:
        current_digit_value = 5 ** i
        next_digit_value = 5 ** (i + 1)

        digit_value = (next_number % next_digit_value) // current_digit_value
        adjusted_digit_value = digit_value -5 if digit_value > 2 else digit_value

        result.append(decimal_digit_to_snafu(adjusted_digit_value))

        next_number -= current_digit_value * adjusted_digit_value

        if next_number == 0:
            break

        i += 1

    return "".join(reversed(result))


def part1(data):
#     data = """1=-0-2
# 12111
# 2=0=
# 21
# 2=01
# 111
# 20012
# 112
# 1=-1=
# 1-12
# 12
# 1=
# 122"""

    decimal_number = sum(snafu_decode(num) for num in data.splitlines())
    return snafu_encode(decimal_number)
