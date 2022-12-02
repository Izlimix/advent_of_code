#!/usr/bin/env python3

# https://adventofcode.com/2022/day/2

def part1(rounds):
    score = 0
    elf_moves = {"A": 1, "B": 2, "C": 3} # (Each represented by its score: 1 for Rock, 2 for Paper, and 3 for Scissors)
    your_moves = {"X": 1, "Y": 2, "Z": 3}
    for (elf, you) in rounds:
        e = elf_moves[elf]
        y = your_moves[you]

        score += y # You get points for the shape you select
        if e == y:
            # Tie!
            score += 3
        elif (y - (e % 3)) == 1:
            # You won!
            score += 6
    print("Part 1 result:")
    print(f"Your total score = {score}")
    
def part2(rounds):
    score = 0
    elf_moves = {"A": 1, "B": 2, "C": 3} # (Each represented by its score: 1 for Rock, 2 for Paper, and 3 for Scissors)
    your_offset = {"X": -1, "Y": 0, "Z": 1} # You need to X: Lose, Y: Draw, Z: Win
    for (elf, you) in rounds:
        e = elf_moves[elf]
        y = (your_offset[you] + e) % 3
        if y == 0: y = 3 # Loop back around

        score += y # You get points for the shape you select
        if e == y:
            # Tie!
            score += 3
        elif (y - (e % 3)) == 1:
            # You won!
            score += 6
    print("Part 2 result:")
    print(f"Your total score = {score}")
    

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    rounds = [line.split() for line in data.strip().split("\n")]

    part1(rounds)
    print("--------")
    part2(rounds)
    