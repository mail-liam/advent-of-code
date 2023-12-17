from collections import defaultdict
from itertools import cycle

from common.grid import Point

DEBUG = False
EXAMPLE_DATA = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
RIGHT = Point(1, 0)
LEFT = Point(-1, 0)
DOWN = Point(0, -1)


class Shaft:
    def __init__(self):
        self.points = defaultdict(bool)

    def get_highest_point(self):
        return max(
            (point[1] for point in self.points if self.points[point] == True),
            default=0,
        )

    def is_solid_point(self, point: Point):
        if point.x < 1 or point.x > 7:
            return True

        if point.y < 1:
            return True

        return self.points[point.coordinate]

    def can_move(self, rock, point_modifier) -> bool:
        for point in rock.show_points:
            new_point = point + point_modifier
            if self.is_solid_point(new_point):
                return False
        return True

    def add_points(self, points):
        for point in points:
            if DEBUG:
                print(f"Making {point} solid")
            self.points[point.coordinate] = True


class Rock:
    def __init__(self, start_point):
        self.start_point = start_point

    def __repr__(self):
        return f"{self.__class__.__name__} at ({self.start_point.x}, {self.start_point.y})"

    @property
    def show_points(self):
        return [self.start_point + point for point in self.points]


class LineRock(Rock):
    def __init__(self, start_point):
        super().__init__(start_point)
        self.points = (
            Point(0, 0),
            Point(1, 0),
            Point(2, 0),
            Point(3, 0),
        )

class CrossRock(Rock):
    def __init__(self, start_point):
        super().__init__(start_point)
        self.points = (
            Point(1, 0),
            Point(0, 1),
            Point(1, 1),
            Point(2, 1),
            Point(1, 2),
        )

class CornerRock(Rock):
    def __init__(self, start_point):
        super().__init__(start_point)
        self.points = (
            Point(0, 0),
            Point(1, 0),
            Point(2, 0),
            Point(2, 1),
            Point(2, 2),
        )


class TallRock(Rock):
    def __init__(self, start_point):
        super().__init__(start_point)
        self.points = (
            Point(0, 0),
            Point(0, 1),
            Point(0, 2),
            Point(0, 3),
        )

class SquareRock(Rock):
    def __init__(self, start_point):
        super().__init__(start_point)
        self.points = (
            Point(0, 0),
            Point(0, 1),
            Point(1, 0),
            Point(1, 1),
        )


def process_rocks(total_rocks, air_data) -> Shaft:
    air_jets = cycle(air_data)
    next_rock = cycle((LineRock, CrossRock, CornerRock, TallRock, SquareRock))

    shaft = Shaft()
    for _ in range(total_rocks):
        spawn_x, spawn_y = 3, shaft.get_highest_point() + 4
        spawn_point = Point(spawn_x, spawn_y)

        rock_class = next(next_rock)
        rock = rock_class(start_point=spawn_point)
        if DEBUG:
            print(f"Spawned {rock}")

        while True:
            direction = RIGHT if next(air_jets) == ">" else LEFT

            if shaft.can_move(rock, direction):
                new_spawn = rock.start_point + direction
                rock = rock_class(new_spawn)
                if DEBUG:
                    dir_name = "right" if direction is RIGHT else "left"
                    print(f"Rock moved {dir_name}: {rock}")

            if shaft.can_move(rock, DOWN):
                new_spawn = rock.start_point + DOWN
                rock = rock_class(new_spawn)
                if DEBUG:
                    print(f"Rock moved down: {rock}")
            else:
                shaft.add_points(rock.show_points)
                break

    return shaft


def part1(data):
    # data = EXAMPLE_DATA
    TOTAL_ROCKS = 2022

    shaft = process_rocks(TOTAL_ROCKS, data)

    return shaft.get_highest_point()


def part2(data):
    # data = EXAMPLE_DATA
    TOTAL_ROCKS = 1_000_000_000_000
    PRE_PERIOD_ROCKS = 229  # 15 for testcase

    shaft = process_rocks(PRE_PERIOD_ROCKS, data)
    assert shaft.get_highest_point() == 350

    ROCKS_PER_PERIOD = 1745  # 35 for testcase
    HEIGHT_PER_PERIOD = 2778  # 53 for testcase

    # Testcase period: 1,3,3,4,0,1,2,3,0,1,1,3,2,2,0,0,2,3,4,0,1,2,1,2,0,1,2,1,2,0,1,3,2,0,0
    # Get the number of additional (full) periods needed
    periods = (TOTAL_ROCKS - PRE_PERIOD_ROCKS) // ROCKS_PER_PERIOD
    # dropped_rocks = PRE_PERIOD_ROCKS + (ROCKS_PER_PERIOD * periods)
    resume_height = shaft.get_highest_point() + (HEIGHT_PER_PERIOD * periods)

    # dropped_rocks is exactly amount required for testcase
    # total_height = resume_height
    # dropped_rocks is 999999999219, so need 781 rocks from the period + their associated height (1246)
    return resume_height + 1246