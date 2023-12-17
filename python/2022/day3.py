PRIORITY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def part1(data):
    total = 0
    for sack in data.splitlines():
        half_size = len(sack) // 2
        first, second = set(sack[:half_size]), set(sack[half_size:])
        
        item = first.intersection(second).pop()
        total += PRIORITY.find(item) + 1  

    return total


def part2(data):
    data_gen = (line for line in data.splitlines())

    total = 0
    while True:
        try:
            first = set(next(data_gen))
        except StopIteration:
            break

        second = set(next(data_gen))
        third = set(next(data_gen))
            
        item = first.intersection(second, third).pop()
        total += PRIORITY.find(item) + 1

    return total
