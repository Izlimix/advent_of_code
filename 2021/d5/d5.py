#!/usr/bin/env python3

# https://adventofcode.com/2021/day/5

import re
from collections import defaultdict

def part1(vents):
    overlaps = count_vent_overlaps(vents, False)
    print("Part 1 result:")
    print(f"Number of vent overlaps: {overlaps}")
    
    
def part2(vents):
    overlaps = count_vent_overlaps(vents, True)
    print("Part 2 result:")
    print(f"Number of vent overlaps: {overlaps}")

def count_vent_overlaps(vents, count_diags=False):
    # This really isn't clean or clear, but it works enough for this puzzle.
    vent_lines = defaultdict(int)
    for v in vents:
        (x1, y1, x2, y2) = map(int, v)
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            for y in range(y1, y2 + 1):
                vent_lines[(x1, y)] += 1
        elif y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            for x in range(x1, x2 + 1):
                vent_lines[(x, y1)] += 1
        elif count_diags:
            # 45 degree diagonals~
            if x1 <= x2:
                x_start, y_start = x1, y1
                x_end, y_end = x2, y2
            else:
                x_start, y_start = x2, y2
                x_end, y_end = x1, y1
            for offset in range(0, x_end - x_start + 1):
                x = x_start + offset
                if y_start <= y_end:
                    y = y_start + offset
                else:
                    y = y_start - offset
                vent_lines[(x, y)] += 1

    overlaps = sum(1 for (coord, n) in vent_lines.items() if n >= 2)
    return overlaps

def parse_vents(lines):
    out = []
    pattern = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")
    for l in lines:
        m = pattern.match(l)
        if m:
            out.append(m.groups())
    return out

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    lines = data.strip().split("\n")
    vents = parse_vents(lines)

    part1(vents)
    print("--------")
    part2(vents)
    