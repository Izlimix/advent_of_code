#!/usr/bin/env python3

# https://adventofcode.com/2022/day/1

def part1(elves):
    print("Part 1 result:")
    print("The elf carrying the most calories is carrying:")
    print(max(sum(pack) for pack in elves))
    
    
def part2(elves):
    totals = sorted([sum(pack) for pack in elves], reverse=True)
    print("Part 2 result:")
    print(f"Top three: {totals[:3]}")
    print(f"Total cals by top 3: {sum(totals[:3])}")

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    elves = [[int(n) for n in pack.split()] for pack in data.strip().split("\n\n")]

    part1(elves)
    print("--------")
    part2(elves)
    