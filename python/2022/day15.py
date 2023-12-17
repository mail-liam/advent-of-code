from collections import defaultdict
from itertools import pairwise

from common.parsing import parse_numbers

EXAMPLE_DATA = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

def get_manhatten_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def part1(data):
    # data = EXAMPLE_DATA

    KNOWN_EMPTY = set()
    OBJECTS = set()
    TARGET_ROW = 2_000_000  # 10 for sample

    for line in data.splitlines():
        sensor_col, sensor_row, beacon_col, beacon_row = parse_numbers(line)

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

            if row_max == TARGET_ROW:
                for point in [(col, row_max) for col in range(col_min, col_max+1)]:
                    KNOWN_EMPTY.add(point)

            if row_min == TARGET_ROW:
                for point in [(col, row_min) for col in range(col_min, col_max+1)]:
                    KNOWN_EMPTY.add(point)

            row_adj -= 1
            col_adj += 1

    return len(KNOWN_EMPTY) - len(OBJECTS)


def part2(data):
    # data = EXAMPLE_DATA

    DISTRESS_MIN_COL = 0
    DISTRESS_MAX_COL = 4_000_000  # 20 for sample
    DISTRESS_MIN_ROW = 0
    DISTRESS_MAX_ROW = 4_000_000  # 20 for sample

    KNOWN_EMPTY = defaultdict(set)

    for line in data.splitlines():
        sensor_col, sensor_row, beacon_col, beacon_row = parse_numbers(line)

        beacon = beacon_col, beacon_row
        sensor = sensor_col, sensor_row
        distance = get_manhatten_distance(beacon, sensor)

        row_adj, col_adj = distance, 0
        while row_adj != -1:
            row_max, row_min = min(DISTRESS_MAX_ROW, sensor_row + row_adj), max(DISTRESS_MIN_ROW, sensor_row - row_adj)
            col_max, col_min = min(DISTRESS_MAX_COL, sensor_col + col_adj), max(DISTRESS_MIN_COL, sensor_col - col_adj)

            KNOWN_EMPTY[row_min].add((col_min, col_max))
            KNOWN_EMPTY[row_max].add((col_min, col_max))

            row_adj -= 1
            col_adj += 1

    def find_empty_point():
        for row, ranges in sorted(KNOWN_EMPTY.items(), key=lambda k: k[0]):
            largest_seen = 0
            for i, (l_range, r_range) in enumerate(pairwise(sorted(ranges))):
                if i == 0 and l_range[0] != 0:
                    return 0, row

                if l_range[1] > largest_seen:
                    if l_range[0] > largest_seen:
                        return largest_seen + 1, row
                    # print(f"Updating largest_seen to {l_range[1]}")
                    largest_seen = l_range[1]
                    if largest_seen == DISTRESS_MAX_COL:
                        break

            if r_range[0] > l_range[1] + 1:
                return l_range[1] + 1, row

            if largest_seen != DISTRESS_MAX_COL and r_range[1] != DISTRESS_MAX_COL:
                return DISTRESS_MAX_COL, row
            
    target = find_empty_point()
    if target is None:
        raise ValueError("No target")
    
    return target[0] * 4_000_000 + target[1]
