#!/usr/bin/env python3
import re

# https://adventofcode.com/2023/day/4


def part1(lines):
    total = 0
    # Could just use str.split() twice here
    pattern = re.compile(r"^Card (?:[ \d]+): ([\d ]+) \| ([\d ]+)$")
    for l in lines:
        m = pattern.match(l)
        card, winning_numbers = m.groups()
        # List of card numbers, just in case there are duplicates
        card = list(card.split())
        winning_numbers = set(winning_numbers.split())
        wins = sum(1 for c in card if c in winning_numbers)
        if wins > 0:
            total += pow(2, wins - 1)

    print(f"Part 1: Total points of winning cards = {total}")
    
    
def part2(lines):
    # Start with one copy of each scratch card
    n_cards = len(lines)
    scratchcards = dict.fromkeys(range(1, n_cards + 1), 1)
    # Could just use str.split() twice here
    pattern = re.compile(r"^Card (?:[ \d]+): ([\d ]+) \| ([\d ]+)$")
    for (i, l) in enumerate(lines, 1):
        m = pattern.match(l)
        card, winning_numbers = m.groups()
        # List of card numbers, just in case there are duplicates
        card = list(card.split())
        winning_numbers = set(winning_numbers.split())
        wins = sum(1 for c in card if c in winning_numbers)
        
        # Make copies of the following cards
        # We get 1 copy of each following card per copy of this card we own
        copies = scratchcards[i]
        # Can't make copies of cards past the end of the table (actually safe without this, as defined by the problem)
        # copy_end = min(n_cards, i + wins) + 1
        # for c in range(i + 1, copy_end):
        #     scratchcards[c] += copies
        for c in range(i + 1, i + wins + 1):
            scratchcards[c] += copies

    print(f"Part 2: Total number of scratchcards = {sum(scratchcards.values())}")


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
    