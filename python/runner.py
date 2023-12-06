import argparse
import importlib
import time

from aocd import get_data, submit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Python Advent of Code runner",
        description="CLI tool to run given Year/Day/Part components of AoC problems",
    )
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)
    parser.add_argument("part", type=int)
    parser.add_argument("-s", "--submit", action="store_true")

    args = parser.parse_args()
    year, day, part = args.year, args.day, args.part

    data = get_data(day=day, year=year)
    module = importlib.import_module(f"{year}.day{day}")
    func = getattr(module, f"part{part}")

    start = time.time()
    result = func(data)
    end = time.time()
    print(result)
    print(f"Execution time: {end - start}")


    if args.submit:
        part = "a" if args.part == 1 else "b"
        submit(result, part=part, day=args.day, year=args.year)

