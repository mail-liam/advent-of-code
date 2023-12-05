from math import ceil

with open('input.txt') as file:
    lines = [line.strip() for line in file.readlines()]

LENGTH = len(lines[0])
MAX_BIN = pow(2, LENGTH) - 1
N_LINES = len(lines)
MIN_THRES = ceil(N_LINES / 2)

gamma = ''

for i in range(LENGTH):
    bits = [line[i] for line in lines]
    zeros = bits.count('0')

    new_value = '1' if zeros < MIN_THRES else '0'
    gamma += new_value

gamma = int(gamma, 2)
epsilon = MAX_BIN - gamma

print(gamma * epsilon)