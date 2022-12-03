#!/usr/bin/env python3

# https://adventofcode.com/2022/day/3

import string

def part1(rucksacks):
    total = 0
    priorities = dict((letter, priority) for (priority, letter) in enumerate(string.ascii_letters, 1))
    for bag in rucksacks:
        midpt = len(bag) // 2
        c1, c2 = bag[:midpt], bag[midpt:]
        overlap = list(set(c1).intersection(c2))[0]
        total += priorities[overlap]
    print("Part 1 result:")
    print(f"Sum of priorities of items: {total}")
    
    
def part2(rucksacks):
    total = 0
    priorities = dict((letter, priority) for (priority, letter) in enumerate(string.ascii_letters, 1))
    l = len(rucksacks)
    for i in range(0, l, 3):
        bags = rucksacks[i:i+3]
        overlap = list(set(bags[0]).intersection(bags[1], bags[2]))[0]
        total += priorities[overlap]
    print("Part 2 result:")
    print(f"Sum of priorities of each group: {total}")
    

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    rucksacks = data.strip().split()

    part1(rucksacks)
    print("--------")
    part2(rucksacks)
    