#!/usr/bin/env python3

# https://adventofcode.com/2021/day/4

def part1(ns, boards):
    # get the score of the board that wins first
    winning_b = None
    for n in ns:
        for b in boards:
            if b.call(n):
                # This board just won!
                winning_b = b
                score = b.score(n)
                break
        if winning_b is not None: break
    
    print("Part 1 result:")
    if winning_b is not None:
        print("Winning board:")
        winning_b.pprint_checked()
        print("Winning score:")
        print(score)
    else:
        print("No boards won?")
        for b in boards:
            print("---- Boards: ----")
            b.pprint_checked()

def part2(ns, boards):
    # get the score of the board that wins last
    remaining_bs = boards
    final_b = None
    for n in ns:
        # print(f"Calling {n}")
        for b in remaining_bs:
            next_bs = remaining_bs[:]
            if b.call(n):
                # This board just won!
                if len(next_bs) <= 1:
                    # print(f"Final n: {n}")
                    final_b = b
                    score = b.score(n)
                    break
                else:
                    next_bs.remove(b)
            remaining_bs = next_bs # Hack so we're not iterating over and removing from remaining_bs at the same time 
        if final_b:
            break
    
    print("Part 2 result:")
    if final_b:
        print("Board that wins last:")
        final_b.pprint_checked()
        print("Score:")
        print(score)
    else:
        print("Maybe a tie?")
        for b in boards:
            print("---- Boards: ----")
            b.pprint_checked()
    
class Board:
    """A 5x5 bingo board"""
    def __init__(self, grid):
        # Each cell stores the number and whether it's been checked
        self.ns = set(e for line in grid for e in line)
        self.grid = [[(n, False) for n in line] for line in grid]
    
    @staticmethod
    def parse_board(lines):
        # Given some lines of whitespace-separated sudoku numbers, make a 5x5 board
        return Board(Helpers.line2grid(lines.strip().split()))
    
    def call(self, e):
        # A number was called, is it in our grid?
        # If it was, check whether we just won!
        if e in self.ns:
            l = len(self.grid)
            for i in range(l):
                for j in range(l):
                    (n, c) = self.grid[i][j]
                    if e == n:
                        self.grid[i][j] = (n, True)
                        if self.check_win(self.grid[i]) or self.check_win(self.col(j)):
                            return True
        return False

    def check_any_win(self):
        return any(self.check_win(line) for line in self.grid) or any(self.check_win(line) for line in self.cols())

    def check_win(self, line):
        return all(c for (n, c) in line)

    def cols(self):
        return (self.col(i) for i in range(len(self.grid)))

    def col(self, n):
        return Helpers.column(self.grid, n)
    
    def score(self, winning_n):
        # Score = (sum of unmarked numbers) * (the number that was just called when the board won)
        return sum(int(n) for line in self.grid for (n, c) in line if not c) * int(winning_n)

    def pprint(self):
        for line in self.grid:
            print(" ".join(n for (n, c) in line))

    def pprint_checked(self):
        for line in self.grid:
            print(" ".join(f"{n}{'!' if c else ''}" for (n, c) in line))

class Helpers:
    """Helper functions taken wholesale from a sudoku-solver doodle"""
    @staticmethod
    def line2grid(s, *, n=5):
        # Given a list, return it as an nxn grid
        grid = []
        for offset in range(0, n ** 2, n):
            grid.append(s[offset:offset+n])
        return grid

    @staticmethod
    def column(grid, col):
        return (grid[row][col] for row in range(len(grid)))


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    lines = data.strip().split("\n")
    ns = lines[0].split(",")
    # print("---- Numbers: ----")
    # print(ns)
    # print("---- Boards: ----")
    boards = [Board.parse_board(" ".join(lines[i:i+6])) for i in range(1, len(lines), 6)]
    
    """for b in boards:
        b.pprint_checked()
        print("--------")
    """

    part1(ns, boards)
    print("--------")
    part2(ns, boards)
    