#!/usr/bin/env python3

# https://adventofcode.com/2021/day/1

def part1(depths):
    # Given a file, parse into a list of lines of depths
    # Count depths (after the 0th) higher than the one immediately before
    print("Part 1 result:")
    print(num_increases(depths))

def part2(depths):
    window_sums = [sum(w) for w in sliding_window(depths, 3)]
    print("Part 2 result:")
    print(num_increases(window_sums))

def num_increases(depths):
    return sum(1 for (a, b) in zip(depths, depths[1:]) if b > a)

def sliding_window(data, size=2):
    iterables = [data[i:] for i in range(size)]
    return zip(*iterables)

# Command-line execution:
if __name__ == "__main__":
    import sys
    # Run like:
    # python d1.py input.txt
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    depths = [int(d) for d in data.split()]
    part2(depths)