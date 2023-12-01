#!/usr/bin/env python3
import re

# https://adventofcode.com/2023/day/1

"""
Cleaned up a little. 
Thanks to reddit for reminding me about enumerate, and teaching me about:
1. rf strings (you can combine some string modifiers!)
2. re.findall() with a lookahead to match overlapping patterns
"""

def part1(lines):
    vs = [value(row) for row in lines]
    print("Part 1:")
    print("The total calibration value is:")
    print(sum(vs))
    
    
def part2(lines):
    # hahaha this is an awful hack
    patterns = dict(zip(
        ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"],
        (rf"\g<0>{d}\g<0>" for d in range(1, 10))
    ))
    parsed_ls = [replace_patterns(row, patterns) for row in lines]
    vs = [value(row) for row in parsed_ls]
    
    print("Part 2:")
    print("The total calibration value is:")
    print(sum(vs))


def value(row):
    # Filter digits
    digits = set("0123456789")
    ds = [c for c in row if c in digits]
    # Get first and last digit
    return int(ds[0] + ds[-1])

def replace_patterns(s: str, patterns: dict[str, int]):
    for p, repl in patterns.items():
        s = re.sub(p, repl, s)
    return s
    

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    lines = data.strip().split("\n")

    part1(lines)
    print("--------")
    part2(lines)
    