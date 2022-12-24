#!/usr/bin/env python3

# https://adventofcode.com/2022/day/24

# Try A* with moving walls~
# The walls (blizzards) are always in the same place at every time step, so we could cache that.
# We can store positions as (x, y, t), can visualise as a 3D block~

from queue import PriorityQueue
from functools import cache

def part1(blizzards, bounds, start, goal):
    # Find the shortest path through the moving blizzards~
    finder = A_Star(blizzards, bounds, start, goal)
    attempt = finder.find()
    print(f"Path: {attempt}")

    print("Part 1 result:")
    print(f"Looked at {len(finder.distance_to)} nodes")
    print(f"Number of steps: {len(attempt) - 1}") # Starting doesn't count as a step

def part2(blizzards, bounds, start, goal):
    # Part 2: Shortest path from start to goal, then back to start, then to goal again.
    finder1 = A_Star(blizzards, bounds, start, goal, 0)
    attempt1 = finder1.find()
    t1 = len(attempt1) - 1
    #print(f"Path from start to goal: {attempt1}")
    print(f"Time taken on trip 1: {t1}")

    finder2 = A_Star(blizzards, bounds, goal, start, t1)
    attempt2 = finder2.find()
    t2 = len(attempt2) - 1
    #print(f"Path from goal to start: {attempt2}")
    print(f"Time taken on trip 2: {t2}")

    finder3 = A_Star(blizzards, bounds, start, goal, t1 + t2)
    attempt3 = finder3.find()
    t3 = len(attempt3) - 1
    #print(f"Path from start to goal again: {attempt3}")
    print(f"Time taken on trip 3: {t3}")

    print("Part 2 result:")
    print(f"Total time taken: {t1 + t2 + t3}")
    
class Blizzard:       
    directions = {
        "^": (0, -1),
        "v": (0, 1),
        "<": (-1, 0),
        ">": (1, 0)
    }

    def __init__(self, x, y, c):
        self.start_x = x
        self.start_y = y
        self.direction = c
    
    def pos(self, t, bounds):
        row_bounds, col_bounds = bounds
        off_x, off_y = Blizzard.directions[self.direction]
        x = wrap(self.start_x + off_x * t, *row_bounds)
        y = wrap(self.start_y + off_y * t, *col_bounds)
        return (x, y)

class A_Star:
    # Ripping A* structure from day 12~
    def __init__(self, blizzards, bounds, start, goal, start_t=0):
        self.blizzards = blizzards
        self.row_bounds = bounds[0]
        self.col_bounds = bounds[1]
        self.start = start
        self.goal = goal
        self.distance_to = dict() # The minimum distances from start
        self.seen_from = dict() # Which node did we come from to get here?
        self.priorities = PriorityQueue()
        self.start_t = start_t # for part 2, when you double-back.~
    
    def all_neighbours(self, node):
        offsets = [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)] # NESW + wait
        (x, y) = node
        for (off_x, off_y) in offsets:
            (x1, y1) = (x + off_x, y + off_y)
            yield (x1, y1)
    
    def find(self):
        self.priorities.put((0, self.start, self.start_t, None)) # Init priority queue

        while not self.priorities.empty():
            (_, current, t, prev) = self.priorities.get()

            if (current, t) in self.distance_to and current != self.goal:
                # We've already seen this node at this time
                continue
            # When we visit a node for the first time (at this time), its prev node is the one we popped from the queue.
            # Its dist is that of the previous node + 1
            # TODO: Dist == t? Except we can visit the same node at diff t.
            self.seen_from[(current, t)] = prev
            current_dist = self.distance_to.get((prev, t - 1), 0) + 1
            self.distance_to[(current, t)] = current_dist
            
            if current == self.goal:
                # Found the end!
                print(f"Found end {self.goal} at time {t}")
                return self.path_from_start(self.goal, t)
            
            # Add reachable (not walls at time t) neighbours to the priority queue    
            for n in self.all_neighbours(current):
                if (n, t + 1) in self.distance_to:
                    # Already seen this node at this time
                    continue
                nx, ny = n
                # Is it a blizzard-wall or one of the edges (except start and goal)?
                walls = walls_at_time(self.blizzards, (self.row_bounds, self.col_bounds), t + 1) #blizzard positions at the next t

                if (n not in walls) and (n in (self.start, self.goal) or 
                    (in_bounds_incl(nx, *self.row_bounds) and in_bounds_incl(ny, *self.col_bounds))):
                    # Estimate its distance to the end
                    dist_left = manhattan_distance(n, self.goal)

                    # Add to queue in the form (priority, node, t, node_from)
                    self.priorities.put((current_dist + 1 + dist_left, n, t + 1, current))

        print("A* couldn't find a path. Visited nodes and distances:")
        for (node, d) in self.distance_to.items():
            print(f"{node}: {d}")
        return []
    
    
    def path_from_start(self, node, t):
        prev = self.seen_from[(node, t)]
        if prev is None:
            return [node]
        else:
            return self.path_from_start(prev, t - 1) + [node]

def in_bounds_incl(x, lower, higher):
    return lower <= x <= higher

def manhattan_distance(a, b):
    return max(abs(a1 - b1) for (a1, b1) in zip(a, b))

# Wrap a +ve value around between lo and hi (inclusive)
def wrap(v, lo, hi):
    m = (hi + 1) - lo
    v1 = v - lo
    r = lo + ((v1 + m) % m)
    return r

# Can be cached as a frozenset, but check how many ts we need
@cache
def walls_at_time(blizzards, bounds, t):
    walls = dict()
    for b in blizzards:
        pos = b.pos(t, bounds)
        walls[pos] = walls.get(pos, []) + [b.direction]
    return walls

def pprint_walls(walls, x_hi, y_hi):
    print(f"1 - {x_hi}")
    for y in range(1, y_hi + 1):
        for x in range(1, x_hi + 1):
            bs = walls.get((x, y), [])
            l = len(bs)
            match l:
                case 0:
                    c = "."
                case 1:
                    c = bs[0]
                case n:
                    c = n
            print(c, end="")
        print(f" {y}")

def parse_blizzards(lines):
    blizzards = []
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            c = lines[y][x]
            if c in Blizzard.directions:
                blizzards.append(Blizzard(x, y, c))
    return frozenset(blizzards) # Freeze so we can cache it

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    lines = data.strip().split("\n")
    blizzards = parse_blizzards(lines)
    # x and y bounds (Inclusive, skipping walls)
    col_bounds = 1, len(lines) - 2
    row_bounds = 1, len(lines[0]) - 2
    # Start and end pos
    start = (lines[0].find("."), 0)
    goal = (lines[-1].find("."), len(lines) - 1)
    print(f"col_bounds: {col_bounds}, row_bounds: {row_bounds}, start {start}, goal {goal}")
    print("---- Done parsing ----")
    
    """
    for t in range(6):
        print(f"--- Round {t} ---")
        pprint_walls(walls_at_time(blizzards, (row_bounds, col_bounds), t), row_bounds[1], col_bounds[1]) # Row bounds and col bounds don't wrap at the right spots...
    """

    """
    # Since the blizzards loop when they reach the edge, the map is the same as round 0 in round lcm(35, 100) => 700 (lcm of height and width)
    print(f"Is the map at round 0 the same as at round 700?")
    r0 = walls_at_time(blizzards, (row_bounds, col_bounds), 0)
    r700 = walls_at_time(blizzards, (row_bounds, col_bounds), 700)
    print(f"r0 {r0}, r700 {r700}.")
    print(f"Equal? {r0 == r700}")
    """

    part1(blizzards, (row_bounds, col_bounds), start, goal)
    print("--------")
    part2(blizzards, (row_bounds, col_bounds), start, goal)
    