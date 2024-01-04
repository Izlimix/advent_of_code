#!/usr/bin/env python3
from tqdm import tqdm

# https://adventofcode.com/2023/day/21

"""
Would be good to revisit this one, as I don't have a good solution for part 2.
"""

def part1(grid: list[str], steps: int = 64):
    # If we have an even number of steps left, we waste 2 steps at a time to get back to the same cell
    # Since we can only move in cardinal directions, cells cannot be both odd and even (regardless of path!)
    walkable = set()
    for (y, row) in enumerate(grid):
        for (x, c) in enumerate(row):
            pos = x + y * 1j
            match c:
                case "S":
                    start = pos
                    walkable.add(pos)
                case ".":
                    walkable.add(pos)
    result = set()
    seen = set()
    frontier = set([start])
    for i in tqdm(range(steps + 1)):
        steps_left = steps - i
        # print(f"{i=}, {steps_left=}")
        next_steps = set()
        for p in frontier:
            seen.add(p)
            if (steps_left % 2) == 0:
                result.add(p)
            next_steps.update(n for n in neighbours(p) if n in walkable)
        # New frontier = neighbours - seen
        frontier = next_steps.difference(seen)

    pprint(walkable, result)
    
    print(f"Part 1: {len(result)=}")

def part2(grid: list[str], steps: int = 64):
    # Infinite map and much larger n_steps, brute-force isn't an option
    # Options (prob equivalent): 1. some sort of cycle detection
    # 2. maths?? -> Could mark the min_steps to reach any tile, and note the width/height of grid (if odd, then flip odd/even every copy?)
    # -> map is 131 x 131
    # 
    
    orig_height = len(grid)

    walkable = set()
    for (y, row) in enumerate(grid):
        for (x, c) in enumerate(row):
            pos = x + y * 1j
            match c:
                case "S":
                    start = pos
                    walkable.add(pos)
                case ".":
                    walkable.add(pos)
    echo_offset = start.real
    
    # Get bounds of original grid. If pos lies outside the original bounds, can correct the "walkable" check for the corrseponding original tile
    result = set()
    seen = set()
    frontier = set([start])
    cycle_vs = []
    for i in range(steps + 1):
        steps_left = steps - i
        next_steps = set()
        for p in frontier:
            seen.add(p)
            if (steps_left % 2) == 0:
                result.add(p)
            next_steps.update(n for n in neighbours(p) if matching_cell(orig_height, n) in walkable)
        # New frontier = neighbours - seen
        frontier = next_steps.difference(seen)
        if ((steps_left % 2) == 0) and ((i - echo_offset) % orig_height == 0):
            # For some reason I can't figure out, on odd-parity steps left (step 196, etc), the result is incorrect
            # So instead keep only even-parity cycles (0, 2, 4) of 131 steps, and halve the number of cycles (n) in the function
            print(f"Step {i}: {len(result)=}, {steps_left=}, parity {(steps_left % 2) == 0=}")
            cycle_vs.append(len(result))
            if len(cycle_vs) > 5:
                print(f"Plug sequence {cycle_vs} into wolfram alpha to predict the final term")
                # 2 (16204 - 43329 n + 28966 n^2), n = 202300 / 2 + 1 => 592723929260582
                break

    pprint2(walkable, result, orig_height, name="input_pprint.txt")
    print(f"Part 2: {len(result)=}")

def neighbours(pos):
    return [pos + off for off in [1, -1, 1j, -1j]]

def make_copies(grid: list[str], n: int):
    n = n + 1
    out = [line * n for line in grid] * n
    # Makes multiple start points, but ok as long as we pprint with the right "reachable"?
    # print(out)
    return out

def matching_cell(height: int, pos: complex):
    # Also works with negative numbers!
    return complex(pos.real % height, pos.imag % height)

def pprint(walkable: set[complex], reachable: set[complex], *, name: str = None):
    xs = {int(v.real) for v in walkable}
    ys = {int(v.imag) for v in walkable}
    x_lo, x_hi = min(xs), max(xs)
    y_lo, y_hi = min(ys), max(ys)
    out_lines = []
    for y in range(y_lo, y_hi + 1):
        out_row = []
        for x in range(x_lo, x_hi + 1):
            pos = x + y * 1j
            if pos in reachable:
                c = "O"
            elif pos in walkable:
                c = "."
            else:
                c = "#"
            out_row.append(c)
        out_lines.append("".join(out_row))
    out = "\n".join(out_lines)
    # print(out)
    if name is None:
        name = "input_pprint.txt"
    with open(name, "w") as f:
        f.write(out)


def pprint2(walkable: set[complex], reachable: set[complex], h, *, name: str = None):
    xs = {int(v.real) for v in walkable | reachable}
    ys = {int(v.imag) for v in walkable | reachable}
    x_lo, x_hi = min(xs), max(xs)
    y_lo, y_hi = min(ys), max(ys)
    out_lines = []
    for y in range(y_lo, y_hi + 1):
        out_row = []
        for x in range(x_lo, x_hi + 1):
            pos = x + y * 1j
            if pos in reachable:
                c = "O"
            elif matching_cell(h, pos) in walkable:
                c = "."
            else:
                c = "#"
            out_row.append(c)
        out_lines.append("".join(out_row))
    out = "\n".join(out_lines)
    # print(out)
    if name is None:
        name = "input_pprint.txt"
    # with open(name, "w") as f:
    #     f.write(out)


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip() 
    grid = data.split("\n")
    
    part1(grid, 65)
    print("--------")
    # part2(grid, 65 + 131 * 202300)
    part2(grid, 26501365)
    