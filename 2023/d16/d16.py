#!/usr/bin/env python3

from collections import deque

# https://adventofcode.com/2023/day/16

offs = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0)
}

def part1(grid):
    result = shoot_beam(grid, (0, 0, "E"))
    print(f"Part 1: {result}")


def part2(grid):
    result = 0
    # Shoot beam along every edge, get the max (brute force!)
    height = len(grid)
    width = len(grid[0])
    # W edge going E
    result = max(result, *[shoot_beam(grid, (0, y, "E")) for y in range(height)])
    # N edge going S
    result = max(result, *[shoot_beam(grid, (x, 0, "S")) for x in range(width)])
    # E edge going W
    result = max(result, *[shoot_beam(grid, (width - 1, y, "W")) for y in range(height)])
    # S edge going N
    result = max(result, *[shoot_beam(grid, (x, height - 1, "N")) for x in range(width)])
    
    print(f"Part 2: {result}")

def shoot_beam(grid, start_beam):
    height = len(grid)
    width = len(grid[0])
    # Store pos as (x, y) and store NESW direction of beam
    # Keep a set of next and seen beam positions (incl dir), 
    #  don't repeat seen (to avoid infinite loops)
    seen = set()
    energised = set()  # Could just do a 2nd pass over set
    beams = deque([start_beam])
    while beams:
        bx, by, bd = beams.pop()
        if (bx, by, bd) in seen:
            continue
        # Make sure we don't go off the grid
        if not ((0 <= bx < width) and (0 <= by < height)):
            continue
        seen.add((bx, by, bd))
        energised.add((bx, by))
        c = grid[by][bx]
        match (c, bd):
            case (".", _) | ("|", "N") | ("|", "S") | ("-", "E") | ("-", "W"):
                # Keep going in the same direction
                beams.append(split_beam(bx, by, bd))
            case ("|", _):
                # split NS
                beams.append(split_beam(bx, by, "N"))
                beams.append(split_beam(bx, by, "S"))
            case ("-", _):
                # split EW
                beams.append(split_beam(bx, by, "E"))
                beams.append(split_beam(bx, by, "W"))
            case ("/", "E") | ("\\", "W"):
                beams.append(split_beam(bx, by, "N"))
            case ("/", "W") | ("\\", "E"):
                beams.append(split_beam(bx, by, "S"))
            case ("/", "N") | ("\\", "S"):
                beams.append(split_beam(bx, by, "E"))
            case ("/", "S") | ("\\", "N"):
                beams.append(split_beam(bx, by, "W"))
            case _:
                raise Exception(f"Missing case for {(c, bd)=} at pos {(bx, by)}")
    
    return len(energised)

def split_beam(x0, y0, d):
    offx, offy = offs[d]
    return x0 + offx, y0+offy, d


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip() 
    
    grid = data.split("\n")
    part1(grid)
    print("--------")
    part2(grid)
    