from collections import deque

BRACKET_PAIRS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

PAIR_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def complete_valid_line(line: str):
    seen = deque()
    enqued = deque(line)

    for _ in range(len(line)):
        current_char = enqued.popleft()
        if current_char in BRACKET_PAIRS.keys():
            seen.append(current_char)
        else:
            prev_open = seen.pop()
            if BRACKET_PAIRS[prev_open] != current_char:
                return False
    
    remainder = ''
    while len(seen) != 0:
        remainder += BRACKET_PAIRS[seen.pop()]
    return remainder

def score_remainder(remainder: str) -> int:
    score = 0
    for char in remainder:
        score *= 5
        score += PAIR_SCORE[char]
    return score


with open('input.txt') as file:
    LINES = [line.strip() for line in file.readlines()]

missing_pairs = [complete_valid_line(line) for line in LINES]
scores = sorted(
    score_remainder(remainder)
    for remainder in filter(lambda x: x, missing_pairs)
)

# Could use median here but odd number guranteed
print(scores[len(scores) // 2])