#!/usr/bin/env python3
import re
from functools import cache
from tqdm import tqdm

# https://adventofcode.com/2023/day/12


def part1(lines):
    # I could make a monster of an overlapping regex here based on the numbers?
    total = 0
    for l in tqdm(lines):
        record, springs = l.split(" ")
        springs = tuple(map(int, springs.split(",")))
        arrangements = place_springs(record, springs)
        total += arrangements
        # print(f"Found {arrangements} arrangements!")
    
    print(f"Part 1 cache stats: {place_springs.cache_info()}")
    print(f"Part 1: {total=}")
    

def part2(lines):
    # Let's just try again but cache this time
    total = 0
    for l in tqdm(lines):
        record, springs = l.split(" ")
        record = "?".join([record for _ in range(5)])
        springs = tuple(map(int, springs.split(",") * 5))
        
        # Look for the next place in line that could hold n springs,
        #  and that's followed by a ., a ?, or the end of the string
        arrangements = place_springs(record, springs)
        total += arrangements
        # print(f"Found {arrangements} arrangements!")
    
    print(f"Part 2 cache stats (incl p1): {place_springs.cache_info()}")
    print(f"Part 2: {total=}")

@cache
def place_springs(line, springs, depth=0):
    # prefix = "-" * depth
    # print(f"{prefix}Looking in {line=} for {springs=}")
    if not springs:
        # We've finished assigning all the springs!
        if "#" in line:
            # If there are any fixed springs left, we've failed
            # print(f"{prefix}Fixed springs left over")
            return 0
        # print(f"{prefix}Matched all springs!")
        return 1
    s0 = springs[0]
    rest = springs[1:]
    
    # Look for the next place in line that could hold n springs,
    #  and that's followed by a ., a ?, or the end of the string
    spring_pattern = re.compile(r"[?#]{" + str(s0) + r"}(\.|\?|$)")
        
    # Look to find the first place we can put s0 springs
    m = spring_pattern.search(line)
    if m is None:
        # No matches
        return 0
    start, end = m.span()
    # This isn't a valid match if we had to skip a fixed spring!
    if "#" in line[:start]:
        # print(f"{prefix}Invalid match for {s0} springs at {end=} - Can't skip a # in {line[:start]}")
        return 0
    
    # Try and put 1 spring there
    # print(f"{prefix}Placing {s0} springs at {end=}")
    total = place_springs(line[end:], rest, depth+1)
    # print(f"{prefix}Found {total} arrangements from placing a spring")
    
    # Skip that spot and put this spring in the next position
    if line[start] != "#":
        line_rest = line[start+1:]
        # print(f"{prefix}Trying to place spring again in {line_rest}")
        arrs_rest = place_springs(line_rest, springs, depth)
        # print(f"{prefix}Found {arrs_rest} arrangements from skipping then placing a spring")
        total += arrs_rest
    # else:
        # print(f"{prefix}Can't match rest - Can't skip a # in {line[:start+1]=}")
    
    return total

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip()
    
    lines = data.split("\n")
    part1(lines)
    print("--------")
    part2(lines)
    