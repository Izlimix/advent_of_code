#!/usr/bin/env python3

import re
import math
from collections import deque
from tqdm import tqdm

# https://adventofcode.com/2023/day/20

def part1(lines):
    # Sending a pulse: (from, to, value lo/hi)
    # List of pulses to process: queue (processed in order)
    pulses = deque()
    pattern = re.compile(r"^(.*) -> (.*)$")
    modules = dict()
    module_codes = {
        "%": Flipflop,
        "&": Conjunction
    }
    conjunctions = []
    for l in lines:
        name, target_str = pattern.match(l).groups()
        targets = [t.strip() for t in target_str.split(",")]
        op = name[0]
        if op in module_codes:
            name = name[1:]
            module = module_codes[op](name, targets)
        else:
            module = Broadcast(name, targets)
        modules[name] = module 
        if op == "&":
            conjunctions.append(name)
    # Parsing: Go through and add all the sources of the conjunction modules
    for (name, m) in modules.items():
        for c in conjunctions:
            if c in m.targets:
                modules[c].add_source(name)
    
    # The button is pushed 1000 times (waiting for all pulses to be processed between each push)
    # A bit worried that part 2 will need cycle detection again
    lows, highs = 0, 0
    for _ in tqdm(range(1000)):
        pulses.append(("button", "broadcaster", False))
        while pulses:
            p = pulses.popleft()
            p_from, p_to, value = p
            if value:
                highs += 1
            else:
                lows += 1
            # If target of pulse isn't in modules (e.g. output), skip
            if p_to not in modules:
                continue
            r = modules[p_to].run(p)
            pulses.extend(r)
    
    print(f"Part 1: {lows * highs=}")
    
def part2(lines):
    # Using https://dreampuf.github.io/GraphvizOnline/ and a manually-edited input file to explore the graph
    # -> Actually, we have a chance of solving this by looking at each of the nodes that feeds qt (which feeds rx) and seeing when they fire

    # Reset everything to default by constructing it all over again
    pulses = deque()
    pattern = re.compile(r"^(.*) -> (.*)$")
    modules = dict()
    module_codes = {
        "%": Flipflop,
        "&": Conjunction
    }
    conjunctions = []
    for l in lines:
        name, target_str = pattern.match(l).groups()
        targets = [t.strip() for t in target_str.split(",")]
        op = name[0]
        if op in module_codes:
            name = name[1:]
            module = module_codes[op](name, targets)
        else:
            module = Broadcast(name, targets)
        modules[name] = module 
        if op == "&":
            conjunctions.append(name)
    # Parsing: Go through and add all the sources of the conjunction modules
    for (name, m) in modules.items():
        for c in conjunctions:
            if c in m.targets:
                modules[c].add_source(name)
    
    # We want to find the number of button-presses needed to send a low pulse to rx
    # Attempt 1: Press the button 10 million times (arbitrary), break as soon as we process a message to rx
    # -> This takes 10 mins, and doesn't find the answer within that. Can't brute-force this way
    # Attempt 2: examine graph. For my input, we're looking for a high pulse from nodes gl, kk, mr, bb
    #  Hope that the nodes feeding these are distinct and that they cycle regularly and without an offset (they do)
    # -> A slightly more general solution here could look for the names of the nodes that feed rx,
    # and possibly do more presses to check it's a complete cycle
    target_nodes = ["gl", "kk", "mr", "bb"]
    target_presses = dict()
    try:
        for i in tqdm(range(1, 10_000_000 + 1)):
            pulses.append(("button", "broadcaster", False))
            while pulses:
                p = pulses.popleft()
                p_from, p_to, value = p
                # Attempt 2:
                if (p_from in target_nodes) and (value):
                    print(f"button press {i} - {p_from} - high pulse")
                    target_presses[p_from] = i
                    if all(n in target_presses for n in target_nodes):
                        print(f"Part 2: estimated button presses from lcm = {math.lcm(*target_presses.values())}")
                        return
                # Attempt 1: If we sent a low value to rx, we're done!
                if (p_to == "rx") and (not value):
                    raise StopIteration
                # If target of pulse isn't in modules (e.g. output), skip
                if p_to not in modules:
                    continue
                r = modules[p_to].run(p)
                pulses.extend(r)
    except StopIteration:
        pass
    print(f"Part 2: button presses = {i}")

class Broadcast:
    def __init__(self, name: str, targets: list[str]) -> None:
        self.name = name
        self.targets = targets
    
    def run(self, pulse):
        _, _, v = pulse
        # Send a pulse to each target
        return [(self.name, t, v) for t in self.targets]

class Flipflop:
    def __init__(self, name: str, targets: list[str]) -> None:
        self.name = name
        self.targets = targets
        # Initially off
        self.state = False
    
    def run(self, pulse: tuple):
        _, _, v = pulse
        # If received a low pulse, flip and send new state as a signal
        if not v:
            self.state = not self.state
            return [(self.name, t, self.state) for t in self.targets]
        else:
            return []

class Conjunction:
    def __init__(self, name: str, targets: list[str]) -> None:
        self.name = name
        self.targets = targets
        self.state = dict()

    def add_source(self, source: str):
        # Initially off for each source input
        self.state[source] = False
    
    def run(self, pulse: tuple):
        p_from, _, v = pulse
        # Update memory for that input
        self.state[p_from] = v
        # print(f"{self.name} {self.state.items()=}")
        if all(self.state.values()):
            # Remember all high -> send low
            return [(self.name, t, False) for t in self.targets]
        else:
            # Send high
            return [(self.name, t, True) for t in self.targets]



# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip() 
    
    lines = data.split("\n")
    part1(lines)
    print("--------")
    # part2(lines)
    