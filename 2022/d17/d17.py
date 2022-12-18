#!/usr/bin/env python3

# https://adventofcode.com/2022/day/17

import itertools
from tqdm import tqdm

# Currently very messy, but it works. The falling rocks cycle-detection can be cleaned up a lot.

def part1(jets, rocks, rounds=2022):
    current_highest = falling_rocks(jets, rocks, rounds)
    print("Part 1 result:")
    print(f"After {rounds} rounds, the tower is {current_highest} units tall")
    
def part2(jets, rocks):
    elephant_rounds = 1_000_000_000_000 # One trillion? Really?
    rounds = elephant_rounds
    # If any line fills up, we can forget everything below it, store our current highest, then reset the origin?
    # ^ But full lines are actually quite unlikely
    # Look for a cycle, then repeat the height of it?
    current_highest = falling_rocks(jets, rocks, rounds)
    print("Part 2 result:")
    print(f"After {rounds} rounds, the tower is {current_highest} units tall")

def falling_rocks(jets, rocks, rounds, check_cycles=True):
    # TODO: Learn about numpy array slicing, and sparse Bool arrays?
    chamber = set()
    current_highest = 0
    # The bottom-left corner of the chamber is (0, 0). 7 units wide, so bottom-right is (0, 6)
    # Blocks start falling with their bottom-left aligned to (2, 3 + highest)
    # Cycle of enumerated jets and rocks? Then if the two match up again at the same x-position, it might be a cycle?
    # But if a block falls below the start-height of the cycle, is it safe?
    jet_cycle = itertools.cycle(enumerate(jets))
    rock_cycle = itertools.cycle(enumerate(rocks))
    rock_info = dict()

    for round in tqdm(range(1, rounds + 1)):
        r_i, r = next(rock_cycle)
        r_h, r_w = r.height, r.width

        falling = True
        fall_origin = (2, current_highest + 3) # Merge this and the next line~
        pos = fall_origin

        while falling:
            # Try to push the rock in the direction of jet
            j_i, jet = next(jet_cycle)
            jet_offset = 1 if jet == ">" else -1
            pushed_pos = (pos[0] + jet_offset, pos[1])
            # Check for wall collision
            if pushed_pos[0] >= 0 and pushed_pos[0] + r_w <= 7:
                blocked_chamber_cells = [(x, y) for x in range(pushed_pos[0], pushed_pos[0] + r_w)
                                                for y in range(pushed_pos[1], pushed_pos[1] + r_h)
                                                if (x, y) in chamber]
                rock_cells = list(r.occupied_cells(pushed_pos))
                if not collides(blocked_chamber_cells, rock_cells):
                    pos = pushed_pos
            
            # Fall one unit
            # If the fall is blocked, this rock settles
            fall_pos = (pos[0], pos[1] - 1)
            if fall_pos[1] < 0:
                # Hit the floor
                falling = False
                break
            blocked_chamber_cells = [(x, y) for x in range(fall_pos[0], fall_pos[0] + r_w)
                                            for y in range(fall_pos[1], fall_pos[1] + r_h)
                                            if (x, y) in chamber]
            rock_cells = list(r.occupied_cells(fall_pos))
            if collides(blocked_chamber_cells, rock_cells):
                falling = False
                break
            pos = fall_pos
        
        # Come to rest
        chamber.update(r.occupied_cells(pos))
        current_highest = max(current_highest, pos[1] + r.height)

        # Check for a cycle based on where this rock settled
        # r_i: rock type
        # j_i: which jet instruction
        # (x, -y- this should be the current highest) of settle-pos
        # ^ (we need to check whether the y-coord of where this settled is the current highest.
        #     If it isn't, we can just wait until the part of the cycle where it does)
        # round: which round we found it
        if check_cycles:
            if current_highest == pos[1] + r.height:
                possible_prev = rock_info.get((r_i, j_i, pos[0]), None)
                if possible_prev is not None:
                    #print("----")
                    # Probably a cycle!
                    (prev_y, prev_round) = possible_prev
                    #print(f"Found cycle from {prev_round} to {round}")
                    
                    round_diff = round - prev_round
                    height_diff = current_highest - prev_y # Why -was- there an off-1 error here? using pos[1] for the y of the _origin_ and not the current highest.
                    cycles = (rounds - round) // round_diff

                    if rounds - (round + cycles * round_diff) != 0:
                        #print("But let's be careful, this might not be a cycle. wait until it's a whole number...")
                        #print("----")
                        # Store info to look for a cycle next time 
                        rock_info[r_i, j_i, pos[0]] = (current_highest, round)
                        continue

                    current_highest += cycles * height_diff
                    remaining_rounds = rounds - (round + cycles * round_diff)
                    h_diff_remaining = [y for (y, round) in rock_info.values() if round == prev_round + remaining_rounds][0] - prev_y # haha this is so terrible
                    
                    # It's not a real cycle >.<
                    # If we only jump when there's a whole number of cycles remaining, then it might work?
                    # (Yeah, by luck. It gives it time to settle into a cycle.)
                    # (Better would be to remember fingerprint of top-view of blocks, or the prev ~20-50 height deltas)
                    """
                    print("----")
                    _show_chamber(chamber, 1747, 1770)
                    print("----")
                    _show_chamber(chamber, 7, 30)
                    """    
                    return current_highest + h_diff_remaining

            # Store info to look for a cycle next time 
            rock_info[r_i, j_i, pos[0]] = (current_highest, round)

        # Forget collision info of cells < 5k below current
        if round % 20000 == 0:
            chamber = {(x, y) for (x, y) in chamber if current_highest - y < 5000}

        #print("----")
    return current_highest

def collides(grid1, grid2):
    # Given two grids of the same shape,
    # group elements of both grids. If any pair are both True, then they collide
    # Atm this operates on two sets of occupied coords?
    return not set(grid1).isdisjoint(grid2)

class Rock:
    def __init__(self, shape):
        lines = shape.split("\n")
        self.height = len(lines)
        self.width = len(lines[0])
        self.shape = [[c == "#" for c in l] for l in lines] # Should give a 2d-array of Bools

    def pprint(self, rock_char="#", air_char="."):
        for row in self.shape:
            for cell in row:
                print(rock_char if cell else air_char, end="")
            print("")
    
    def occupied_cells(self, origin=(0, 0)):
        for y in range(self.height):
            # this y ranges (0-h), down from the top...
            for x in range(self.width):
                if self.shape[::-1][y][x]: # So we reverse the order of rows here for use with part1
                    yield (origin[0] + x, origin[1] + y)

def _show_chamber(chamber, lo=None, hi = None):
    if lo is None or hi is None:
        lo = min(p[1] for p in chamber)
        hi = max(p[1] for p in chamber)
    for y in reversed(range(lo, hi + 1)):
        for x in range(7):
            print("#" if (x, y) in chamber else ".", end="")
        print(y, end="")
        print("")


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()    
    jets = data.strip()

    # Rock shapes
    with open("shapes.txt", encoding="utf-8") as f:
        rock_data = f.read()    
    shapes = rock_data.split("\n\n")
    rocks = [Rock(shape) for shape in shapes]
    
    part1(jets, rocks)
    print("--------")
    part2(jets, rocks)
    