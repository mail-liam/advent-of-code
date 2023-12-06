import itertools
import re


def get_transform_data_p1(data):
    transforms = []
    current_transform = []
    for line in data:
        if line == "":
            if current_transform:
                transforms.append(current_transform)
                current_transform = []
            continue

        subrange = [int(hit) for hit in re.findall("\d+", line)]
        if subrange:
            start = subrange[1]
            end = start + subrange[2]
            difference = start - subrange[0]
            current_transform.append((start, end, difference))

    transforms.append(current_transform)
    return transforms


def get_transform_data_p2(data):
    transforms = []
    current_transform = []
    for line in data:
        if line == "":
            if current_transform:
                transforms.append(current_transform)
                current_transform = []
            continue

        subrange = [int(hit) for hit in re.findall("\d+", line)]
        if subrange:
            dest_start, src_start, length = subrange
            dest_end = dest_start + length - 1
            difference = dest_start - src_start
            current_transform.append((dest_start, dest_end, difference))

    transforms.append(current_transform)
    return list(reversed(transforms))


def process_seed(seed_no, data):
    result = seed_no

    for transform in data:
        for start, end, difference in transform:
            if result >= start and result < end:
                result -= difference
                break

    return result


def part1(data):
#     data = """seeds: 79 14 55 13

# seed-to-soil map:
# 50 98 2
# 52 50 48

# soil-to-fertilizer map:
# 0 15 37
# 37 52 2
# 39 0 15

# fertilizer-to-water map:
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4

# water-to-light map:
# 88 18 7
# 18 25 70

# light-to-temperature map:
# 45 77 23
# 81 45 19
# 68 64 13

# temperature-to-humidity map:
# 0 69 1
# 1 0 69

# humidity-to-location map:
# 60 56 37
# 56 93 4"""

    split_data = data.splitlines()
    seed_data, map_data = split_data[0], split_data[2:]
    seeds = [int(hit) for hit in re.findall(r"\d+", seed_data)]

    transform_data = get_transform_data_p1(map_data)

    print(seeds)
    results = [process_seed(seed, transform_data) for seed in seeds]
    # print(results)
    return min(results)


def part2(data):
#     data = """seeds: 79 14 55 13

# seed-to-soil map:
# 50 98 2
# 52 50 48

# soil-to-fertilizer map:
# 0 15 37
# 37 52 2
# 39 0 15

# fertilizer-to-water map:
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4

# water-to-light map:
# 88 18 7
# 18 25 70

# light-to-temperature map:
# 45 77 23
# 81 45 19
# 68 64 13

# temperature-to-humidity map:
# 0 69 1
# 1 0 69

# humidity-to-location map:
# 60 56 37
# 56 93 4"""

    split_data = data.splitlines()
    seed_data, map_data = split_data[0], split_data[2:]
    seeds = (int(hit) for hit in re.findall(r"\d+", seed_data))

    seed_ranges = [(start, start + length - 1) for start, length in itertools.batched(seeds, 2)]
    transform_data = get_transform_data_p2(map_data)

    found = False
    for location_no in itertools.count():
        result = location_no
        # print(f"Trying location {location_no}")
        for transform in transform_data:
            for start, end, difference in transform:
                if result >= start and result <= end:
                    # print(f"Updating current result: {result}")
                    result -= difference
                    # print(f"{result=}")
                    # print("----------")
                    break

        for range_start, range_end in seed_ranges:
            if result >= range_start and result <= range_end:
                found = True
                break

        if found:
            break

    return location_no