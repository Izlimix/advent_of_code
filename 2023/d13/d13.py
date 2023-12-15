#!/usr/bin/env python3

# https://adventofcode.com/2023/day/13


def part1(grids):
    total = 0
    for grid in grids:
        # Search vertically for a match
        r = find_mirror(grid)
        if r is not None:
            total += r * 100
            continue
        # Search horizontally for a match
        r = find_mirror(transpose(grid))
        if r is not None:
            total += r
            continue
        print(f"Couldn't find a mirror for {grid=}")
        
    print(f"Part 1: {total=}")
    

def part2(grids):
    total = 0
    for grid in grids:
        # Search vertically for a smudged match
        r = find_smudged_mirror(grid)
        if r is not None:
            total += r * 100
            continue
        # Search horizontally for a smudged match
        r = find_smudged_mirror(transpose(grid))
        if r is not None:
            total += r
            continue
        print(f"Couldn't find a smudged mirror for {grid=}")
    print(f"Part 2: {total=}")

def find_mirror(grid):
    n_cols = len(grid)
    for i in range(1, n_cols + 1):
        r = is_reflection(grid, i)
        if r:
            return i
    return None

def is_reflection(grid, y):
    before = grid[y-1::-1] # So when input y = 1, there's 1 row in the before-slice
    after = grid[y:]
    return before and after and all(r1 == r2 for (r1, r2) in zip(before, after))

def find_smudged_mirror(grid):
    n_cols = len(grid)
    for i in range(1, n_cols + 1):
        r = is_smudged(grid, i)
        if r:
            return i
    return None

def is_smudged(grid, y):
    before = grid[y-1::-1]
    after = grid[y:]
    # If the number of differences is exactly 1, then True
    differences = sum(c1 != c2 for (r1, r2) in zip(before, after) for (c1, c2) in zip(r1, r2))
    return differences == 1

def transpose(grid):
    return list(zip(*grid))


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip()
    
    grids = [line.split("\n") for line in data.split("\n\n")]
    part1(grids)
    print("--------")
    part2(grids)
    