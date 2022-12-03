from aocd import get_data, submit

data = get_data(day=3, year=2022)

PRIORITY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

total = 0
for sack in data.split("\n"):
    half_size = len(sack) // 2
    first, second = sack[:half_size], sack[half_size:]
    
    for item in first:
        if item in second:
            total += PRIORITY.find(item) + 1
            break
            

print(total)
submit(total, part="a", day=3, year=2022)