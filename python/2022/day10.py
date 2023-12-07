KEY_CYCLES = {20, 60, 100, 140, 180, 220}
TIME_MAP = {"noop": 1, "addx": 2}


def part1(data):
    cycle = 0
    register = 1
    values = []

    def check_key_cycle():
        if cycle in KEY_CYCLES:
            print(f"Key cycle {cycle}, register: {register}")
            values.append(cycle * register)

    for line in data.splitlines():
        match line.split(" "):
            case [command]:
                cycle += TIME_MAP[command]
                check_key_cycle()

            case [command, value]:
                for _ in range(TIME_MAP[command]):
                    cycle += 1
                    check_key_cycle()

                register += int(value)

    print(values)
    print(register)

    return sum(values)


def part2(data):
    cycle = 0
    register = 1
    values = []
    sprite_pos = (0, 1, 2)
    screen = []

    def draw_pixel(n):
        nonlocal values
        n = n % 40
        values.append("#" if n in sprite_pos else ".")
        if len(values) == 40:
            screen.append(values)
            values = []

    def update_sprite_pos(n):
        nonlocal sprite_pos
        sprite_pos = (n - 1, n, n + 1)


    for line in data.splitlines():
        match line.split(" "):
            case [command]:
                draw_pixel(cycle)
                cycle += TIME_MAP[command]

            case [command, value]:
                for _ in range(TIME_MAP[command]):
                    draw_pixel(cycle)
                    cycle += 1

                register += int(value)
                update_sprite_pos(register)

    for row in screen:
        print(row)