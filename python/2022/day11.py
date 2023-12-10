import re
from collections import deque

from common.parsing import parse_numbers


MONKEY_OP = re.compile(r"\s*Operation: new = old (.) (.*)")
MONKEY_MAP = {}

class Monkey:
    def __init__(self, id, items, op, const, test, true_target, false_target):
        self.id = id
        self._items = deque(items)
        self.multiply = op == "*"
        self.const = const
        self.test = test
        self.true_target = true_target
        self.false_target = false_target
        self.inspections = 0

    def __repr__(self):
        return f"Monkey {self.id}"

    def add_item(self, value):
        self._items.append(value)

    def apply_operation(self, value):
        const = value if self.const == "old" else int(self.const)
        if self.multiply:
            return value * const
        return value + const

    def process(self):
        while len(self._items) != 0:
            self.inspections += 1
            item = self._items.popleft()
            # print(f"Inspecting item: {item}")
            new_value = self.apply_operation(item)
            # print(f"Worry increased to {new_value}")
            new_value = new_value // 3
            # print(f"Worry decreased to {new_value}")

            target = self.true_target if new_value % self.test == 0 else self.false_target
            # print(f"Passing item {new_value} to Monkey {target}")

            MONKEY_MAP[target].add_item(new_value)


def part1(data):
    data_gen = (line for line in data.splitlines())

    while True:
        try:
            id = parse_numbers(next(data_gen))[0]
            items = parse_numbers(next(data_gen))
            op, const = MONKEY_OP.match(next(data_gen)).groups()
            test = parse_numbers(next(data_gen))[0]
            true_target = parse_numbers(next(data_gen))[0]
            false_target = parse_numbers(next(data_gen))[0]

            monkey = Monkey(
                id=id,
                items=items,
                op=op,
                const=const,
                test=test,
                true_target=true_target,
                false_target=false_target,
            )

            MONKEY_MAP[id] = monkey
            next(data_gen)  # Remove blank line

        except StopIteration:
            break

    for _ in range(20):
        for monkey in MONKEY_MAP.values():
            monkey.process()

    inspections = sorted(MONKEY_MAP.values(), key=lambda m: m.inspections, reverse=True)
    return inspections[0].inspections * inspections[1].inspections


class Item:
    def __init__(self, value):
        self.value = value
        self.modulo = 0

    def set_value(self, value, modulo_quantity):
        modulo_count, new_value = divmod(value, modulo_quantity)
        self.modulo += modulo_count
        self.value = new_value


class MonkeyV2(Monkey):
    def process(self):
        while len(self._items) != 0:
            self.inspections += 1
            item = self._items.popleft()
            # print(f"Inspecting item: {item}")
            new_value = self.apply_operation(item.value)
            item.set_value(new_value, self.modulo)

            target = self.true_target if new_value % self.test == 0 else self.false_target

            MONKEY_MAP[target].add_item(item)

    def set_modulo(self, modulo):
        self.modulo = modulo


def part2(data):
    data_gen = (line for line in data.split("\n"))
    MODULO = 1

    while True:
        try:
            id = parse_numbers(next(data_gen))[0]
            items = parse_numbers(next(data_gen))
            op, const = MONKEY_OP.match(next(data_gen)).groups()
            test = parse_numbers(next(data_gen))[0]
            true_target = parse_numbers(next(data_gen))[0]
            false_target = parse_numbers(next(data_gen))[0]

            MODULO *= test

            monkey = MonkeyV2(
                id=id,
                items=(Item(item) for item in items),
                op=op,
                const=const,
                test=test,
                true_target=true_target,
                false_target=false_target,
            )

            MONKEY_MAP[id] = monkey
            next(data_gen)  # Remove blank line

        except StopIteration:
            break

    for monkey in MONKEY_MAP.values():
        monkey.set_modulo(MODULO)

    for _ in range(10_000):
        for monkey in MONKEY_MAP.values():
            monkey.process()

    inspections = sorted(MONKEY_MAP.values(), key=lambda m: m.inspections, reverse=True)
    return inspections[0].inspections * inspections[1].inspections
