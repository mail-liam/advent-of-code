import re
import typing as t
from enum import Enum
from math import ceil

from aocd import get_data, submit

class ResourceType(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3

DEBUG = False
TIME_LIMIT = 24

data = get_data(day=19, year=2022)
# data = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
# Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

INPUT_RE = re.compile("Blueprint (\d*): Each ore robot costs (\d*) ore. Each clay robot costs (\d*) ore. Each obsidian robot costs (\d*) ore and (\d*) clay. Each geode robot costs (\d*) ore and (\d*) obsidian")

class BlueprintCosts:
    def __init__(self, ore_bot_ore_cost: int, clay_bot_ore_cost: int, obs_bot_ore_cost: int, obs_bot_clay_cost: int, geode_bot_ore_cost: int, geode_bot_obs_cost: int):
        self.costs = (
            (ore_bot_ore_cost, 0, 0, 0),
            (clay_bot_ore_cost, 0, 0, 0),
            (obs_bot_ore_cost, obs_bot_clay_cost, 0, 0),
            (geode_bot_ore_cost, 0, geode_bot_obs_cost, 0),
        )

    def get_cost_for_robot_type(self, resource: ResourceType):
        return self.costs[resource.value]

    def get_highest_requirement_for(self, resource: ResourceType):
        return max(cost[resource.value] for cost in self.costs)


def debug_print(message):
    if DEBUG:
        print(message)


def pay_robot_cost(stockpile, cost):
    return tuple(
        res_stock - res_cost
        for res_stock, res_cost in zip(stockpile, cost)
    )


def update_robot_count(incomes: t.Tuple[int], resource: ResourceType):
    return tuple(
        income + 1 if index == resource.value else income
        for index, income in enumerate(incomes)
    )


def update_stockpile(stockpile: t.Tuple[int], incomes: t.Tuple[int], elapsed_time: int):
    return tuple(
        resource_stockpile + (income * elapsed_time)
        for resource_stockpile, income in zip(stockpile, incomes)
    )



def build_robot(
    blueprints: BlueprintCosts,
    robot_count: t.Tuple[int],
    stockpile: t.Tuple[int],
    time_left: int,
):
    geode_counts = set()
    for robot in ResourceType:
        # debug_print(f"Analyzing {robot.name} robot")
        if robot != ResourceType.GEODE and robot_count[robot.value] >= blueprints.get_highest_requirement_for(robot):  # Actually resource here
            # debug_print(f"Already met maximum requirement for {robot.name} robot ({robot_count[robot.value]})")
            continue

        time_until_cost_met = []
        for i, (cost, available, income) in enumerate(zip(blueprints.get_cost_for_robot_type(robot), stockpile, robot_count)):
            # debug_print(f"Calculating resource {ResourceType(i).name}")
            # debug_print(f"Robot cost: {cost} | available resources: {available} | current count: {income}")

            if cost == 0:
                # debug_print(f"Skipping as {robot.name} robot does not need {ResourceType(i).name}")
                continue
            
            missing_cost = max(cost - available, 0)
            # debug_print(f"Requires {cost} units of {ResourceType(i).name}. Have {available}, so need {missing_cost}")
            try:
                wait_time = int(ceil(missing_cost / income))
            except ZeroDivisionError:
                # debug_print(f"STOPPING ANALYSIS - no income of resource {ResourceType(i).name}")
                time_until_cost_met.append(TIME_LIMIT)  # Hacky af
                break
            # debug_print(f"It will take {wait_time} seconds to get enough {ResourceType(i)}")
            time_until_cost_met.append(wait_time)
        longest_wait = max(time_until_cost_met) + 1  # Add 1 for build time
        # debug_print(f"It will take {longest_wait} seconds to finish building {robot.name} robot")

        if longest_wait >= time_left:
            # debug_print(f"Time will run out before we can build {robot.name} robot (Needs {longest_wait} seconds, we have {time_left}).")
            continue

        # debug_print(f"Advancing state to after {robot.name} robot construction...")
        new_time_left = time_left - longest_wait
        new_robot_count = update_robot_count(robot_count, robot)
        new_stockpile = update_stockpile(stockpile, robot_count, longest_wait)
        new_stockpile = pay_robot_cost(new_stockpile, blueprints.costs[robot.value])

        # debug_print(f"New arguments to build_robot | robot_count: {new_robot_count} | stockpile: {new_stockpile} | time_left: {new_time_left}")
        geode_count = build_robot(blueprints=blueprints, robot_count=new_robot_count, stockpile=new_stockpile, time_left=new_time_left)
        geode_counts.add(geode_count)
    
    if not geode_counts:
        # debug_print("No robots viable to build. Advancing state to end of simulation...")
        final_stockpile = update_stockpile(stockpile, robot_count, time_left)
        # debug_print(f"Final stockpile at simulation end: {final_stockpile}")
        # debug_print("---------------------------------------------------")
        return final_stockpile[ResourceType.GEODE.value]

    # debug_print(f"Returning maximum of geode counts: {geode_counts} ({max(geode_counts)})")
    # debug_print("---------------------------------------------------")
    return max(geode_counts)


qualities = []
for config in data.splitlines():
    blueprint_no, *config = (int(group) for group in INPUT_RE.match(config).groups())
    print(f"Starting blueprint {blueprint_no}")
    blueprints = BlueprintCosts(*config)

    geode_count = build_robot(
        blueprints=blueprints,
        robot_count=(1, 0, 0, 0),
        stockpile=(0, 0, 0, 0),
        time_left=TIME_LIMIT,
    )
    
    print(f"Blueprint {blueprint_no} yielded {geode_count} geodes.")
    quality = blueprint_no * geode_count
    print(f"Recording quality {quality}")
    qualities.append(quality)

print(sum(qualities))
# submit(sum(qualities), part="a", day=19, year=2022)