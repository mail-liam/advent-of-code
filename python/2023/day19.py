import dataclasses
import operator
import re
from collections import defaultdict, deque
from copy import deepcopy

from common.parsing import parse_numbers

EXAMPLE_DATA = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

CONDITON_RE = re.compile(r"([x|m|a|s])([<|>])(\d+)")
DEBUG = False


def debug_print(message):
    if DEBUG:
        print(message)


@dataclasses.dataclass
class MachinePart:
    x: int
    m: int
    a: int
    s: int

    def __repr__(self):
        return f"Part ({self.x}, {self.m}, {self.a}, {self.s})"

    def get_value(self):
        return self.x + self.m + self.a + self.s


class WorkflowRule:
    def __init__(self, condition, result):
        self.result = result

        if condition is True:
            self.accept = lambda _: self.result
            self.condition = "Always True"
        else:
            attribute, comparator, magnitude = CONDITON_RE.match(condition).groups()
            compare_func = operator.lt if comparator == "<" else operator.gt
            self.accept = lambda mp: self.result if compare_func(getattr(mp, attribute), int(magnitude)) else False
            self.condition = f"{attribute} {comparator} {magnitude}"

    def __repr__(self):
        return self.condition


class Workflow:
    def __init__(self, rule_data):
        self.rules = []

        for data in rule_data.split(","):
            match data.split(":"):
                case [condition, result]:
                    self.rules.append(WorkflowRule(condition, result))
                case [result]:
                    self.rules.append(WorkflowRule(True, result))

    def process_part(self, part):
        for rule in self.rules:
            result = rule.accept(part)

            if result is False:
                debug_print("No match, proceeding to next rule")
                continue

            return result


def part1(data):
    # data = EXAMPLE_DATA

    WORKFLOWS = {}

    data_gen = iter(data.splitlines())

    while True:
        workflow_data = next(data_gen)

        if not workflow_data:
            break

        rules_start = workflow_data.find("{")
        name, rule_data = workflow_data[:rules_start], workflow_data[rules_start + 1:-1]

        WORKFLOWS[name] = Workflow(rule_data)

    machine_parts = [MachinePart(*parse_numbers(part)) for part in data_gen]

    accepted_parts = []
    for part in machine_parts:
        result = "in"

        debug_print(f"Inputting part {part} to workflow {result}")
        while result is not True and result is not False:
            result = WORKFLOWS[result].process_part(part)
            debug_print(f"Workflow result: {result}")

            if result == "R":
                break

            if result == "A":
                accepted_parts.append(part)
                break

    return sum(part.get_value() for part in accepted_parts)


class State:
    def __init__(self, node):
        self.accepted = None
        self.conditions = defaultdict(list)
        self.node = node

    @classmethod
    def copy(cls, state):
        copied_state = cls(state.node)
        copied_state.accepted = state.accepted
        copied_state.conditions = deepcopy(state.conditions)

        return copied_state

    def __repr__(self):
        return f"State ({self.node}) {self.conditions}"

    def get_value(self):
        total = 1
        for condition_key in ("x", "m", "a", "s"):
            accepted_values = set(range(4000))

            for restriction in self.conditions[condition_key]:
                accepted_values.intersection_update(restriction)

            total *= len(accepted_values)

        return total


class WorkflowV2:
    def __init__(self, rule_data):
        self.rules = []

        for data in rule_data.split(","):
            match data.split(":"):
                case [condition, result]:
                    attribute, comparator, magnitude = CONDITON_RE.match(condition).groups()
                    self.rules.append((attribute, comparator, int(magnitude), result))
                case [result]:
                    self.rules.append((True, result))

    def process(self, state):
        return_states = []
        prev_state = state
        for rule in self.rules:
            match rule:
                case attribute, comparator, magnitude, result:
                    magnitude -= 1
                    success_state = State.copy(prev_state)
                    fail_state = State.copy(prev_state)
                    if comparator == "<":
                        condition = range(magnitude)
                        condition_fail = range(magnitude, 4000)
                    else:
                        condition = range(magnitude + 1, 4000)
                        condition_fail = range(magnitude + 1)
                    success_state.conditions[attribute].append(condition)
                    success_state.node = result
                    fail_state.conditions[attribute].append(condition_fail)

                    return_states.append(success_state)
                    prev_state = fail_state
                case _, result:
                    prev_state.node = result
                    return_states.append(prev_state)

        return return_states


def part2(data):
    # data = EXAMPLE_DATA

    WORKFLOWS = {}

    data_gen = iter(data.splitlines())

    while True:
        workflow_data = next(data_gen)

        if not workflow_data:
            break

        rules_start = workflow_data.find("{")
        name, rule_data = workflow_data[:rules_start], workflow_data[rules_start + 1:-1]

        WORKFLOWS[name] = WorkflowV2(rule_data)

    initial_state = State("in")
    queue = deque()
    queue.append(initial_state)

    total = 0
    while queue:
        current_state = queue.popleft()
        next_states = WORKFLOWS[current_state.node].process(current_state)

        for state in next_states:
            if state.node == "A":
                total += state.get_value()
                continue

            if state.node == "R":
                continue

            queue.append(state)

    return total
