from collections import deque

BRACKET_PAIRS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

def has_illegal_char(line: str):
    seen = deque()
    enqued = deque(line)

    for _ in range(len(line)):
        current_char = enqued.popleft()
        if current_char in BRACKET_PAIRS.keys():
            seen.append(current_char)
        else:
            prev_open = seen.pop()
            if BRACKET_PAIRS[prev_open] != current_char:
                return current_char
    return False


with open('input.txt') as file:
    LINES = [line.strip() for line in file.readlines()]

valid_lines = [has_illegal_char(line) for line in LINES]

ILLEGAL_CHAR_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

result = sum(
    ILLEGAL_CHAR_SCORE[char]
    for char in filter(lambda x: x, valid_lines)
)
    
print(result)
