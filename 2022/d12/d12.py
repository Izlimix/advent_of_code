#!/usr/bin/env python3

# https://adventofcode.com/2022/day/12
# Iterative DFS doesn't do very well here.
# And this implementation of A* should probably be replaced with BFS for less overhead.

import string
from queue import PriorityQueue

def part1(heightmap):
    map_h = len(heightmap)
    # Locate the start and destination in the map
    for y in range(map_h):
        sx = heightmap[y].find("S")
        if sx != -1:
            # found the start
            start = (sx, y)
            break
    for y in range(map_h):
        ex = heightmap[y].find("E")
        if ex != -1:
            # found the end
            end = (ex, y)
            break
    print(f"Found start at {start}, end at {end}")
    
    letter_heights = dict((letter, h) for (h, letter) in enumerate(string.ascii_lowercase, 1))
    letter_heights["S"] = 1
    letter_heights["E"] = 26
    
    finder = A_Star(heightmap, letter_heights, start)
    attempt = finder.find(end)
    print("Part 1 result:")
    #print("Final path:")
    #print(attempt)
    print(f"Looked at {len(finder.distance_to)} nodes")
    print(f"Number of steps: {len(attempt) - 1}") # Starting at (0, 0) doesn't count as a step

    
def part2(heightmap):
    map_h = len(heightmap)
    # We only need to find the end
    for y in range(map_h):
        ex = heightmap[y].find("E")
        if ex != -1:
            # found the end
            end = (ex, y)
            break
    print(f"Found end at {end}")

    letter_heights = dict((letter, h) for (h, letter) in enumerate(string.ascii_lowercase, 1))
    letter_heights["S"] = 1
    letter_heights["E"] = 26
    
    finder = A_Star(heightmap, letter_heights, end)
    attempt = finder.find_elevation(1)

    print("Part 2 result:")
    #print("Final path:")
    #print(attempt)
    print(f"Looked at {len(finder.distance_to)} nodes")
    print(f"Number of steps: {len(attempt) - 1}") # Starting at (0, 0) doesn't count as a step
    
    
def in_bounds(x, lower, higher):
    return lower <= x < higher

def manhattan_distance(a, b):
    return max(abs(a1 - b1) for (a1, b1) in zip(a, b))

class A_Star:
    def __init__(self, heightmap, letter_heights, start):
        self.heightmap = heightmap
        self.map_h = len(heightmap)
        self.map_w = len(heightmap[0])
        self.letter_heights = letter_heights
        self.start = start
        self.distance_to = dict() # The minimum distances from start
        self.seen_from = dict() # Which node did we come from to get here?
        self.priorities = PriorityQueue()
    
    def neighbours(self, node):
        offsets = [(-1, 0), (0, 1), (1, 0), (0, -1)] # NESW
        (x, y) = node
        for (off_x, off_y) in offsets:
            (x1, y1) = (x + off_x, y + off_y)
            if in_bounds(x1, 0, self.map_w) and in_bounds(y1, 0, self.map_h):
                yield (x1, y1)
    
    def find(self, end):
        if end in self.distance_to:
            # If we've already seen the end, return the path to it
            return self.path_from_start(end)
        
        self.priorities.put((0, self.start, None)) # Init priority queue
        end_x, end_y = end
        end_height = self.letter_heights[self.heightmap[end_y][end_x]]

        while not self.priorities.empty():
            (_, current, prev) = self.priorities.get()

            if current in self.distance_to and current != end:
                # We've already seen this node
                continue
            # When we visit a node for the first time, its prev node is the one we popped from the queue.
            # Its dist is that of the previous node + 1
            self.seen_from[current] = prev
            current_dist = self.distance_to.get(prev, 0) + 1
            self.distance_to[current] = current_dist
            
            if current == end:
                # Found the end!
                return self.path_from_start(end)
            (x, y) = current
            elevation = self.letter_heights[self.heightmap[y][x]]
            
            # Add reachable (height diff) neighbours to the priority queue    
            for n in self.neighbours(current):
                if n in self.distance_to:
                    # Already seen this node
                    continue
                nx, ny = n
                neighbour_height = self.letter_heights[self.heightmap[ny][nx]]
                if elevation + 1 >= neighbour_height:
                    # Estimate its distance to the end
                    height_diff = end_height - neighbour_height
                    dist_left = max(manhattan_distance(n, end), height_diff)

                    # Add to queue in the form (priority, node, node_from)
                    self.priorities.put((current_dist + 1 + dist_left, n, current))

        print("A* couldn't find a path. Visited nodes and distances:")
        for (node, d) in self.distance_to.items():
            print(f"{node}: {d}")
        return []

    # TODO: find an admissible heuristic. Closest a from current?
    def find_elevation(self, end_height=1):
        print(f"Searching from {self.start} for the closest node of height {end_height}")
        self.priorities.put((0, self.start, None)) # Init priority queue

        while not self.priorities.empty():
            (_, current, prev) = self.priorities.get()

            if current in self.distance_to:
                # We've already seen this node
                continue
            # When we visit a node for the first time, its prev node is the one we popped from the queue.
            # Its dist is that of the previous node + 1
            self.seen_from[current] = prev
            current_dist = self.distance_to.get(prev, 0) + 1
            self.distance_to[current] = current_dist
            
            (x, y) = current
            elevation = self.letter_heights[self.heightmap[y][x]]
            if elevation == end_height:
                # Found the closest a node!
                return self.path_from_start(current)
            
            # Add reachable (height diff) neighbours to the priority queue    
            for n in self.neighbours(current):
                if n in self.distance_to:
                    # Already seen this node
                    continue
                nx, ny = n
                neighbour_height = self.letter_heights[self.heightmap[ny][nx]]
                # Could we have reached the current node from this neighbour?
                if neighbour_height + 1 >= elevation:
                    # Estimate its distance to the end
                    height_diff = neighbour_height - end_height
                    dist_left = height_diff #max(manhattan_distance(n, end), height_diff)

                    # Add to queue in the form (priority, node, node_from)
                    self.priorities.put((current_dist + 1 + dist_left, n, current))

        print("A* couldn't find a path. Visited nodes and distances:")
        for (node, d) in self.distance_to.items():
            print(f"{node}: {d}")
        
        return []

    def path_from_start(self, node):
        prev = self.seen_from[node]
        if prev is None:
            return [node]
        else:
            return self.path_from_start(prev) + [node]

# (This DFS not used:)
# Depth-limited search (DFS with a depth-limit)
def _dls(heightmap, letter_heights, path, end, depth, map_h=None, map_w=None, visited_nodes=[0]):
    # Just for fun, to visualise how bad this is:
    visited_nodes[0] += 1
    if visited_nodes[0] % 100000 == 0:
        print(f"Now looked at {visited_nodes[0]} nodes")
    if depth <= 0:
        if path[-1] == end:
            # Found a solution!
            return path
        else:
            # Ran out of depth
            return None

    x, y = path[-1]
    elevation = letter_heights[heightmap[y][x]]
    if not (map_h and map_w):
        map_h = len(heightmap)
        map_w = len(heightmap[0])
    offsets = [(-1, 0), (0, 1), (1, 0), (0, -1)] # NESW
    
    # Of the adjacent nodes not in our path, pick one
    # When moving, only nodes of at most 1 higher than current can be reached
    for (off_x, off_y) in offsets:
        (poss_x, poss_y) = (x + off_x, y + off_y)
        if 0 > poss_x or poss_x >= map_w or 0 > poss_y or poss_y >= map_h:
            # Out of bounds
            continue
        if (poss_x, poss_y) in path:
            # We've visited this cell before
            continue
        dest_elevation = letter_heights[heightmap[poss_y][poss_x]]
        if dest_elevation > elevation + 1:
            # Too high
            continue
        path.append((poss_x, poss_y))
        attempt = _dls(heightmap, letter_heights, path, end, depth - 1, map_h, map_w)
        if attempt is not None:
            # We found a solution!
            return attempt
        
        # That didn't work, try the next possibility.
        del path[-1]
        
    # Tried all the possibilities, no path.
    return None

def part1b(heightmap):
    # Using this implementation of Iterative-deepening DFS doesn't work at all.
    map_h, map_w = len(heightmap), len(heightmap[0])
    # Locate the start and destination in the map
    for y in range(map_h):
        sx = heightmap[y].find("S")
        if sx != -1:
            # found the start
            start = (sx, y)
            break
    for y in range(map_h):
        ex = heightmap[y].find("E")
        if ex != -1:
            # found the end
            end = (ex, y)
            break
    print(f"Found start at {start}, end at {end}")
    
    letter_heights = dict((letter, h) for (h, letter) in enumerate(string.ascii_lowercase, 1))
    letter_heights["S"] = 1
    letter_heights["E"] = 26
    
    for d in range(25, map_h * map_w):
        print(f"Doing dls at depth {d}")
        attempt = _dls(heightmap, letter_heights, [start], end, d, map_h, map_w)
        if attempt is not None:
            break
        
    print("Part 1b result (iterative dfs):")
    print("Final path:")
    print(attempt)
    print(f"Number of steps: {len(attempt) - 1}") # Starting at (0, 0) doesn't count as a step

def explain_why_dfs_on_1b_is_terrible():
    print("Using depth-first-search and only remembering the current path, we examine routes covering the same nodes many times.")
    print("There's only one route of depth 0: Stay at (0, 0)")
    print("There's a maximum of 4 routes of exactly depth 1: Up, down, left and right from the origin.")
    print("For depth 2, there are a maximum of 16 routes (ignoring that 4 return to the origin)")
    print("So the number of routes at a certain depth is roughly 4 to the power of d.\n")

    print("Powers of 4:")
    for i in range(51):
        print(f"4 ** {i}: {4 ** i:,}")
    print("----")
    print("The solution to part 1 of this puzzle (with our input) has length 456.")
    import math
    print(f"4 ** 456: {4 ** 456:,}")
    print(f"^ Number of digits in base 10: {math.floor(math.log10(4 ** 456)) + 1}")
    

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    heightmap = data.strip().split("\n")

    part1(heightmap)
    print("--------")
    part2(heightmap)

    #explain_why_dfs_on_1b_is_terrible()
    #part1b(heightmap)
    