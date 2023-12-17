import math
import typing as t

from common.parsing import parse_numbers

DEBUG = False
NAME = ("ORE", "CLAY", "OBSIDIAN", "GEODE")
N_RESOURCES = 4

EXAMPLE_DATA = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""


class BlueprintCosts:
    def __init__(self, ore_bot_ore_cost: int, clay_bot_ore_cost: int, obs_bot_ore_cost: int, obs_bot_clay_cost: int, geode_bot_ore_cost: int, geode_bot_obs_cost: int):
        self.costs = (
            (ore_bot_ore_cost, 0, 0, 0),
            (clay_bot_ore_cost, 0, 0, 0),
            (obs_bot_ore_cost, obs_bot_clay_cost, 0, 0),
            (geode_bot_ore_cost, 0, geode_bot_obs_cost, 0),
        )

    def get_highest_requirement_for(self, resource: int):
        if resource == 0:  # Avoid Ore bots being the most expensive
            return max(cost[resource] for cost in self.costs[1:])
        return max(cost[resource] for cost in self.costs)


def debug_print(message):
    if DEBUG:
        print(message)


def pay_robot_cost(stockpile, cost):
    return tuple(
        res_stock - res_cost
        for res_stock, res_cost in zip(stockpile, cost)
    )


def update_robot_count(incomes: t.Tuple[int], resource: int):
    return tuple(
        income + 1 if index == resource else income
        for index, income in enumerate(incomes)
    )


def update_stockpile(stockpile: t.Tuple[int], incomes: t.Tuple[int], elapsed_time: int):
    return tuple(
        resource_stockpile + (income * elapsed_time)
        for resource_stockpile, income in zip(stockpile, incomes)
    )


def build_robot(blueprints: BlueprintCosts, robot_count: t.Tuple[int], stockpile: t.Tuple[int], time_left: int, max_time: int):
    if time_left == 1:
        # debug_print(f"Final cycle: skipping robot build")
        return stockpile[3] + robot_count[3]

    geode_counts = set()
    for robot in range(N_RESOURCES):
        max_daily_requirement = blueprints.get_highest_requirement_for(robot)  # Actually resource here
        # debug_print(f"Analyzing {NAME[robot]} robot")
        if robot != 3 and robot_count[robot] >= max_daily_requirement:
            # debug_print(f"Already met maximum requirement for {NAME[robot]} robot ({robot_count[robot]})")
            continue

        if robot != 3 and (stockpile[robot] + robot_count[robot] * time_left) >= max_daily_requirement * time_left:
            # debug_print(f"Total stockpile+income already exceeds maximum possible usage (Have: {stockpile[robot] + robot_count[robot] * time_left}. Max need: {max_daily_requirement * time_left}")
            continue

        time_until_cost_met = []
        robot_cost = blueprints.costs[robot]
        for resource in range(N_RESOURCES):
            cost = robot_cost[resource]
            available = stockpile[resource]
            income = robot_count[resource]
            # debug_print(f"Calculating resource {NAME[resource]}")
            # debug_print(f"Robot cost: {cost} | available resources: {available} | current count: {income}")

            if cost == 0:
                # debug_print(f"Skipping as {NAME[robot]} robot does not need {NAME[resource]}")
                continue
            
            missing_cost = max(cost - available, 0)
            # debug_print(f"Requires {cost} units of {NAME[resource]}. Have {available}, so need {missing_cost}")
            try:
                wait_time = int(math.ceil(missing_cost / income))
            except ZeroDivisionError:
                # debug_print(f"STOPPING ANALYSIS - no income of resource {NAME[resource]}")
                time_until_cost_met.append(max_time)  # Hacky af
                break
            # debug_print(f"It will take {wait_time} seconds to get enough {NAME[resource]}")
            time_until_cost_met.append(wait_time)
        longest_wait = max(time_until_cost_met) + 1  # Add 1 for build time
        # debug_print(f"It will take {longest_wait} seconds to finish building {NAME[robot]} robot")

        if longest_wait >= time_left:
            # debug_print(f"Time will run out before we can build {NAME[robot]} robot (Needs {longest_wait} seconds, we have {time_left}).")
            continue

        # debug_print(f"Advancing state to after {NAME[robot]} robot construction...")
        new_time_left = time_left - longest_wait
        new_robot_count = update_robot_count(robot_count, robot)
        new_stockpile = update_stockpile(stockpile, robot_count, longest_wait)
        new_stockpile = pay_robot_cost(new_stockpile, robot_cost)

        # debug_print(f"New arguments to build_robot | robot_count: {new_robot_count} | stockpile: {new_stockpile} | time_left: {new_time_left}")
        geode_count = build_robot(blueprints=blueprints, robot_count=new_robot_count, stockpile=new_stockpile, time_left=new_time_left, max_time=max_time)
        geode_counts.add(geode_count)
    
    if not geode_counts:
        # debug_print("No robots viable to build. Advancing state to end of simulation...")
        final_stockpile = update_stockpile(stockpile, robot_count, time_left)
        # debug_print(f"Final stockpile at simulation end: {final_stockpile}")
        # debug_print("---------------------------------------------------")
        return final_stockpile[3]

    # debug_print(f"Returning maximum of geode counts: {geode_counts} ({max(geode_counts)})")
    # debug_print("---------------------------------------------------")
    return max(geode_counts)


def part1(data):
    # data = EXAMPLE_DATA

    TIME_LIMIT = 24
    qualities = []
    for config in data.splitlines():
        blueprint_no, *blueprint_args = parse_numbers(config)
        print(f"Starting blueprint {blueprint_no}")
        blueprints = BlueprintCosts(*blueprint_args)

        geode_count = build_robot(
            blueprints=blueprints,
            robot_count=(1, 0, 0, 0),
            stockpile=(0, 0, 0, 0),
            time_left=TIME_LIMIT,
            max_time=TIME_LIMIT,
        )
        
        print(f"Blueprint {blueprint_no} yielded {geode_count} geodes.")
        qualities.append(blueprint_no * geode_count)

    return sum(qualities)


def part2(data):
    # data = EXAMPLE_DATA

    TIME_LIMIT = 32
    score = 1
    for config in data.splitlines()[:3]:
        blueprint_no, *blueprint_args = parse_numbers(config)
        print(f"Starting blueprint {blueprint_no}")
        blueprints = BlueprintCosts(*blueprint_args)

        geode_count = build_robot(
            blueprints=blueprints,
            robot_count=(1, 0, 0, 0),
            stockpile=(0, 0, 0, 0),
            time_left=TIME_LIMIT,
            max_time=TIME_LIMIT,
        )
        
        print(f"Blueprint {blueprint_no} yielded {geode_count} geodes.")
        score *= geode_count

    return score
