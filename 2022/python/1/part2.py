groups = []

with open('input.txt') as file:
    current_group = []
    for line in file:
        if not line.strip():
            groups.append(current_group)
            current_group = []
        else:
            current_group.append(int(line))

summed_groups = [sum(group) for group in groups]
sorted_groups = sorted(summed_groups)
print(sum(sorted_groups[-3:]))