import re

with open('input.txt') as file:
    target_area = file.readline()

regex = re.compile('y=-?(\d+)\.\.')
y_max_velocity = int(re.search(regex, target_area).groups()[0])
# Need to be travelling at most this velocity
# in order to not overshoot target area from starting point

max_height = sum(range(y_max_velocity))
print(max_height)