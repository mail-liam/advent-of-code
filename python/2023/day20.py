import itertools
from collections import deque

EXAMPLE_DATA = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""


class FlipFlop:
    def __init__(self, name, targets):
        self.name = name
        self.state = False
        self.targets = tuple(targets.split(", "))

    def __repr__(self):
        return f"FlipFlop ({self.name}) -> {self.targets}"

    def process(self, packet):
        _, pulse = packet
        if pulse:
            return []  # ignore high pulses
        self.state = not self.state

        return [(target, (self.name, self.state)) for target in self.targets]


class NandGate:
    def __init__(self, name, targets):
        self.mem = {}
        self.name = name
        self.state = True
        self.targets = tuple(targets.split(", "))

    def __repr__(self):
        return f"NandGate ({self.name}) -> {self.targets}"

    def process(self, packet):
        name, pulse = packet
        self.mem[name] = pulse
        self.state = not all(self.mem.values())

        return [(target, (self.name, self.state)) for target in self.targets]


def part1(data):
    # data = EXAMPLE_DATA

    MODULES = {}

    broadcast_targets = None
    for line in data.splitlines():
        type, targets = line.split(" -> ")
        module_type, name = type[0], type[1:]
        if module_type == "b":
            broadcast_targets = tuple(targets.split(", "))
            continue

        cls = FlipFlop if module_type == "%" else NandGate
        MODULES[name] = cls(name, targets)

    # Register senders with NandGates
    for nand_gate in (module for module in MODULES.values() if isinstance(module, NandGate)):
        nand_name = nand_gate.name
        for name, module in MODULES.items():
            if nand_name in module.targets:
                nand_gate.mem[name] = False
    

    high_pulses = 0
    low_pulses = 0

    for _ in range(1000):
        queue = deque()
        # Push button
        button_outputs = ((target, ("broadcaster", False)) for target in broadcast_targets)
        queue.extend(button_outputs)
        low_pulses += 1

        while queue:
            # print(queue)
            # breakpoint()
            target, pulse = queue.popleft()

            if pulse[1]:
                high_pulses += 1
            else:
                low_pulses += 1

            target_module = MODULES.get(target)
            if target_module is None:
                continue

            return_pulses = target_module.process(pulse)
            queue.extend(return_pulses)

    return high_pulses * low_pulses


def part2(data):
    # data = EXAMPLE_DATA

    MODULES = {}

    broadcast_targets = None
    for line in data.splitlines():
        type, targets = line.split(" -> ")
        module_type, name = type[0], type[1:]
        if module_type == "b":
            broadcast_targets = tuple(targets.split(", "))
            continue

        cls = FlipFlop if module_type == "%" else NandGate
        MODULES[name] = cls(name, targets)

    # Register senders with NandGates
    for nand_gate in (module for module in MODULES.values() if isinstance(module, NandGate)):
        nand_name = nand_gate.name
        for name, module in MODULES.items():
            if nand_name in module.targets:
                nand_gate.mem[name] = False


    high_pulses = 0
    low_pulses = 0
    rx_found = False

    for i in itertools.count(1):
        queue = deque()
        # Push button
        button_outputs = ((target, ("broadcaster", False)) for target in broadcast_targets)
        queue.extend(button_outputs)
        low_pulses += 1

        while queue:
            # print(queue)
            # breakpoint()
            target, pulse = queue.popleft()

            if pulse[1]:
                high_pulses += 1
            else:
                low_pulses += 1

            target_module = MODULES.get(target)
            if target_module is None:
                continue

            return_pulses = target_module.process(pulse)

            if any(packet[0] == "rx" and packet[1][1] is False for packet in return_pulses):
                rx_found = True
                break
            queue.extend(return_pulses)

        if rx_found:
            break

    return i
