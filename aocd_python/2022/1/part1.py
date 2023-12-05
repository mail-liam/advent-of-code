groups = []

with open('input.txt') as file:
    current_group = []
    for line in file:
        if not line.strip():
            groups.append(current_group)
            current_group = []
        else:
            current_group.append(int(line))

largest = 0
for group in groups:
    total = sum(group)
    if total > largest:
        largest = total
print(largest)