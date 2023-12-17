#!/usr/bin/env python3
from tqdm import tqdm

# https://adventofcode.com/2023/day/14

"""
Commit of shame:
I'm not taking out the rotation functions yet, even though they complicated the process and weren't used in the end.
Would be nice to clean this up so each roll is faster (when looping through cells to roll a rock, we can keep the most recently seen blocked tile for that row/col?)
"""

directions = {
    # dir: (offset, sort key)
    "N": (-1j, lambda x: x.imag),
    "W": (-1, lambda x: x.real),
    "S": (1j, lambda x: -x.imag),  # Could use ascending=False, but eh
    "E": (1, lambda x: -x.real)
}

def part1(grid):
    blocks = set()
    rocks = []
    # Find all blocks and rocks
    for (y, row) in enumerate(grid):
        for (x, c) in enumerate(row):
            pos = x + y * 1j
            match c:
                case "#":
                    blocks.add(pos)
                case "O":
                    rocks.append(pos)
    # Roll
    height = len(grid)
    width = len(grid[0])
    new_rocks = roll(blocks, rocks, width, height, "N")

    total = load(height, new_rocks)
    print(f"Part 1: {total=}")
    

def part2(grid, cycles=1_000_000_000):
    # We're going to need to find patterns in the cycles so we don't run all 1_000_000_000 times
    # Prob need to cache?
    # If the end of any NWSE cycle looks like any previous cycle, then skip to that point in the result

    # The grid is hashable if we turn it into a tuple
    # We could either change which direction we slide, or just rotate 90deg anticlockwise, and do 4x cycles?
    blocks = set()
    rocks = []
    # Find all blocks and rocks
    for (y, row) in enumerate(grid):
        for (x, c) in enumerate(row):
            pos = x + y * 1j
            match c:
                case "#":
                    blocks.add(pos)
                case "O":
                    rocks.append(pos)
    # 1 billion spin cycles!
    height = len(grid)
    width = len(grid[0])
    rocks = spin_cycle(blocks, rocks, width, height, cycles)

    height = len(grid)
    total = load(height, rocks)
    print(f"Part 2: {total=}")

def load(height, rocks):
    return sum(height - pos.imag for pos in rocks)

def roll(blocks, rocks, x_max, y_max, d):
    # Roll rocks (NWSE), return new positions of rocks
    # Sort rocks by asc rolling axis
    off, key = directions[d]
    rocks = sorted(rocks, key=key)
    
    new_rocks = set()
    for pos in rocks:
        # print(f"{pos=}")
        # x = pos.real
        # y_settled = pos.imag
        # for y1 in reversed(range(int(pos.imag))):
        #     # Roll until stopped by a block or new rock
        #     #  (old rocks haven't moved yet bc sorted by y)
        #     pos1 = x + y1 * 1j
        #     if (pos1 in blocks) or (pos1 in new_rocks):
        #         break
        #     y_settled = y1
        # new_rocks.add(x + y_settled * 1j)
        settled_pos = pos
        next_pos = pos + off
        obstacles = blocks | new_rocks
        # print(f"{next_pos=}")
        while (next_pos not in obstacles) and (0 <= next_pos.real < x_max) and (0 <= next_pos.imag < y_max):
            settled_pos = next_pos
            next_pos = next_pos + off
            # print(f"{next_pos=}")
        new_rocks.add(settled_pos)
    return new_rocks

def spin_cycle(blocks, rocks, x_max, y_max, cycles):
    # pprint_grid(blocks, rocks)
    rocks = tuple(rocks)  # So it's hashable
    seen_grids = {rocks: 0}

    # block_directions = [set(rot_clockwise(b, d) for b in blocks) for d in range(4)]

    # Keep spinning until we find a loop
    for i in tqdm(range(1, cycles + 1)):
        # roll N, then turn clockwise so W is top (for NWSE)
        # for d in range(4):
        #     rocks = roll(block_directions[d], rocks)
        #     rocks = set(map(rot_clockwise, rocks))
        #     pprint_grid(block_directions[d], rocks)
        for d in directions:
            rocks = roll(blocks, rocks, x_max, y_max, d)
        rocks = tuple(rocks)
        # Have we seen this grid before?
        i0 = seen_grids.get(rocks)
        if i0 is not None:
            loop_length = i - i0
            left = (cycles - i) % loop_length
            if left == 0:
                print(f"Found loop after cycle {i}: {loop_length=}, cycles {left=}, skipping to end!")
                # print(rocks)
                # print(f"{i0=} {i=}")
                # print(f"{seen_grids=}")
                break
        seen_grids[rocks] = i
    
    # Finished all the cycles!
    return rocks


# Hindsight: don't actually need these
# Also they don't change the pos of the rocks and blocks
# def rot(grid):
#     return list(zip(*reversed(grid)))

# def rot_counterclockwise(grid):
#     # would be useful to know numpy here for rot90 :p
#     return list(zip(*grid))[::-1]

def rot_clockwise(x, turns=1):
    # Normally for complex numbers, clockwise would be -1j, but our y is +ve downwards
    return x * pow(1j, turns)

def rot_counterclockwise(x, turns=1):
    return x * pow(-1j, turns)

def pprint_grid(blocks, rocks, n=10):
    print()
    for y in range(n):
        for x in range(n):
            pos = x + y * 1j
            if pos in blocks:
                c = "#"
            elif pos in rocks:
                c = "O"
            else:
                c = "."
            print(c, end="")
        print()


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip()
    
    grid = data.split("\n")
    # part1(grid)
    print("--------")
    part2(grid)
    