#!/usr/bin/env python3

# https://adventofcode.com/2022/day/16
# Idea for caching max_flow and its general shape from some of the solutions on reddit.

import re
from itertools import combinations
from functools import cache
from tqdm import tqdm

def part1(closed_valves, start="AA", minutes=30):
    result = max_flow(closed_valves, start, minutes)
    print(max_flow.cache_info())
    print("Part 1 result:")
    print(f"The most pressure we can release is: {result}")

def part2(closed_valves, start="AA", minutes=26):
    result = 0
    for (v1, v2) in tqdm(all_splits(closed_valves), total = 2 ** len(closed_valves)):
        r1 = max_flow(frozenset(v1), start, minutes)
        r2 = max_flow(frozenset(v2), start, minutes)
        result = max(result, r1 + r2)
    print(max_flow.cache_info())
    print("Part 2 result:")
    print(f"The most pressure we can release with an elephant is: {result}")

# Attempt 1: Brute-force every possible split of closed valves between you and the elephant.
# Attempt 3: Brute-force again, but this time cache the results of max_flow
# There are 15 valves, so 2^15 splits. 
def all_splits(xs):
    xs = set(xs)
    l = len(xs)
    for i in range(1, l):
        for ys in combinations(xs, i):
            ys = set(ys)
            yield (xs.difference(ys), ys)

@cache
def max_flow(closed_valves, current, minutes):
    if minutes <= 0:
        return 0
    flows = [0]
    for v, f in closed_valves:
        # Your attempt at this valve
        d = dist_between(current, v)
        if d is not None and d < minutes:
            mins_remaining = minutes - (d + 1) # it takes 1 more min to open the valve
            flow = mins_remaining * f
            flows.append(flow + max_flow(closed_valves - {(v, f)}, v, mins_remaining))
        
    return max(flows)

def dist_between(start, end, distances=dict()):
    global valves
    # Note: unless distances is provided, this mutates the same initial dict every time
    if not distances:
        # Empty, first run. Init by saying the distance of each valve to itself is 0.
        distances.update(dict.fromkeys(((v, v) for v in valves), 0))
    d1 = distances.get((start, end), None)
    #d2 = distances.get((end, start), None)
    if d1 is not None:
        # We already have the distance between these two
        return d1
    #if d2 is not None:
    #    return d2
    # Explore and add distances between nodes until we find what we want
    depth = 1
    (_, tunnels) = valves[start]
    next_tunnels = set()
    seen = {start}
    while tunnels:
        for t in tunnels:
            if t in seen:
                continue
            distances.setdefault((start, t), depth)
            distances.setdefault((t, start), depth)
            d_to_end = distances.get((t, end), None)
            if d_to_end is not None:
                return depth + d_to_end
            for next_t in valves[t][1]:
                next_tunnels.add(next_t)
        tunnels, next_tunnels = next_tunnels, set()
        depth += 1
    
    print(f"Couldn't find a tunnel from {start} to {end}, searched up to depth {depth}")
    print(distances)
    return None

def find_valves(lines):
    pattern = re.compile("^Valve (.+) has flow rate=(\d+); tunnels? leads? to valves? (.+)$")
    valves = dict()
    for l in lines:
        m = pattern.match(l)
        if m:
            (v_name, flow, tunnels) = m.groups()
            valves[v_name] = (int(flow), tunnels.split(", "))
        else:
            print(f"No match on line: {l}")
    return valves


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    lines = data.strip().split("\n")
    global valves # I don't like this being global, but eh.
    valves = find_valves(lines)
    start = "AA"
    closed_valves = frozenset((valve, flow) for (valve, (flow, _)) in valves.items() if flow > 0) # Only the ones that have a non-zero flow

    print("Parsing done...")
    print("---- Part 1 ----")
    part1(closed_valves)
    print("---- Part 2 ----")
    part2(closed_valves)
    