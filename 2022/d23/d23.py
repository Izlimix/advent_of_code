#!/usr/bin/env python3

# https://adventofcode.com/2022/day/23

from collections import Counter

def part1(elves, rounds=10):
    # Run 10 rounds, check number of blank tiles at the end.
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)] # NSWE
    adjacents = set((x, y) for x in (1, 0, -1) for y in (1, 0, -1)) - {(0, 0)}

    for i in range(1, rounds + 1):
        # First half of round: 
        # Each elf checks if there are any adjacent elves, if none, do nothing.
        # Otherwise propose one step in the first valid direction
        # e.g. If looking north, check N, NE and NW are free.
        # If direction_offset varies in x, then we check (+1, 0, -1) of y. If y offset, then we vary x.
        proposals = dict()
        for e in elves:
            (x, y) = e
            # Check for adjacent elves
            if all((x + off_x, y + off_y) not in elves for (off_x, off_y) in adjacents):
                proposals[e] = e
                continue
            
            # Propose a direction
            for (off_x, off_y) in directions:
                next_pos = (x + off_x, y + off_y)
                # If x is 0, check (+1, 0, -1) of y
                if off_x == 0:
                    if all((x + x1, y + off_y) not in elves for x1 in (1, 0, -1)):
                        # The space is free, propose to move there.
                        proposals[e] = next_pos
                        break
                # If y is 0, check (+1, 0, -1) of x
                if off_y == 0:
                    if all((x + off_x, y + y1) not in elves for y1 in (1, 0, -1)):
                        # The space is free, propose to move there.
                        proposals[e] = next_pos
                        break
            else:
                # Tried all directions, propose to stay here.
                proposals[e] = e
        
        # Second half of round: Only elves that proposed a unique spot move.
        overlapping = set(pos for (pos, count) in Counter(proposals.values()).items() if count > 1)
        for (elf, next_pos) in proposals.items():
            if next_pos not in overlapping:
                elves.remove(elf)
                elves.add(next_pos)

        # Finally, the first direction considered is moved to the end of the list.
        directions.append(directions.pop(0))
    
    #pprint_elves(elves)

    print("Part 1 result:")
    print(f"After {rounds} moves, empty ground tiles: {count_blanks(elves)}")

def part2(elves):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)] # NSWE
    adjacents = set((x, y) for x in (1, 0, -1) for y in (1, 0, -1)) - {(0, 0)}
    rounds = 0

    while True:
        rounds += 1
        proposals = dict()
        for e in elves:
            (x, y) = e
            # Check for adjacent elves
            if all((x + off_x, y + off_y) not in elves for (off_x, off_y) in adjacents):
                proposals[e] = e
                continue
            
            # Propose a direction
            for (off_x, off_y) in directions: # TODO: start from a different direction next round
                next_pos = (x + off_x, y + off_y)
                # If x is 0, check (+1, 0, -1) of y
                if off_x == 0:
                    if all((x + x1, y + off_y) not in elves for x1 in (1, 0, -1)):
                        # The space is free, propose to move there.
                        proposals[e] = next_pos
                        break
                # If y is 0, check (+1, 0, -1) of x
                if off_y == 0:
                    if all((x + off_x, y + y1) not in elves for y1 in (1, 0, -1)):
                        # The space is free, propose to move there.
                        proposals[e] = next_pos
                        break
            else:
                # Tried all directions, propose to stay here.
                proposals[e] = e

        # Part 2: Check for the first round where no elf moves
        if all(pos == next_pos for (pos, next_pos) in proposals.items()):
            break

        # Second half of round: Only elves that proposed a unique spot move.
        overlapping = set(pos for (pos, count) in Counter(proposals.values()).items() if count > 1)
        for (elf, next_pos) in proposals.items():
            if next_pos not in overlapping:
                elves.remove(elf)
                elves.add(next_pos)

        # Finally, the first direction considered is moved to the end of the list.
        directions.append(directions.pop(0))
    
    print("Part 2 result:")
    print(f"The first round where no elf moved was round {rounds}")

def count_blanks(elves):
    xs, ys = sorted(x for (x, _) in elves), sorted(y for (_, y) in elves)
    blank = 0
    for y in range(ys[0], ys[-1] + 1):
        for x in range(xs[0], xs[-1] + 1):
            if (x, y) not in elves: blank += 1
    return blank

def pprint_elves(elves, elf_char="#", blank_char="."):
    xs, ys = sorted(x for (x, _) in elves), sorted(y for (_, y) in elves)
    #blank = 0
    print(f"{xs[0]}-{xs[-1]}")
    for y in range(ys[0], ys[-1] + 1):
        for x in range(xs[0], xs[-1] + 1):
            c = elf_char if (x, y) in elves else blank_char
            #if (x, y) not in elves: blank += 1
            print(c, end="")
        print(y)
    #print(f"Empty tiles: {blank}")
    
def parse_elves(lines):
    elves = set()
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "#":
                elves.add((x, y))
    return elves

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    elves = parse_elves(data.strip().split("\n"))
    print("---- Done parsing ----")
    
    part1(elves.copy())
    print("--------")
    part2(elves.copy())
    