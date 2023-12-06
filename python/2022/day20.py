from collections import deque


EXAMPLE_DATA = """1
2
-3
3
-2
0
4"""


class Rotator:
    def __init__(self, initial_state):
        self.items = deque(initial_state)
        self.length = len(self.items)

    def find(self, item):
        for i in range(self.length):
            if self.items[i] == item:
                break
        else:
            raise ValueError("Item not found in queue")
        
        # Push the item to the end of the queue
        rotate_amount = -((i + 1) % self.length)
        self.items.rotate(rotate_amount)

    def move_end_item(self, rotate_amount):
        moving_item = self.items.pop()
        self.items.rotate(-rotate_amount)
        self.items.append(moving_item)

    def score(self):
        for i in range(self.length):
            if self.items[i][0] == 0:
                break
        else:
            raise ValueError("Zero not found in queue")

        self.items.rotate(-i)

        first = self.items[1000 % self.length][0]
        second = self.items[2000 % self.length][0]
        third = self.items[3000 % self.length][0]

        print((first, second, third))
        return first + second + third


def part1(data):
    # data = EXAMPLE_DATA

    initial_state = [(int(line), pos) for pos, line in enumerate(data.splitlines())]

    rotator = Rotator(initial_state=initial_state)
    for item in initial_state:
        # print(f"Locating item {item}")
        rotator.find(item)
        rotator.move_end_item(item[0])

    return rotator.score()


def part2(data):
    # data = EXAMPLE_DATA

    DECRYPTION_KEY = 811589153
    MIX_AMOUNT = 10

    initial_state = [(int(line) * DECRYPTION_KEY, pos) for pos, line in enumerate(data.splitlines())]

    rotator = Rotator(initial_state=initial_state)
    for _ in range(MIX_AMOUNT):
        for item in initial_state:
            # print(f"Locating item {item}")
            rotator.find(item)
            rotator.move_end_item(item[0])

    return rotator.score()