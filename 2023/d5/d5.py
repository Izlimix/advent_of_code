#!/usr/bin/env python3
import re
from tqdm import tqdm

# https://adventofcode.com/2023/day/5


def part1(data):
    # Note: maps are in (destination_start, source_start, n_elements) order
    # Option 1 is to make a map of each value from 1-n, and replace the elements with those in the maps
    # But the ranges are _very_ big in the input (e.g. 1 billion+ elements), so we'll run out of space and it'll take too long
    # So instead, we can just keep a list of each range and test to see if it's in one of those ranges (check each map in order)
    # Python "x in range" bounds-checking is actually really fast, since range isn't acting as a generator in this case

    # To reduce number of passes, we can sort seeds and sort by source_start and reduce either left or right list at each step

    # Parse sections
    sections = data.split("\n\n")
    # Get seeds and first map
    seeds = re.findall(r"\d+", sections[0])
    values = sorted(int(s) for s in seeds)
    maps = sections[1:]
    # Every mapping has shape: dest_start, source_start, n_elements
    mapping_pattern = re.compile(r"(\d+) (\d+) (\d+)")
    for m in tqdm(maps):
        # Parse the map into lists of [source_start, n_elements, dest_start] for ease of sorting
        maps = sorted([int(v) for v in line.group(2, 3, 1)] for line in mapping_pattern.finditer(m))
        # Parse every value and sort the result for the next map
        values = sorted(use_mapping(maps, values))
    print(f"Part 1: The closest location is {min(values)}")
    
def use_mapping(maps, values):
    # Given a sorted mapping and sorted list of values, yield the mapped values (in no particular order)
    if not maps:
        # print(f"Exhausted maps, yielding from {values}")
        # We've exhausted maps, so everything left in values is returned as-is
        yield from values
        return
    (source, n, dest) = maps[0]
    for i in range(len(values)):
        v = values[i]
        # print(f"Map {maps[0]}, {v=}")
        if v < source:
            # print("Too small, v maps to itself")
            yield v
        elif v < (source + n):
            # This value matches this map
            # print("Match!")
            yield dest + (v - source)
        else:
            # This value is too big for this map, move on to the next one with the remaining iterator values
            # print("No match")
            yield from use_mapping(maps[1:], values[i:]) 
            return


def part2(data):
    # Parse ranges of seed numbers, split them when needed while mapping
    # Parse sections
    sections = data.split("\n\n")
    # Get seeds and first map
    seeds = re.finditer(r"(\d+) (\d+)", sections[0])
    values = sorted([int(v) for v in s.groups()] for s in seeds)
    maps = sections[1:]
    # Every mapping has shape: dest_start, source_start, n_elements
    mapping_pattern = re.compile(r"(\d+) (\d+) (\d+)")
    for m in tqdm(maps):
        # Parse the map into lists of [source_start, n_elements, dest_start] for ease of sorting
        maps = sorted([int(v) for v in line.group(2, 3, 1)] for line in mapping_pattern.finditer(m))
        # Parse every value and sort the result for the next map
        # print(f"{values=} {m=}")
        values = sorted(use_mapping2(maps, values))
        # print(f"Result {values=}")
    print(f"Part 2: The closest location is {min(values)}")

def use_mapping2(maps, values):
    # Given a sorted mapping and sorted list of value ranges, yield the mapped value ranges (in no particular order)
    if not maps:
        # print(f"Exhausted maps, yielding from {values}")
        # We've exhausted maps, so everything left in values is returned as-is
        yield from values
        return
    (source, n, dest) = maps[0]
    for i in range(len(values)):
        (v, v_n) = values[i]
        # print(f"Map {maps[0]}, {v=} {v_n=}")
        if v < source:
            # print("Too small for mapping")
            if (v + v_n) < source:
                # print("All of v maps to itself")
                yield (v, v_n)
            else:
                l_over = source - v
                # print(f"Splitting into 2 ranges, {l_over=}")
                yield (v, v_n - l_over)
                yield from use_mapping2(maps, [(source, l_over)] + values[i+1:])
                return

        elif v < (source + n):
            # print("Match!")
            dest_v = dest + (v - source)
            v_end = v + v_n
            source_end = source + n
            if v_end < source_end:
                # print("All of v gets mapped")
                yield (dest_v, v_n)
            else:
                l_over = v_end - source_end
                # print(f"Splitting into 2 ranges, first range mapped to {(dest_v, v_n - l_over)}, {l_over=}")
                yield (dest_v, v_n - l_over)
                yield from use_mapping2(maps[1:], [(source_end, l_over)] + values[i+1:])
                return
        else:
            # This value is too big for this map, move on to the next one with the remaining iterator values
            # print("No match")
            yield from use_mapping2(maps[1:], values[i:]) 
            return


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip()
    
    # lines = data.strip().split("\n")

    part1(data)
    print("--------")
    part2(data)
    