#!/usr/bin/env python3
import re

# https://adventofcode.com/2023/day/15

def part1(ls):
    total = 0
    for step in ls:
        v = get_hash(step)
        total += v

    print(f"Part 1: {total=}")

def part2(ls):
    # We can rely on the fact that python dicts keep original insertion order
    # (even on update, but not on delete)
    # Could avoid creating 256 boxes by using a dict, but eh
    boxes = [dict() for _ in range(256)]
    pattern = re.compile(r"(=|-)")
    for step in ls:
        lens, op, focal = pattern.split(step)
        box = boxes[get_hash(lens)]
        match op:
            case "-":
                # Delete lens if present
                box.pop(lens, None)
            case "=":
                box[lens] = int(focal)
    
    # Get total focusing power
    total = 0
    for (b_n, box) in enumerate(boxes, 1):
        for (lens_n, lens) in enumerate(box, 1):
            total += b_n * lens_n * box[lens]
    print(f"Part 2: {total=}")

def get_hash(word):
    v = 0
    for c in word:
        v += ord(c)
        v = (v * 17) % 256
    return v


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip() 
    
    ls = data.split(",")
    part1(ls)
    print("--------")
    part2(ls)
    