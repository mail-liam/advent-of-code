import re
from aocd import get_data, submit

data = get_data(day=15, year=2022)
# data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
# Sensor at x=9, y=16: closest beacon is at x=10, y=16
# Sensor at x=13, y=2: closest beacon is at x=15, y=3
# Sensor at x=12, y=14: closest beacon is at x=10, y=16
# Sensor at x=10, y=20: closest beacon is at x=10, y=16
# Sensor at x=14, y=17: closest beacon is at x=10, y=16
# Sensor at x=8, y=7: closest beacon is at x=2, y=10
# Sensor at x=2, y=0: closest beacon is at x=2, y=10
# Sensor at x=0, y=11: closest beacon is at x=2, y=10
# Sensor at x=20, y=14: closest beacon is at x=25, y=17
# Sensor at x=17, y=20: closest beacon is at x=21, y=22
# Sensor at x=16, y=7: closest beacon is at x=15, y=3
# Sensor at x=14, y=3: closest beacon is at x=15, y=3
# Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

INPUT_RE = re.compile("Sensor at x=(\-?\d*), y=(\-?\d*): closest beacon is at x=(\-?\d*), y=(\-?\d*)")
KNOWN_EMPTY = set()
OBJECTS = set()
TARGET_ROW = 2_000_000

def get_manhatten_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

for line in data.splitlines():
    sensor_col, sensor_row, beacon_col, beacon_row = (
        int(group) for group in INPUT_RE.match(line).groups()
    )

    beacon = beacon_col, beacon_row
    sensor = sensor_col, sensor_row
    # print(f"Beacon {beacon}. Sensor {sensor}")
    if beacon_row == TARGET_ROW:
        OBJECTS.add(beacon)
    if sensor_row == TARGET_ROW:
        OBJECTS.add(sensor)

    distance = get_manhatten_distance(beacon, sensor)

    row_adj, col_adj = distance, 0
    while row_adj != -1:
        row_max, row_min = sensor_row + row_adj, sensor_row - row_adj
        col_max, col_min = sensor_col + col_adj, sensor_col - col_adj
        # print(f"Adjusted rows: {row_max}, {row_min}")
        # print(f"Adjusted cols: {col_max}, {col_min}")
        # print([(col, row_max) for col in range(col_min, col_max+1)])
        if row_max == TARGET_ROW:
            for point in [(col, row_max) for col in range(col_min, col_max+1)]:
                KNOWN_EMPTY.add(point)
        # print([(col, row_min) for col in range(col_min, col_max+1)])
        if row_min == TARGET_ROW:
            for point in [(col, row_min) for col in range(col_min, col_max+1)]:
                KNOWN_EMPTY.add(point)

        row_adj -= 1
        col_adj += 1

total = len(KNOWN_EMPTY) - len(OBJECTS)

print(total)
submit(total, part="a", day=15, year=2022)