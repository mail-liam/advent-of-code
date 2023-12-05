from collections import deque
from aocd import get_data, submit

data = get_data(day=21, year=2022)
# data = """root: pppw + sjmn
# dbpl: 5
# cczh: sllz + lgvd
# zczc: 2
# ptdq: humn - dvpt
# dvpt: 3
# lfqf: 4
# humn: 5
# ljgn: 2
# sjmn: drzm * dbpl
# sllz: 4
# pppw: cczh / lfqf
# lgvd: ljgn * ptdq
# drzm: hmdt - zczc
# hmdt: 32"""


MONKEY_NUMS = {}
MONKEY_QUEUE = deque()


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

print(MONKEY_NUMS["root"])
# submit(total, part="a", day=21, year=2022)