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



for monkey_data in data.splitlines():
    monkey_id, monkey_config = monkey_data.split(": ")
    monkey = Monkey(monkey_id, monkey_config)
    MONKIES[monkey_id] = monkey


root_monkey = MONKIES["root"]
expression = root_monkey.get_expression()
print(expression)

test_num = 0
while True:
    if eval(expression.format(test_num)):
        break
    test_num += 1

print(test_num)
submit(test_num, part="b", day=21, year=2022)