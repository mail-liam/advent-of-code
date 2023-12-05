import re
import typing as t
from collections import deque
from copy import deepcopy
from itertools import product

from aocd import get_data, submit

data = get_data(day=16, year=2022)
# data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
# Valve BB has flow rate=13; tunnels lead to valves CC, AA
# Valve CC has flow rate=2; tunnels lead to valves DD, BB
# Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
# Valve EE has flow rate=3; tunnels lead to valves FF, DD
# Valve FF has flow rate=0; tunnels lead to valves EE, GG
# Valve GG has flow rate=0; tunnels lead to valves FF, HH
# Valve HH has flow rate=22; tunnel leads to valve GG
# Valve II has flow rate=0; tunnels lead to valves AA, JJ
# Valve JJ has flow rate=21; tunnel leads to valve II"""

DEBUG = False
INPUT_RE = re.compile("Valve (\w\w) has flow rate=(\d*); tunnel[s]? lead[s]? to valve[s]? (.*)")
UNIVERSES = deque()


def debug_print(message):
    if DEBUG:
        print(message)


class Agent:
    def __init__(self, name, universe):
        self.distance = 0
        self.name = name
        self.target = "AA"
        self.universe = universe

    def __repr__(self):
        return f"Agent {self.name}"

    def set_target(self, valve_name, distance):
        debug_print(f"Assigning valve {valve_name} (distance {distance}) to agent {self.name}")
        self.distance = distance
        self.target = valve_name

    def needs_target(self):
        return self.distance == 0 and self.universe.valves[self.target].is_open == True

    def update(self):
        if self.distance == 0:
            debug_print(f"Agent {self.name} is opening valve {self.target}")
            self.universe.open_valve(self.target)
        elif self.distance > 0:
            debug_print(f"Agent {self.name} is moving to {self.target}")
            self.distance -= 1


class Universe:
    def __init__(self, time_left, valves):
        self.elephant = Agent(name="Elephant", universe=self)
        self.elf = Agent(name="Elf", universe=self)
        self.flow_rate = 0
        self.score = 0
        self.time_left = time_left
        self.valves = valves
        self.available_valves = {valve for valve in valves.values() if valve.flow_rate != 0}

    def __repr__(self):
        return f"Universe ({self.score}) [{self.time_left} seconds left]"

    def open_valve(self, valve_name):
        valve = self.valves[valve_name]
        if valve.is_open:  # Bad hack but it's 1:30AM
            return

        self.flow_rate += valve.flow_rate
        valve.is_open = True  # ¯\_(ツ)_/¯

    def process(self):
        has_split = False
        self.score += self.flow_rate
        self.time_left -= 1

        if self.time_left == 0:
            return False

        elf_distances = []
        elephant_distances = []
        self.elf.update()
        self.elephant.update()
        if len(self.available_valves) > 0:
            if self.elf.needs_target():
                elf_distances = self.get_valve_distances_for(self.elf)
                
            if self.elephant.needs_target():
                elephant_distances = self.get_valve_distances_for(self.elephant)

        # debug_print("New targets:")
        # debug_print(f"Elf targets: {elf_distances}")
        # debug_print(f"Elephant targets: {elephant_distances}")
        
        # Split the universe!
        if len(elf_distances) > 0 and len(elephant_distances) > 0:
            has_split = True
            for (elf_target, elf_distance), (elephant_target, elephant_distance) in product(elf_distances, elephant_distances):
                if elf_target is elephant_target:
                    debug_print(f"Skipping pair due to same target: {elf_target} == {elephant_target}")
                    continue

                self.elf.set_target(elf_target.name, elf_distance)
                self.elephant.set_target(elephant_target.name, elephant_distance)

                debug_print("Spawning universe...")
                self.copy(exclude_valve_names=[elf_target.name, elephant_target.name])

        elif len(elf_distances) > 0:
            has_split = True
            for valve, dist in elf_distances:
                debug_print(f"Spawning universe by assigning valve {valve.name} ({dist}) to agent {self.elf.name}")
                self.elf.set_target(valve.name, dist)
                self.copy(exclude_valve_names=[valve.name])

        elif len(elephant_distances) > 0:
            has_split = True
            for valve, dist in elephant_distances:
                debug_print(f"Spawning universe by assigning valve {valve.name} ({dist}) to agent {self.elephant.name}")
                self.elephant.set_target(valve.name, dist)
                self.copy(exclude_valve_names=[valve.name])

        debug_print(f"Universe has {self.time_left} seconds left. Score is {self.score}")

        return has_split


    def copy(self, exclude_valve_names: t.List[str]):
        new_universe = deepcopy(self)
        
        remove_valves = {new_universe.valves[name] for name in exclude_valve_names}
        debug_print(f"Removing valves {remove_valves} from new universe available valves")
        new_universe.available_valves = new_universe.available_valves - remove_valves
        UNIVERSES.append(new_universe)

    def get_valve_distances_for(self, agent):
        debug_print(f"Spawning universes for agent {agent.name}")
        debug_print(f"Available valves: {self.available_valves}")
        if len(self.available_valves) == 0:
            return []

        location = agent.target
        seen = set()
        seen.add(location)
        to_visit = deque()
        to_visit.append((location, 0))
        processed = []

        while to_visit:
            current_name, distance = to_visit.popleft()
            if distance > self.time_left:
                break
            current_valve = self.valves[current_name]

            for name in current_valve.connections:
                if name in seen:
                    continue
                to_visit.append((name, distance + 1))
                seen.add(name)
            processed.append((current_valve, distance))

        return [p for p in processed if p[0] in self.available_valves]
        


class Valve:
    def __init__(self, name, flow_rate, connections):
        self.name = name
        self.flow_rate = flow_rate
        self.connections = connections
        self.is_open = False

    def __repr__(self):
        return f"Valve {self.name} ({self.flow_rate})."


initial_valves = {}
for line in data.splitlines():
    name, flow_rate, connections = INPUT_RE.match(line).groups()
    initial_valves[name] = Valve(name=name, flow_rate=int(flow_rate), connections=connections.split(", "))

universe = Universe(time_left=27, valves=initial_valves)

total = 0
total_universes = 0
try:
    while True:
        has_split = universe.process()

        if has_split:
            debug_print(f"Refreshing universe due to split")
            universe = UNIVERSES.pop()

        if universe.time_left == 0:
            if universe.score > total:
                print(f"Universe time has expired! Updating score (New: {universe.score}. Best: {total})")
            total = max(universe.score, total)
            total_universes += 1
            universe = UNIVERSES.pop()

        if DEBUG:
            breakpoint()
except IndexError:  # pop() when empty
    pass

print(total)
print(f"Total universes: {total_universes}")
# submit(total, part="b", day=16, year=2022)