from collections import deque
from aocd import get_data, submit


EXAMPLE_DATA = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""


MONKEY_NUMS = {}
MONKEY_QUEUE = deque()
MONKIES = {}


class MonkeyBusiness(Exception):
    pass


class Monkey:
    def __init__(self, id, config):
        self.id = id

        match config.split(" "):
            case [num]:
                self.num = int(num)
            case [left, op, right]:
                self.left = left
                self.right = right
                self.op = op
                self.num = None

    def __repr__(self):
        return f"Monkey ({self.id})"

    def do_operation(self):
        if self.num is not None:
            return self.num

        left = MONKEY_NUMS[self.left]
        right = MONKEY_NUMS[self.right]

        if left is None or right is None:
            raise MonkeyBusiness()

        return eval(f"{left} {self.op} {right}")
    

class MonkeyV2:
    def __init__(self, id, config):
        self.id = id

        match config.split(" "):
            case [num]:
                self.num = int(num)
            case [left, op, right]:
                self.left = left
                self.right = right
                self.op = op if self.id != "root" else "=="
                self.num = None

        if self.id == "humn":
            self.num = "{}"

    def __repr__(self):
        return f"Monkey ({self.id})"

    def get_expression(self):
        # print(self)
        if isinstance(self.num, int) or isinstance(self.num, str):
            return self.num

        left = MONKIES[self.left].get_expression()
        right = MONKIES[self.right].get_expression()

        if isinstance(left, int) and isinstance(right, int):
            return eval(f"int({left} {self.op} {right})")

        # print(f"({left} {self.op} {right})")
        return f"({left} {self.op} {right})"


def part1(data):
    # data = EXAMPLE_DATA

    for monkey_data in data.splitlines():
        monkey_id, monkey_config = monkey_data.split(": ")
        monkey = Monkey(monkey_id, monkey_config)
        MONKEY_NUMS[monkey_id] = None
        MONKEY_QUEUE.append(monkey)

    while len(MONKEY_QUEUE):
        monkey = MONKEY_QUEUE.popleft()

        try:
            MONKEY_NUMS[monkey.id] = monkey.do_operation()
        except MonkeyBusiness:
            MONKEY_QUEUE.append(monkey)

    return MONKEY_NUMS["root"]


def part2(data):
    # data = EXAMPLE_DATA

    for monkey_data in data.splitlines():
        monkey_id, monkey_config = monkey_data.split(": ")
        monkey = MonkeyV2(monkey_id, monkey_config)
        MONKIES[monkey_id] = monkey


    root_monkey = MONKIES["root"]
    expression = root_monkey.get_expression()
    print(expression)

    test_num = 0
    while True:
        if eval(expression.format(test_num)):
            break
        test_num += 1

    return test_num