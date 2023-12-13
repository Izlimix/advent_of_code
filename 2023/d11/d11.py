#!/usr/bin/env python3
from itertools import combinations
from tqdm import tqdm

# https://adventofcode.com/2023/day/10


def part1(data):
    grid = data.split("\n")
    # Expand both rows and cols
    grid = transpose(expand_blank_rows(grid))
    grid = transpose(expand_blank_rows(grid))

    # May be good to do a line-sweep algorithm here to calculate all pairs of distances
    # Find all galaxies
    galaxies = []
    for (y, row) in enumerate(grid):
        for (x, c) in enumerate(row):
            if c == "#":
                pos = x + y * 1j
                galaxies.append(pos)
    dists = []
    for (p1, p2) in tqdm(combinations(galaxies, 2)):
        d = taxicab_dist(p1, p2)
        dists.append(d)
    print(f"Part 1: {sum(dists)=}")
    

def part2(data, expansion):
    # The empty rows and cols are 1m times larger!
    # This time, keep track of the indexes of empty rows and cols
    # When getting the dist between two, add 1m * the number of empty rows and cols in between!
    empty_rows = []
    empty_cols = []
    grid = data.split("\n")

    # Find all blank cols
    for (x, col) in enumerate(transpose(grid)):
        if all(c == "." for c in col):
            empty_cols.append(x)
    # Find all galaxies and blank rows
    galaxies = []
    for (y, row) in enumerate(grid):
        for (x, c) in enumerate(row):
            if c == "#":
                pos = x + y * 1j
                galaxies.append(pos)
        if all(c == "." for c in row):
            empty_rows.append(y)
    print(f"{empty_rows=} {empty_cols=}")

    dists = []
    for (p1, p2) in tqdm(combinations(galaxies, 2)):
        d = taxicab_dist(p1, p2)
        # find overlapping blank cols
        x1, x2 = sorted(map(int, (p1.real, p2.real)))
        cols_covered = range(x1, x2)
        extra_cols = sum(1 for x in empty_cols if x in cols_covered)
        # find overlapping blank rows
        y1, y2 = sorted(map(int, (p1.imag, p2.imag)))
        rows_covered = range(y1, y2)
        extra_rows = sum(1 for y in empty_rows if y in rows_covered)

        # We already counted 1 of the expanded rows, so add another n-1
        d += (expansion - 1) * (extra_cols + extra_rows)
        dists.append(d)
    print(f"Part 2: {sum(dists)=}")


def taxicab_dist(p1, p2):
    d = p1 - p2
    return abs(d.real) + abs(d.imag)

def expand_blank_rows(grid):
    # Warning: may need to make sure rows are non-mutable (e.g. string) and that we aren't mutating in-place
    out = []
    for row in grid:
        out.append(row)
        if all(c == "." for c in row):
            out.append(row)
    return out

def transpose(grid):
    return list(zip(*grid))


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip()
    
    part1(data)
    print("--------")
    part2(data, expansion=1_000_000)
    