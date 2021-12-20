import re
from itertools import count


def x_values(initial_x):
    acc = 0
    for _ in count():
        acc += initial_x
        yield acc
        initial_x = max(0, initial_x - 1)


def y_values(initial_y):
    acc = 0
    for adj in count(start=initial_y, step=-1):
        acc += adj
        yield acc


def check_path(x_init, y_init):
    x_gen = x_values(x_init)
    y_gen = y_values(y_init)

    while True:
        x = next(x_gen)
        y = next(y_gen)

        if x in range(X_MIN, X_MAX + 1) and y in range(Y_MIN, Y_MAX + 1):
            # print(f'{x_init=}')
            # print(f'{y_init=}')
            return True

        if x > X_MAX or y < Y_MIN:
            return False


with open('input.txt') as file:
    target_area = file.readline()

regex = re.compile('x=(\d+)\.\.(\d+), y=(-\d+)\.\.(-\d+)')
X_MIN, X_MAX, Y_MIN, Y_MAX = [int(num) for num in re.search(regex, target_area).groups()]

successes = 0
for y_init in range(Y_MIN, abs(Y_MIN)):
    for x_init in range(0, X_MAX + 1):
        is_success = check_path(x_init, y_init)
        if is_success:
            successes += 1
print(successes)