import re
from collections import deque
from aocd import get_data, submit

MONKEY_ID = re.compile("Monkey (\d*):")
MONKEY_ITEMS = re.compile("\s*Starting items: (.*)")
MONKEY_OP = re.compile("\s*Operation: new = old (.) (.*)")
MONKEY_TEST = re.compile("\s*Test: divisible by (\d*)")
MONKEY_TRUE = re.compile("\s*If true: throw to monkey (\d*)")
MONKEY_FALSE = re.compile("\s*If false: throw to monkey (\d*)")

data = get_data(day=11, year=2022)

MONKEY_MAP = {}
MODULO_BASE = 1

class Item:
    def __init__(self, value):
        self.value = value
        self.modulo = 0

    def set_value(self, value):
        modulo, value = divmod(value, MODULO_BASE)
        self.modulo += modulo
        self.value = value

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
        self.outbox = deque()

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
            new_value = self.apply_operation(item.value)
            item.set_value(new_value)

            target = self.true_target if new_value % self.test == 0 else self.false_target
            # print(f"Queuing value {new_value} in outbox for monkey {target}")

            MONKEY_MAP[target].add_item(item)

            

data_gen = (line for line in data.split("\n"))
divisors = []

while True:
    try:
        id = int(MONKEY_ID.match(next(data_gen)).group(1))
        items = MONKEY_ITEMS.match(next(data_gen)).group(1)
        op, const = MONKEY_OP.match(next(data_gen)).groups()
        test = int(MONKEY_TEST.match(next(data_gen)).group(1))
        true_target = MONKEY_TRUE.match(next(data_gen)).group(1)
        false_target = MONKEY_FALSE.match(next(data_gen)).group(1)

        divisors.append(test)

        monkey = Monkey(
            id=id,
            items=[Item(int(item)) for item in items.split(", ")],
            op=op,
            const=const,
            test=test,
            true_target=int(true_target),
            false_target=int(false_target),
        )

        MONKEY_MAP[id] = monkey
        next(data_gen)  # Remove blank line

    except StopIteration:
        break

for divisor in divisors:
    MODULO_BASE *= divisor

for _ in range(10_000):
    for monkey in MONKEY_MAP.values():
        monkey.process()


inspections = sorted(MONKEY_MAP.values(), key=lambda m: m.inspections, reverse=True)
total = inspections[0].inspections * inspections[1].inspections
print([monkey.inspections for monkey in inspections])
print(total)
submit(total, part="b", day=11, year=2022)