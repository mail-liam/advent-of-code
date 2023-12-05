with open('input.txt') as file:
  input = [int(line) for line in file.readlines()]

prev = None
increases = 0

for measurement in input:
  if prev is not None and measurement > prev:
    increases += 1

  prev = measurement

print(increases)
