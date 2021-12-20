# Start knowns = 1 (2), 4 (4), 7 (3), 8 (7)
# top = 7 (3) - 1 (2)
# tleft = 4 (4) - 1 (2) - mid (1)
# tright = 1 (2) - 6 (6) if len(1) after
# mid = 3 (5) - 1 (2) - top (1) - bottom (1) if len(1) after
# bleft = 8 (7) - 4 (4) - top (1) - bottom (1)
# bright = 1 (2) - tright (1)
# bot = 3 (5) - 4 (3) - top (1) if len(1) after

def get_unique_len_digit(num, samples):
    for sample in samples.split():
        if len(sample) == num:
            return set(sample)

def get_matching_digit(digit_set, numbers):
    for num, num_set in numbers.items():
        if digit_set == num_set:
            return str(num)

def decode_display(display):
    samples, outputs = display.split(' | ')
    number = {}
    number[1] = get_unique_len_digit(2, samples)
    number[4] = get_unique_len_digit(4, samples)
    number[7] = get_unique_len_digit(3, samples)
    number[8] = get_unique_len_digit(7, samples)

    len_sixes = [set(sample) for sample in samples.split() if len(sample) == 6]
    len_fives = [set(sample) for sample in samples.split() if len(sample) == 5]
    top = number[7] - number[1]

    for cand in len_sixes:
        test = cand - number[1]
        if len(test) == 5:
            number[6] = cand
            continue
        test2 = cand - number[4] - top
        if len(test2) == 1:
            number[9] = cand
    len_sixes.remove(number[6])
    len_sixes.remove(number[9])
    number[0] = len_sixes[0]

    for cand in len_fives:
        test = number[9] - cand
        if len(test) == 2:
            number[2] = cand
            continue
        test2 = cand - number[1]
        if len(test2) == 3:
            number[3] = cand
    len_fives.remove(number[2])
    len_fives.remove(number[3])
    number[5] = len_fives[0]

    result = [get_matching_digit(set(output), number) for output in outputs.split()]
    return int(''.join(result))


with open('input.txt') as file:
    results = [decode_display(display) for display in file.readlines()]
    print(sum(results))