# INPUT = ['forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2']

depth = 0
position = 0
aim = 0

with open('input.txt') as file:
  for command in file.readlines():
    direction, distance = command.split()
    distance = int(distance)

    if direction == 'forward':
      position += distance
      depth += aim * distance
    elif direction == 'down':
      aim += distance
    elif direction == 'up':
      aim -= distance

result = depth * position
print(f'{depth=}')
print(f'{position=}')
print(f'{result=}')