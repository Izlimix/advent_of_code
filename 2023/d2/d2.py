#!/usr/bin/env python3
import re
import operator
from collections import defaultdict
from functools import reduce

# https://adventofcode.com/2023/day/2

def part1(lines):
    # The games are in consecutive order, so we don't actually need to parse the ids
    total = 0
    max_cubes = {"red": 12, "green": 13, "blue": 14}
    round_pattern = re.compile("(?:: |; |, )")  # Also split on each cube value
    for (i, l) in enumerate(lines, 1):
        try:
            # Split the round into (value, colour) pairs.
            for round in round_pattern.split(l):
                n, colour = round.split(" ")
                # Skip the Game prefix
                if n == "Game": continue
                # If the number of balls we drew > max, then skip this game
                if int(n) > max_cubes[colour]:
                    raise StopIteration
        except StopIteration:
            # print(f"Game {id}: impossible")
            continue
        else:
            # print(f"Game {id}: ok!")
            # Got through all the rounds without going over. This game is possible!
            total += i
    print(f"Part 1: The sum of IDs of possible games is: {total}")
    
    
def part2(lines):
    total = 0
    round_pattern = re.compile("(?:: |; |, )")  # Also split on each cube value
    for l in lines:
        # Each cube value starts at 0
        min_cubes = defaultdict(int)
        # Split the round into (value, colour) pairs.
        for round in round_pattern.split(l):
            n, colour = round.split(" ")
            # Skip the Game prefix
            if n == "Game": continue
            # If n cubes > current min of that colour, update
            min_cubes[colour] = max(int(n), min_cubes[colour])
        
        # Finished all the rounds!
        # Power = R * G * B
        power = reduce(operator.mul, (min_cubes.get(colour) for colour in ["red", "green", "blue"]))
        total += power
    print(f"Part 2: The sum of powers is: {total}")


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    lines = data.strip().split("\n")

    part1(lines)
    print("--------")
    part2(lines)
    