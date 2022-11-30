#!/usr/bin/env python3

# https://adventofcode.com/2021/day/3

from collections import Counter

def part1(lines):
    groups = zip(*lines)
    gamma, epsilon = [], []
    for place in groups:
        """
        counts = Counter(place).most_common()
        (g, _) = counts[0]
        (e, _) = counts[-1]
        """
        ((g, _), (e, _)) = most_and_least_common_e(place)
        gamma.append(g)
        epsilon.append(e)
    gamma = int("".join(gamma), 2)
    epsilon = int("".join(epsilon), 2)

    print("Part 1 result:")
    print(f"gamma: {gamma}")
    print(f"epsilon: {epsilon}")
    print(f"Power consumption: {gamma * epsilon}")

def part2(lines):
    oxy = int(find_rating(lines, True), 2)
    co2 = int(find_rating(lines, False), 2)
    print("Part 2 result:")
    print(f"Oxygen generator rating: {oxy}")
    print(f"CO2 scrubber rating: {co2}")
    print(f"Life support rating: {oxy * co2}")
    

def most_and_least_common_e(es):
    c = Counter()
    c.update(es)
    counts = c.most_common() # note: returns tied elements in insertion-order (tie-breaker not done here!)
    return (counts[0], counts[-1])

def find_rating(lines, oxy_mode=True):
    # Find the oxygen generator rating or co2 scrubber rating from the given lines
    bits = len(lines[0])
    possibles = lines
    tiebreaker = "1" if oxy_mode else "0"
    for i in range(bits):
        if len(possibles) <= 1:
            break
        ith_bits = (p[i] for p in possibles)
        ((most, n1), (least, n2)) = most_and_least_common_e(ith_bits)
        # Tie-breaker!
        if n1 == n2 and tiebreaker in (most, least):
            (most, least) = (tiebreaker, tiebreaker)
        
        bit_criteria = most if oxy_mode else least
        possibles = [p for p in possibles if p[i] == bit_criteria]
    return possibles[0]

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    lines = data.strip().split("\n")

    # While the input is a list of binary numbers, it's more convenient just treat them as arbitrary strings at first
    part1(lines)
    part2(lines)
    