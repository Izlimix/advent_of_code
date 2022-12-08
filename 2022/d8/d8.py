#!/usr/bin/env python3

# https://adventofcode.com/2022/day/8

from math import prod

def part1(trees):
    grids = []
    for i in range(4):
        grids.append(visible_trees(trees, i))
    num_visible = sum(1 for x in range(len(trees)) for y in range(len(trees[x])) if any(g[x][y] for g in grids))
    print("Part 1 result:")
    print(f"Total visible trees: {num_visible}")
    
def part2(trees):
    grids = []
    for i in range(4):
        grids.append(view_distance(trees, i))
    scenic_score = max(prod(g[x][y] for g in grids) for x in range(len(trees)) for y in range(len(trees[x])))
    
    print("Part 2 result:")
    print(f"Highest scenic score: {scenic_score}")
    

def visible_trees(trees, orientation=0):
    grid = [[False for _ in line] for line in trees]
    trees = change_orientation(trees, orientation)
    for x in range(len(trees)):
        hi = -1
        for y in range(len(trees[x])):
            t = trees[x][y]
            if t > hi:
                hi = t
                grid[x][y] = True
    result = change_orientation(grid, orientation)
    return result

def view_distance(trees, orientation=0):
    grid = [[0 for _ in line] for line in trees]
    trees = change_orientation(trees, orientation)
    for x in range(len(trees)):
        # Keep track of the closest tree of each height (0-9) that we've seen so far
        closest_trees = [0 for _ in range(10)] 
        for y in range(len(trees[x])):
            t = trees[x][y]
            # This tree's score is the difference in y vs the closest blocking tree we've seen
            closest_y = max(closest_trees[t:])
            grid[x][y] = y - closest_y
            # Now this tree is the closest of height t
            closest_trees[t] = y
    result = change_orientation(grid, orientation)
    return result

def change_orientation(grid, n):
    # We want these operations to be their own involution so we can undo the change on the visiblity grid
    # i.e. f(f(x)) = x
    match n:
        case 0:
            # Looking left-to-right
            pass
        case 1:
            # top-down
            grid = list(zip(*grid))
        case 2:
            # Right-to-left (not really clockwise)
            grid = [line[::-1] for line in grid]
        case 3:
            # Bottom-up
            # flip rows, transpose, then flip again
            # (Its own inverse, since it's a palindrome and each step is its own inverse)
            grid = list(zip(*(grid[::-1])))[::-1]
    return grid

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    lines = data.strip().split("\n")
    trees = [[int(n) for n in l] for l in lines]
    #print(trees)
    print("---- Done parsing ----")

    part1(trees)
    print("--------")
    part2(trees)
    