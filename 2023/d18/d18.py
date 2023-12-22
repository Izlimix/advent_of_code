#!/usr/bin/env python3

import re

# https://adventofcode.com/2023/day/18

"""
No original approach here, had to check reddit for how to even approach part2's size.
"""

def part1(lines):
    # First, draw out the loop cells
    # Then, mark every tile as inside or outside
    # -> do this using the "internal count" from d10 (shoot a beam, count "vert pipes", and when you find an empty cell fill it if you've crossed an odd num of pipes)
    # Alternatively: Add 1 tile to the edge of the shape, flood-fill outside from a corner, then take the difference as internal
    # (note: if there's a trapped corner bit of the outside, then that won't work.)
    # Rather than counting pipes for every cell, we could just fire beams to look for the first internal cell, then flood-fill internal from there
    pos = 0j
    trench = set()
    trench.add(pos)
    for line in lines:
        # Ignoring colour for part 1
        direction, steps, colour = line.split(" ")
        match direction:
            case "U":
                off = -1j
            case "D":
                off = 1j
            case "L":
                off = -1
            case "R":
                off = 1
        for _ in range(int(steps)):
            pos += off
            trench.add(pos)
    print(f"Done digging trench, finished at {pos=}. {len(trench)=}")
    # pprint(trench, 1)

    # Fill interior of lagoon (Based off of d10 line-scanning for now)
    lagoon = set()

    xs = [int(p.real) for p in trench]
    ys = [int(p.imag) for p in trench]
    x_lo, x_hi = min(xs), max(xs)
    y_lo, y_hi = min(ys), max(ys)
    for y in range(y_lo, y_hi + 1):
        walls_crossed = 0
        # Note: this can't handle if the shape has two opposite trenches that meet
        # in_wall = False
        wall_start_direction = None
        for x in range(x_lo, x_hi + 1):
            pos = x + y * 1j
            if pos in trench:
                lagoon.add(pos)
                if wall_start_direction is None:
                    walls_crossed += 1
                    # in_wall = True
                    if (pos - 1j) in trench:
                        if (pos + 1j) in trench:
                            # Simple vert piece |, not a long wall
                            # in_wall = False
                            pass
                        else:
                            # L piece, entered from north
                            wall_start_direction = -1j
                    else:
                        # F piece, entered from south
                        wall_start_direction = 1j 
            else:
                # Ground tile
                # If we were in a wall previously, the wall's ended now
                if wall_start_direction is not None:
                    # in_wall = False
                    # It only counts as a wall crossed if the enter and exit direction don't match
                    if (pos - 1 + wall_start_direction) in trench:
                        # End dir matches start, it cancels out
                        walls_crossed += 1
                    wall_start_direction = None
                if walls_crossed % 2:
                    # Odd number of crossings, we're inside
                    lagoon.add(pos)
    # pprint(lagoon, 2)
    print(f"Part 1: Total volume = {len(lagoon)}")

def part1a(lines):
    # Rewrite of part 1 using 
    dir_offsets = {
        "R": 1,  # R
        "D": 1j,  # D
        "L": -1,  # L
        "U": -1j  # U
    }
    pos = 0j
    trench = [pos]
    perimeter = 0
    # pattern = re.compile(r"#([\dA-Fa-f]{5})([\dA-Fa-f])")
    for line in lines:
        direction, steps, _ = line.split(" ")
        off = dir_offsets[direction]
        # print(f"{line=} {steps=} {off=}")

        pos = pos + off * int(steps)
        perimeter += int(steps)
        trench.append(pos)
    print(f"Done digging trench, finished at {pos=}. {len(trench)=}, {perimeter=}")
    # print(f"{trench=}")
    # print(f"{shoelace(trench)=}")
    result = shoelace(trench) + 1 + (perimeter // 2)

    print(f"Part 1a: {result=}")

def part2(lines):
    # Yeah... with these dimensions we won't be able to bruteforce it
    # Get the vertex-coords of each end
    # Maths explanation of Pick's theorem + shoelace formula taken from reddit (this day has fully evaded me otherwise):
    #  https://www.reddit.com/r/adventofcode/comments/18l0qtr/comment/kdveugr/
    dir_offsets = {
        "0": 1,  # R
        "1": 1j,  # D
        "2": -1,  # L
        "3": -1j  # U
    }
    pos = 0j
    trench = [pos]
    perimeter = 0
    pattern = re.compile(r"#([\dA-Fa-f]{5})([\dA-Fa-f])")
    for line in lines:
        m = pattern.search(line)
        steps = int(m.group(1), 16)
        off = dir_offsets[m.group(2)]

        perimeter += steps
        pos = pos + off * steps
        trench.append(pos)
    print(f"Done digging trench, finished at {pos=}. {len(trench)=}, {perimeter=}")
    result = shoelace(trench) + 1 + (perimeter // 2)

    print(f"Part 2: {result=}")


def shoelace(vertices):
    # https://en.wikipedia.org/wiki/Shoelace_formula
    area = 0
    for (p1, p2) in zip(vertices, vertices[1:]):
        area += (p1.imag + p2.imag) * (p1.real - p2.real)

    return area // 2

def pprint(cells, n = 1):
    xs = [int(p.real) for p in cells]
    ys = [int(p.imag) for p in cells]
    x_lo, x_hi = min(xs), max(xs)
    y_lo, y_hi = min(ys), max(ys)
    out_lines = []
    for y in range(y_lo, y_hi + 1):
        out_row = []
        for x in range(x_lo, x_hi + 1):
            out_row.append("#" if (x + y * 1j) in cells else ".")
        out_lines.append("".join(out_row))
    out = "\n".join(out_lines)
    print(out)
    # with open(f"input_grid_{n}.txt", "w") as f:
    #     f.write(out)


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip() 
    
    lines = data.split("\n")
    # part1(lines)
    part1a(lines)
    print("--------")
    part2(lines)
    