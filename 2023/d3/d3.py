#!/usr/bin/env python3
import re
import math


# https://adventofcode.com/2023/day/3
"""
Initial attempt+approach (cleaned up so part 1 and part 2 use the same map of parts)

"""

def main(lines):
    # Let's make a grid of Numbers and Symbols.
    # y-down, x-right, with the first symbol being (0, 0)
    # We could use imaginary numbers for this, coords = x + yj
    digit_pattern = re.compile(r"\d+")
    symbol_pattern = re.compile(r"[^.\d]")  # Not digit or literal .
    grid = dict()
    all_parts = []
    all_symbols = []
    all_gears = []  # For part 2

    # Find all the Numbers and Symbols
    for (y, l) in enumerate(lines):
        # Find all the Symbols
        symbols = symbol_pattern.finditer(l)
        for m in symbols:
            pos = m.start() + y * 1j
            all_symbols.append(pos)
            if m.group(0) == "*":
                all_gears.append(pos)

        # Find all the Numbers
        numbers = digit_pattern.finditer(l)
        for m in numbers:
            num = Number(int(m.group(0)))
            all_parts.append(num)
            for x in range(*m.span()):
                grid[x + y * 1j] = num
    
    # Mark any number adjacent to a symbol as valid
    valid_cells = set(c for s in all_symbols for c in adjacent_cells(s))
    for c in valid_cells:
        part = grid.get(c, None)
        if part is not None:
            part.valid = True
    
    print(f"Part 1: The sum of valid part numbers is:")
    print(sum(p.value for p in all_parts if p.valid))
    print("--------")

    # Part 2: A gear is valid only if next to 2 valid parts
    gear_total = 0
    for g in all_gears:
        # Get unique (based on obj id) parts adjacent to the gear
        parts = set()
        for pos in adjacent_cells(g):
            part = grid.get(pos, None)
            if part is not None and part.valid:
                parts.add(part)
        
        if len(parts) == 2:
            gear_ratio = math.prod(p.value for p in parts)
            gear_total += gear_ratio

    print(f"Part 2: Sum of gear ratios = {gear_total}")
    

class Number:
    def __init__(self, value) -> None:
        self.value = value
        self.valid = False

def adjacent_cells(pos):
    return [pos + x + y * 1j for y in [-1, 0, 1] for x in [-1, 0, 1]]


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    lines = data.strip().split("\n")

    main(lines)
    