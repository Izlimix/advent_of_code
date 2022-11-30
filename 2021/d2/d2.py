#!/usr/bin/env python3

# https://adventofcode.com/2021/day/2

def part1(commands):
    pos, depth = 0, 0
    for (c, n) in commands:
        match c:
            case "forward":
                pos += n
            case "down":
                depth += n
            case "up":
                depth -= n
            case _:
                print(f"Skipping unknown command: {(c, n)}")
    print("Part 1 result:")
    print(pos * depth)

def part2(commands):
    pos, depth, aim = 0, 0, 0
    for (c, n) in commands:
        match c:
            case "forward":
                pos += n
                depth += aim * n
            case "down":
                aim += n
            case "up":
                aim -= n
            case _:
                print(f"Skipping unknown command: {(c, n)}")
    print("Part 2 result:")
    print(pos * depth)

def parse_commands(lines):
    commands = []
    for l in lines:
        # Don't get caught by the trailing newline
        if l:
            (c, n) = l.split(" ")
            n = int(n)
            commands.append((c, n))
    return commands


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    commands = parse_commands(data.split("\n"))
    part2(commands)