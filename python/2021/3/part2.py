with open('input.txt') as file:
    lines = [line.strip() for line in file.readlines()]
lines2 = [line for line in lines]

# O2
oxy_count = 0
while len(lines) > 1:
    threshold = len(lines) / 2
    bits = [line[oxy_count] for line in lines]
    zeros = bits.count('0')

    filter_val = '0' if zeros > threshold else '1'
    lines = list(filter(lambda num: num[oxy_count] == filter_val, lines))
    oxy_count += 1

oxy_val = int(lines[0], 2)


# CO2
cd_count = 0
while len(lines2) > 1:
    threshold = len(lines2) / 2
    bits = [line[cd_count] for line in lines2]
    zeros = bits.count('0')

    filter_val = '0' if zeros <= threshold else '1'
    lines2 = list(filter(lambda num: num[cd_count] == filter_val, lines2))
    cd_count += 1

cd_val = int(lines2[0], 2)

print(oxy_val)
print(cd_val)
print(oxy_val * cd_val)