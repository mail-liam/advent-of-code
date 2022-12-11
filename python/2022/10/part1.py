from aocd import get_data, submit

data = get_data(day=10, year=2022)

KEY_CYCLES = set([20, 60, 100, 140, 180, 220])
TIME_MAP = {
    "noop": 1,
    "addx": 2,
}

cycle = 0
register = 1
values = []

def check_key_cycle():
    if cycle in KEY_CYCLES:
        print(f"Key cycle {cycle}, register: {register}")
        values.append(cycle * register)


for line in data.split("\n"):
    command = line.split(" ")
    time_taken = TIME_MAP[command[0]]

    if command[0] == "noop":
        cycle += time_taken
        check_key_cycle()

    if command[0] == "addx":
        for i in range(time_taken):
            cycle += 1
            check_key_cycle()

        register += int(command[1]) 

print(values)
print(register)
print(sum(values))
submit(sum(values), part="a", day=10, year=2022)