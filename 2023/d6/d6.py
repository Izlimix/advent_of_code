#!/usr/bin/env python3
import math
from tqdm import tqdm

# https://adventofcode.com/2023/day/6

"""
I feel a bit bad about brute-forcing this one. Having the loading bar from tqdm really makes estimating the time remaining easy!
(Though a little less bad considering I did this one at 1am)
Would like to come back and do a more mathy solution to this one at some pt
"""

def part1(lines):
    times = lines[0].split()[1:]
    records = lines[1].split()[1:]
    total_wins = []

    for (t, r) in zip(times, records):
        t, r = int(t), int(r)
        # What's the number of ways we can beat the record of this race?
        total_wins.append(race(t, r))
        print(total_wins[-1])
        
    print(f"Part 1: {math.prod(total_wins)} ")
    

def part2(lines):
    t = lines[0].split(":")[1].replace(" ", "")
    r = lines[1].split(":")[1].replace(" ", "")

    t, r = int(t), int(r)
    # What's the number of ways we can beat the record of this race?
    wins = race(t, r)
    print(f"Part 2: {wins} ")


# def race(t, record, speed=0):
def race(t, record):
    # distance = time remaining * speed
    # Screw it, brute force!
    speed = 0
    wins = 0
    for i in tqdm(range(t)):
        # Will we win if we let go now?
        if (t - i) * speed > record:
            wins += 1
        elif wins > 0:
            # We won't win any more rounds
            break
        speed += 1
    return wins


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip()
    
    lines = data.strip().split("\n")

    # part1(lines)
    print("--------")
    part2(lines)
    