#!/usr/bin/env python3
import math
import re
from itertools import cycle
from tqdm import tqdm

# https://adventofcode.com/2023/day/8
"""
I'm so surprised this part 2 solution works (thank you AOC for making a kind puzzle input)
"""


def part1(data):
    # Parse instructions
    instructions, map_data = data.split("\n\n")
    # Parse map
    map_pattern = r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)"
    maps = {n: (l, r) for (n, l, r) in re.findall(map_pattern, map_data)}
    
    turns = cycle(instructions)
    pos = "AAA"
    for (i, step) in tqdm(enumerate(turns)):
        if pos == "ZZZ":
            print("Reached ZZZ!")
            break
        fork = maps[pos]
        match step:
            case "L":
                pos = fork[0]
            case "R":
                pos = fork[1]
            case _:
                raise Exception(f"{pos=} {fork=} {step=}")
    print(f"Part 1: Took {i} steps")
    

def part2(data):
    # Parse instructions
    instructions, map_data = data.split("\n\n")
    # Parse map
    map_pattern = r"([A-Z\d]+) = \(([A-Z\d]+), ([A-Z\d]+)\)"
    # print(f"{instructions=}, {map_data=}")
    maps = {n: (l, r) for (n, l, r) in re.findall(map_pattern, map_data)}
    
    pos = [n for n in maps.keys() if n[2] == "A"]
    print(f"Starting positions: {pos}")
    # Option 1: Simulate each start point until you do a full cycle - reach the same node at the same instruction index
    # Option 2 (below): How many turns does it take to reach each exit? Take the LCM to find which step they coincide
    #  - Assume that the instructions will loop perfectly and take you back to the end node in the same number of steps
    #  -- this is a strong assumption, since our 2nd round could be a different length from the 1st, or there could be an initial part so it doesn't actually cycle
    #  - Fortunately for this solution, it worked!

    # Simulate each start point separately
    lowest_turns = []
    for start_p in pos:
        p = start_p
        # Number every instruction
        turns = cycle(enumerate(instructions))
        for (steps, (i, turn)) in tqdm(enumerate(turns)):
            if p[2] == "Z":
                print(f"{start_p} reached {p} in {steps} on turn {i}!")
                lowest_turns.append(steps)
                break
            fork = maps[p]
            match turn:
                case "L":
                    p = fork[0]
                case "R":
                    p = fork[1]
                case _:
                    raise Exception(f"{pos=} {[maps[n] for n in pos]} {turn=}")
    print(f"Part 2: Took {math.lcm(*lowest_turns)} steps")


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip()
    
    part1(data)
    print("--------")
    part2(data)
    