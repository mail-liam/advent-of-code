from collections import Counter

counter = Counter()

with open('input.txt') as file:
    for line in file.readlines():
        outputs = line.split(' | ')[1].split()
        lengths = [len(out) for out in outputs]
        counter.update(lengths)

# Ones, Fours, Sevens, Eights
print(sum([counter[2], counter[4], counter[3], counter[7]]))       
