import re
from enum import Enum
from math import ceil

from aocd import get_data, submit

class RobotType(Enum):
    ORE = 1
    CLAY = 2
    OBSIDIAN = 3
    GEODE = 4

TIME_LIMIT = 24

data = get_data(day=19, year=2022)
data = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

INPUT_RE = re.compile("Blueprint (\d*): Each ore robot costs (\d*) ore. Each clay robot costs (\d*) ore. Each obsidian robot costs (\d*) ore and (\d*) clay. Each geode robot costs (\d*) ore and (\d*) obsidian")

class RobotFactory:
    def __init__(self, blueprint: int, ore_bot_ore_cost: int, clay_bot_ore_cost: int, obs_bot_ore_cost: int, obs_bot_clay_cost: int, geode_bot_ore_cost: int, geode_bot_obs_cost: int):
        self.blueprint = blueprint
        self.costs = {
            RobotType.ORE: {
                RobotType.ORE: ore_bot_ore_cost,
                RobotType.CLAY: None,
                RobotType.OBSIDIAN: None,
                RobotType.GEODE: None,
            },
            RobotType.CLAY: {
                RobotType.ORE: clay_bot_ore_cost,
                RobotType.CLAY: None,
                RobotType.OBSIDIAN: None,
                RobotType.GEODE: None,
            },
            RobotType.OBSIDIAN: {
                RobotType.ORE: obs_bot_ore_cost,
                RobotType.CLAY: obs_bot_clay_cost,
                RobotType.OBSIDIAN: None,
                RobotType.GEODE: None,
            },
            RobotType.GEODE: {
                RobotType.ORE: geode_bot_ore_cost,
                RobotType.CLAY: None,
                RobotType.OBSIDIAN: geode_bot_obs_cost,
                RobotType.GEODE: None,
            },
        }
        self.robots = {
            RobotType.ORE: 1,
            RobotType.CLAY: 0,
            RobotType.OBSIDIAN: 0,
            RobotType.GEODE: 0,
        }
        self.stockpile = {
            RobotType.ORE: 0,
            RobotType.CLAY: 0,
            RobotType.OBSIDIAN: 0,
            RobotType.GEODE: 0,
        }
        
        self.forecast()

    def __repr__(self):
        return f"RobotFactory (Blueprint {self.blueprint})"

    def show_bots(self):
        for bot_type, count in self.robots.items():
            print(f"{bot_type.name} Robots: {count}")

    def can_build_target(self):
        return all(
            stockpile >= cost
            for stockpile, cost in zip(self.stockpile.values(), self.costs[self.target].values())
            if cost is not None
        )

    def get_bot_forecast(self, bot_type):
        costs = []
        for resource_type in RobotType:
            resource_cost = self.costs[bot_type][resource_type]
            if resource_cost is None:
                continue
            
            resource_income = self.robots[resource_type]
            if resource_income == 0:
                return TIME_LIMIT

            adjusted_cost = resource_cost - self.stockpile[resource_type]
            costs.append(ceil(adjusted_cost / resource_income))
        return max(costs)

    def forecast(self):
        time_until_build = {
            RobotType.ORE: self.get_bot_forecast(RobotType.ORE),
            RobotType.CLAY: self.get_bot_forecast(RobotType.CLAY),
            RobotType.OBSIDIAN: self.get_bot_forecast(RobotType.OBSIDIAN),
            RobotType.GEODE: self.get_bot_forecast(RobotType.GEODE),
        }
        print(time_until_build)
        breakpoint()

        # if time_until_build[RobotType.ORE]
        # self.target = sorted(time_until_build, key=lambda t: t[0])[0][1]

    def gather_resources(self):
        for resource_type, resource_increase in self.robots.items():
            self.stockpile[resource_type] += resource_increase
        print(f"Stockpile post-update: {self.stockpile}")

    def add_target_bot(self):
        self.robots[self.target] += 1
        for resource_type, resource_cost in self.costs[self.target].items():
            if resource_cost is None:
                continue
            self.stockpile[resource_type] -= resource_cost
        print(f"Stockpile after build: {self.stockpile}")
        self.forecast()

print("-------------------------")
for config in data.splitlines():
    factory_config = (int(group) for group in INPUT_RE.match(config).groups())
    factory = RobotFactory(*factory_config)

    for i in range(TIME_LIMIT):
        print(f"Iteration {i + 1}")

        queue_build = factory.can_build_target()
        if queue_build:
            print(f"Beginning build of robot {factory.target}")
        else:
            print(f"Unable to build target robot {factory.target}")

        factory.gather_resources()

        if queue_build:
            print(f"Finished build of robot {factory.target}")
            factory.add_target_bot()

        print("-------------------------")
        breakpoint()


# print(total)
# submit(total, part="a", day=19, year=2022)