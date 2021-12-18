from collections import deque

with open('input.txt') as file:
  input = [int(line) for line in file.readlines()]

WINDOW_SIZE = 3

window = deque([], WINDOW_SIZE)
prev = None
increases = 0

for value in input:
  window.append(value)
  if len(window) != 3:
    continue
  measurement = sum(window)

  if prev is not None and measurement > prev:
    increases += 1

  prev = measurement

print(increases)