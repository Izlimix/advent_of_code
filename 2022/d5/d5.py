#!/usr/bin/env python3

# https://adventofcode.com/2022/day/5

import re

def part1(stacks, moves):
    print("Starting stacks:")
    pprint_stacks(stacks)
    for (n, crate_from, crate_to) in moves:
        stacks[crate_to].extend(stacks[crate_from][-n:][::-1]) #[:-n-1:-1])
        stacks[crate_from][-n:] = []
    print("Part 1 result:")
    print(f"Top crate of each stack: {''.join(stack[-1] for stack in stacks[1:])}")
    
def part2(stacks, moves):
    print("Starting stacks:")
    pprint_stacks(stacks)
    for (n, crate_from, crate_to) in moves:
        stacks[crate_to].extend(stacks[crate_from][-n:])
        stacks[crate_from][-n:] = []
    print("Part 2 result:")
    print(f"Top crate of each stack: {''.join(stack[-1] for stack in stacks[1:])}")

def parse_stacks(crate_input):
    crate_input = crate_input.split("\n")[::-1]
    n_stacks = int(crate_input[0].strip()[-1])
    width = n_stacks * 4
    stacks = [None] # Our stacks are 1-indexed, so we'll just leave None in the 0th pos
    
    for i in range(1, width, 4):
        crates = []
        for l in crate_input[1:]:
            c = l.ljust(width, " ")[i]
            if c != " ": crates.append(c)
        stacks.append(crates)
    
    return stacks

def parse_moves(move_input):
    pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")
    for l in move_input.split("\n"):
        m = pattern.match(l)
        if m:
            yield tuple(map(int, m.groups()))

def _copy_stacks(stacks):
    out = []
    for stack in stacks:
        if stack is None:
            out.append(None)
        else:
            out.append([e for e in stack])
    return out

def pprint_stacks(stacks):
    for i in range(len(stacks)):
        print(f"{i}: {stacks[i]}")

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    (crate_input, move_input) = data.split("\n\n")
    stacks = parse_stacks(crate_input)
    moves = list(parse_moves(move_input))
    
    #todo: part1 mutates stacks, so deep-copy for part 2!
    # (note: even if you copy stacks with [:], it only copies the pointers to the inner lists)
    part1(_copy_stacks(stacks), moves)
    print("--------")
    part2(_copy_stacks(stacks), moves)
    