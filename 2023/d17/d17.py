#!/usr/bin/env python3

from queue import PriorityQueue
from dataclasses import dataclass, field

# https://adventofcode.com/2023/day/17

def part1(grid):
    city = City(grid)
    dest = (city.width - 1) + (city.height - 1) * 1j
    
    # Let's try not storing cells travelled.
    # Reduce valid directions to left and right turns (no straight moves), but we can move 3 tiles in that direction?
    # Start facing right and facing down
    # Heat loss, pos, dir offset
    start = [(0, 0j, 1), (0, 0j, 1j)]
    
    finder = A_Star(city)
    out = finder.find(start, dest)

    print(f"Part 1: min heat loss {out.heat=}")
    print(f"{out.path=}")

def part2(grid):
    city = City(grid)
    dest = (city.width - 1) + (city.height - 1) * 1j
    
    start = [(0, 0j, 1), (0, 0j, 1j)]
    
    finder = A_Star(city, 4, 10)
    out = finder.find(start, dest)

    print(f"Part 2: min heat loss {out.heat=}")
    print(f"{out.path=}")


@dataclass(order=True)
class Cell:
    priority: int
    heat: int=field(compare=False)
    pos: complex=field(compare=False)
    direction: complex=field(compare=False)
    path: list=field(default_factory=list, compare=False)
 
class City:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def neighbours(self, c: Cell, min_tiles: int = 1, max_tiles: int = 3) -> list[tuple[int, complex, complex]]:
        ns = []
        # Using 4HbQ's trick from day16 to get turn offsets    
        # Attempt 2: Instead of tracking number of cells in that direction,
        #  only turn+move 1-3 tiles, don't ever go straight. 
        # Don't remove seen here
        pos = c.pos
        d = c.direction
        heat = c.heat
        for d1 in (1j * d, -1j * d):
            h1 = heat
            # Add heat of all the skipped tiles
            for t in range(1, min_tiles):
                pos1 = pos + t * d1
                if not self.in_city(pos1):            
                    break
                h1 += self.heat_loss(pos1)

            # Add neighbours in bounds
            for t in range(min_tiles, max_tiles + 1):
                pos1 = pos + t * d1
                if not self.in_city(pos1):            
                    break
                # Heat of that tile = heat of cell + sum(heat of cells between incl.)
                h1 += self.heat_loss(pos1)
                ns.append((h1, pos1, d1))
        return ns
    
    def in_city(self, pos):
        return (0 <= pos.real < self.width) and (0 <= pos.imag < self.height)
    
    def heat_loss(self, pos):
        return int(self.grid[int(pos.imag)][int(pos.real)])


    
class A_Star:
    def __init__(self, city: City, min_tiles: int = 1, max_tiles: int = 3) -> None:
        self.city = city
        self.min_tiles = min_tiles
        self.max_tiles = max_tiles
    
    def find(self, start, goal):
        print(f"Searching for path from {start[1]} -> {goal}")
        candidates = PriorityQueue()
        seen = set()
        print(f"{start=}")
        for s in start:
            candidates.put(Cell(0, *s))
        while not candidates.empty():
            cell = candidates.get()
            if (cell.pos, cell.direction) in seen:
                continue

            seen.add((cell.pos, cell.direction))
            if cell.pos == goal:
                # We reached the goal!
                print(f"Reached goal!")
                return cell
            
            # Try cells next to this one
            ns = self.city.neighbours(cell, self.min_tiles, self.max_tiles)
            for (heat, pos, direction) in ns:
                # Estimate priority of each and add to queue
                est_dist = heat + taxicab_dist(pos, goal)
                candidates.put(Cell(est_dist, heat, pos, direction, cell.path[:] + [cell.pos]))
        print(f"A* couldn't find a path to {goal}")

def taxicab_dist(p1, p2):
    d = p1 - p2
    return abs(d.real) + abs(d.imag)


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip() 
    
    grid = data.split("\n")
    part1(grid)
    print("--------")
    part2(grid)
    