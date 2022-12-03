from aocd import get_data, submit

data = get_data(day=3, year=2022)

PRIORITY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

data_gen = (line for line in data.split("\n"))

total = 0
while True:
    try:
        first = next(data_gen)
    except StopIteration:
        break

    second = next(data_gen)
    third = next(data_gen)
        
    for item in first:
        if item in second and item in third:
            total += PRIORITY.find(item) + 1
            break
            
print(total)
submit(total, part="b", day=3, year=2022)