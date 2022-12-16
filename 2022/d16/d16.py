#!/usr/bin/env python3

# https://adventofcode.com/2022/day/16
# Idea for caching max_flow and its general shape from some of the solutions on reddit.
# After profiling, it turns out dist_between was very inefficient, so it's been replaced by Floyd-Warshall (used in many of the reddit answers)

import re
from collections import defaultdict
import itertools
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
# (It's symmetrical, so we could halve this space by not doing both (xs, ys) and (ys, xs), but the result's cached anyway)
def all_splits(xs):
    xs = set(xs)
    l = len(xs)
    for i in range(1, l):
        for ys in itertools.combinations(xs, i):
            ys = set(ys)
            yield (xs.difference(ys), ys)

@cache
def max_flow(closed_valves, current, minutes):
    if minutes <= 0:
        return 0
    max_f = 0
    for v, f in closed_valves:
        # Your attempt at this valve
        d = dist_between(current, v)
        if d is not None and d < minutes:
            mins_remaining = minutes - (d + 1) # it takes 1 more min to open the valve
            flow = mins_remaining * f
            max_f = max(max_f, flow + max_flow(closed_valves - {(v, f)}, v, mins_remaining))
        
    return max_f

# Now uses Floyd-Warshall! Much faster
# This would be even faster with fewer function calls and global lookups, but I'm happy with this
def dist_between(start, end):
    global distances
    return distances[(start, end)]

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
    
    # Floyd-Warshall to find the shortest distance between all our valves
    global distances
    distances = defaultdict(lambda: 100_000)
    for (v, (_, tunnels)) in valves.items():
        distances[(v, v)] = 0 # The distance to yourself is 0
        for t in tunnels:
            distances[(v, t)] = 1 # Initial edges
            distances[(t, v)] = 1
    for (k, i, j) in itertools.product(valves, valves, valves):
        # Note: k ranges slowest, so all the pairs have a chance to go first
        distances[(i, j)] = min(distances[(i, j)], distances[(i, k)] + distances[(k, j)])

    print("Parsing done...")
    print("---- Part 1 ----")
    part1(closed_valves)
    print("---- Part 2 ----")
    part2(closed_valves)
    