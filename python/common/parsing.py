import re

def parse_numbers(data):
    return tuple(int(num) for num in re.findall(r"-?\d+", data))