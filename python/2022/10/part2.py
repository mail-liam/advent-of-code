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
sprite_pos = (0, 1, 2)
screen = []


def draw_pixel(n):
    global values
    n = n % 40
    values.append("#" if n in sprite_pos else ".")
    if len(values) == 40:
        screen.append(values)
        values = []

def update_sprite_pos(n):
    global sprite_pos
    sprite_pos = (n - 1, n, n + 1)


for line in data.split("\n"):
    command = line.split(" ")
    time_taken = TIME_MAP[command[0]]

    if command[0] == "noop":
        draw_pixel(cycle)
        cycle += time_taken

    if command[0] == "addx":
        for i in range(time_taken):
            draw_pixel(cycle)
            cycle += 1

        register += int(command[1])
        update_sprite_pos(register)

for row in screen:
    print(row)
# submit(total, part="b", day=10, year=2022)