from collections import deque
from itertools import cycle

from common.grid import Point, ADJACENT_SQUARES, CARDINAL_TO_POINTS


DIRECTIONS = ["N", "S", "W", "E"]
ELF_POSITIONS = {}
INITIAL_DIRECTION = cycle(DIRECTIONS)

def process_state() -> bool:
    direction = next(INITIAL_DIRECTION)
    proposed_directions = [elf.propose_direction(direction) for elf in ELF_POSITIONS.values()]
    if all(direction is None for direction in proposed_directions):
        return True

    for elf in ELF_POSITIONS.values():
        elf.can_change_position()

    for elf in [elf for elf in ELF_POSITIONS.values() if elf.should_update]:
        elf.update()

    # print([elf.position for elf in ELF_POSITIONS.values()])
    return False

EXAMPLE_DATA = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

class Elf:
    def __init__(self, start_row, start_col):
        self.start = start_row, start_col
        self.position = Point(start_row, start_col)
        ELF_POSITIONS[self.position.coordinate] = self
        self.desired_target = None
        self.should_update = False

    def __eq__(self, other):
        return self.start == other.start

    def propose_direction(self, start_direction):
        self.desired_target = None
        for modifier in ADJACENT_SQUARES:
            new_pos = self.position + modifier
            if new_pos.coordinate in ELF_POSITIONS:
                break
        else:
            return

        direction_order = deque(DIRECTIONS)
        while direction_order[0] != start_direction:
            direction_order.rotate(-1)

        while len(direction_order):
            current_direction = direction_order.popleft()
            # print(f"Checking direction {current_direction}")
            check_dirs = [self.position + modifier for modifier in CARDINAL_TO_POINTS[current_direction]]
            if all(position.coordinate not in ELF_POSITIONS for position in check_dirs):
                self.desired_target = check_dirs[1]
                # print(f"Proposing movement from {self.position} to {self.desired_target}")
                return current_direction

    def can_change_position(self):
        if self.desired_target is None:
            return

        other_targets = {elf.desired_target.coordinate for elf in ELF_POSITIONS.values() if elf is not self and elf.desired_target is not None}
        if self.desired_target.coordinate not in other_targets:
            self.should_update = True

    def update(self):
        del ELF_POSITIONS[self.position.coordinate]
        self.position = self.desired_target
        ELF_POSITIONS[self.desired_target.coordinate] = self
        self.should_update = False


def part1(data):
    # data = EXAMPLE_DATA

    for row, line in enumerate(data.splitlines()):
        for column, data in enumerate(line):
            if data == "#":
                Elf(row, column)

    rounds = 0
    while rounds < 10:
        if process_state():
            break
        rounds += 1

    print(rounds)
    rows = [position[0] for position in ELF_POSITIONS]
    cols = [position[1] for position in ELF_POSITIONS]
    area = (max(rows) - min(rows) + 1) * (max(cols) - min(cols) + 1)

    return area - len(ELF_POSITIONS)


def part2(data):
    # data = EXAMPLE_DATA

    for row, line in enumerate(data.splitlines()):
        for column, data in enumerate(line):
            if data == "#":
                Elf(row, column)
    
    rounds = 0
    while True:
        if process_state():
            rounds += 1
            break
        rounds += 1

    return rounds