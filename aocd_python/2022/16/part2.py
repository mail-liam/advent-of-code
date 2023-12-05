import re
from collections import deque

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

INPUT_RE = re.compile("Valve (\w\w) has flow rate=(\d*); tunnel[s]? lead[s]? to valve[s]? (.*)")
VALVE_MAP = {}

class Valve:
    def __init__(self, name, flow_rate, connections):
        self.name = name
        self.flow_rate = flow_rate
        self.connections = connections

    def __repr__(self):
        return f"Valve {self.name} ({self.flow_rate})."

    def __lt__(self, other):
        return self.flow_rate < other.flow_rate


for line in data.splitlines():
    name, flow_rate, connections = INPUT_RE.match(line).groups()
    VALVE_MAP[name] = Valve(name=name, flow_rate=int(flow_rate), connections=connections.split(", "))


def score_valve(valve, distance, timer):
    score = valve.flow_rate * (timer - distance - 1)  # One to open
    # print(f"Score for {valve} at distance {distance}: {score}")
    return max(score, 0)


def choose_valve(current_location, current_used, current_total, timer):
    totals = []
    seen = set()
    seen.add(current_location)
    to_visit = deque()
    to_visit.append((current_location, 0))
    processed = []

    while to_visit:
        current_name, distance = to_visit.popleft()
        if distance > timer:
            break
        current_valve = VALVE_MAP[current_name]

        for name in current_valve.connections:
            if name in seen:
                continue
            to_visit.append((name, distance + 1))
            seen.add(name)
        processed.append((current_valve, distance))


    for valve, dist in processed:
        if valve.name in current_used:
            continue

        score = score_valve(valve, dist, timer)
        if score == 0:
            continue

        new_location = valve.name
        new_used = current_used.union({new_location})
        new_total = current_total + score
        new_timer = timer - dist - 1
        # print(f"""Recursively calling choose_value:
        # new_location={new_location}
        # new_used={new_used}
        # current_total={new_total}
        # timer={new_timer}""")

        total = choose_valve(
            current_location=new_location,
            current_used=new_used,
            current_total=new_total,
            timer=new_timer,
        )
        totals.append(total)
    if not totals:
        highest_total = current_total, []
    else:
        highest_total = sorted(totals)[-1]
    highest_total[1].append(current_location)
    # print(f"Returning total: {highest_total}")
    return highest_total


total, path = choose_valve(current_location="AA", current_used={"BT"}, current_total=0, timer=26)

print(total)
print(list(reversed(path)))

total2, path2 = choose_valve(current_location="AA", current_used=set(path), current_total=0, timer=26)

print(total2)
print(list(reversed(path2)))

print(f"Combined total: {total + total2}")
# submit(total, part="a", day=16, year=2022)