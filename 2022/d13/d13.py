#!/usr/bin/env python3

# https://adventofcode.com/2022/day/13

import json
from functools import cmp_to_key

def part1(packets):
    score = 0
    for i in range(len(packets)):
        result = compare_packets(*packets[i])
        if result is None:
            print("This pair of packets didn't short-circuit. Don't know if they're in the right order:")
            print(packets[i])
            continue
        if result:
            score += i + 1
    print("Part 1 result:")
    print(f"Sum of indices of pairs in the right order: {score}")

def part2(packet_pairs):
    # We need all packets back in the same list, plus two divider packets
    dividers = [[[2]], [[6]]]
    packets = list(dividers)
    for ps in packet_pairs:
        packets.extend(ps)
    packets.sort(key=cmp_to_key(cmp_packets))
    
    divider_positions = [i for (i, p) in enumerate(packets, 1) if p in dividers]
    print("Part 2 result:")
    print(f"Positions: {divider_positions}")
    print(f"Decoder key: {divider_positions[0] * divider_positions[1]}")
    
def compare_packets_original(left, right):
    # Note: "right order" and "wrong order" should both short-circuit the result!
    # So we'll use True and False for "right order" and "wrong order", and None for "keep checking"
    if isinstance(left, int) and isinstance(right, int):
        # If both values are integers, the lower integer should come first
        # If they're equal, keep checking
        if left == right: return None
        return left <= right
    elif isinstance(left, list) and isinstance(right, list):
        # If both are lists, compare elements pairwise
        for (l1, r1) in zip(left, right):
            r = compare_packets(l1, r1)
            if r is not None:
                # One of the inner-comparisons short-circuited!
                return r
        # One of the lists ran out of items
        ll, lr = len(left), len(right)
        # If the left list runs out of items first, they're in the right order.
        # If the right side runs out first: wrong order.
        # If they're the same length, keep comparing.
        if ll == lr:
            return None
        else:
            return ll < lr
    else:
        # If only one is an int, convert it into a singleton list and try again
        if isinstance(left, int):
            left = [left]
        if isinstance(right, int):
            right = [right]
        return compare_packets(left, right)

def compare_packets(left, right):
    # Turns out you can use match-case with class patterns. It uses isinstance internally.
    # https://peps.python.org/pep-0622/#class-patterns
    # This would still be better as a proper cmp function
    match left, right:
        case int(), int():
            if left == right: return None
            return left <= right
        case list(), list():
            for (l1, r1) in zip(left, right):
                r = compare_packets(l1, r1)
                if r is not None:
                    return r
            ll, lr = len(left), len(right)
            if ll == lr:
                return None
            else:
                return ll < lr
        case int(), list():
            return compare_packets([left], right)
        case list(), int():
            return compare_packets(left, [right])

def cmp_packets(left, right):
    # Convert compare_packets to an old-style comparison function, so we can use cmp_to_key on it for sorting.
    # ("right order" is ascending order, left < right, so -1)
    r = compare_packets(left, right)
    match r:
        case None:
            return 0
        case True:
            return -1
        case False:
            return 1

def parse_packet(data):
    # Parsing the packets using json.loads().
    # Be careful, make sure you trust your input source. While this isn't as bad as eval, it's still not super safe.
    p1, p2 = data.split("\n")
    return (json.loads(p1), json.loads(p2))


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    packet_data = data.strip().split("\n\n")
    packets = [parse_packet(d) for d in packet_data]

    part1(packets)
    print("--------")
    part2(packets)
    