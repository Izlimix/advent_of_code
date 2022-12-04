#!/usr/bin/env python3

# https://adventofcode.com/2022/day/4

def part1(lines):
    # Parsing each line as we iterate, since the logic for 3 splits is messy.
    count = 0 # Number of lines where one range fully contains the other.
    for l in lines:
        section1, section2 = parse_sections(l)
        if section1.issuperset(section2) or section2.issuperset(section1):
            count += 1
    
    print("Part 1 result:")
    print(f"Number of pairs where one fully contains the other: {count}")
    
def part2(lines):
    count = 0 # Number of lines where the two ranges overlap.
    for l in lines:
        section1, section2 = parse_sections(l)
        if not section1.isdisjoint(section2):
            count += 1
    
    print("Part 2 result:")
    print(f"Number of pairs that overlap: {count}")
    
def parse_sections(line):
    elf1, elf2 = line.split(",")
    (s1, e1) = map(int, elf1.split("-"))
    (s2, e2) = map(int, elf2.split("-"))
    section1 = set(range(s1, e1 + 1))
    section2 = set(range(s2, e2 + 1))
    return (section1, section2)

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
    