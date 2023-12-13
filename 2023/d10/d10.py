#!/usr/bin/env python3

# https://adventofcode.com/2023/day/10


# Which directions does each tile face?
tiles = {
    "|": [-1j, +1j],
    "-": [-1, +1],
    "L": [-1j, +1],
    "J": [-1j, -1],
    "7": [+1j, -1],
    "F": [+1j, +1],
    ".": [],
    "S": [-1j, +1j, -1, +1]
}


def part1(pipes, start_pos, path):
    # Get the closest distance for each cell from the start (by traversing the path forwards and backwards)
    ds_forward = {pos: dist for (dist, pos) in enumerate(path, 1)}
    ds_backward = {pos: dist for (dist, pos) in enumerate(path[::-1], 1)}
    min_ds = {pos: min(d1, ds_backward[pos]) for (pos, d1) in ds_forward.items()}

    # Which tile is furthest away?
    furthest_d = max(min_ds.values())
    print(f"Part 1: The furthest point in the loop is {furthest_d} steps away")
    
def part2(lines, pipes, start_pos, path):
    # Given the simplified pipes, let's start by printing out only the loop
    # print_loop(lines, pipes)

    # Hint on one approach from reddit:
    # - Draw a straight line from a point in any direction
    # - If it passes through the shape an odd number of times, it's inside
    # - If it's an even number of times, it's outside (for every time you enter the shape, you also exit it)
    # This is complicated slightly when your line is tangent to the shape. That'll either be 0 or 2 entrances/exits
    
    # So scan through the simplified input line-by-line.
    # If the point isn't part of the loop, check if it's inside or outside
    # If the point is a vertical piece, then increment the count of times we've crossed the shape-boundary
    points_inside = 0
    for (y, l) in enumerate(lines):
        vert_pipes_crossed = 0
        for (x, c) in enumerate(l):
            pos = (x + y * 1j)
            if pos not in pipes:
                # Piece isn't part of pipes, check if inside or outside
                if vert_pipes_crossed % 2:
                    # Odd number of crossings, we're inside
                    points_inside += 1
            else:
                # handle FJ/L7 (with any number of -) = vert |, F7/LJ (with any hypens) = no change
                # -> Option 1 (my preferred): When we see F or L, remember (through any hyphens) until we reach 7 or J. 
                # -- For the 2nd one, flip vert_flag again if it's from the same direction (F7 or LJ)
                # -> Option 2: When we see F or L, they must be followed by (-*) then 7 or J
                # -- There are no intermediate pipes that are holes (all are hyphens), so this is safe
                # -- If we only count N pieces, then LJ will cancel itself out, F7 won't trigger a flip, and FJ and L7 will both trigger only one flip (equiv to |)
                if c == "S":
                    c = infer_start_piece(pipes, pos)
                    print(f"Inferred start piece {pos} shape is {c}")

                # Is it a vertical piece?
                match c:
                    case "-":
                        # Horizontal, skip
                        continue
                    case "|":
                        vert_pipes_crossed += 1
                    case "F" | "L":
                        # Remember until we reach L or J
                        horiz_start_piece = c
                        vert_pipes_crossed += 1
                    # check if it's the same direction the start of this horizontal section
                    # (Same direction: cancels itself out)    
                    case "7":
                        if horiz_start_piece == "F":
                            vert_pipes_crossed += 1
                        horiz_start_piece = None
                    case "J":
                        if horiz_start_piece == "L":
                            vert_pipes_crossed += 1
                        horiz_start_piece = None
    
    print(f"Part 2: {points_inside=}")


def parse_input(lines: list[str]) -> tuple[dict[complex, list[complex]], complex, list[complex]]:
    # First, parse the map.
    # Find the start S and pipes connected to it
    #  (our input only has 2 pipes actually connected to it, thankfully)
    pipes = dict()
    
    # Parse map and find the start. 
    start_pos = None
    for (y, l) in enumerate(lines):
        for (x, c) in enumerate(l):
            pos = x + y * 1j
            if c == "S": 
                start_pos = pos
            # Store the neighbours of each tile rather than the relative offset of neighbours
            neighbours = [pos + offset for offset in tiles[c]]
            pipes[pos] = neighbours
    
    print(f"Done parsing, {start_pos=}")
    # Simplify start_pos neighbours so we know what shape it is
    pipes[start_pos] = [neighbour for neighbour in pipes[start_pos] if facing(pipes, start_pos, neighbour)]
    print(f"Facing neighbours of start: {pipes[start_pos]}")

    path = trace_loop(pipes, start_pos)[1:-1]
    print(f"Loop length (not including S) = {len(path)}")
    return pipes, start_pos, path


def facing(pipes, pos1, pos2):
    # Given two tiles, can you get from one to the other?
    # Take the coord diff of A and B. 
    # They're facing if (A-B) is a valid path from A and (B-A) is a valid path from B.

    # (or, if we're storing neighbour pos instead of offsets, then facing if
    #  A is a neighbour of B and vice versa)
    return (pos2 in pipes.get(pos1, [])) and (pos1 in pipes.get(pos2, []))

def is_vert(pipes, pos):
    # Is the starting pipe a vertical pipe?
    # (Since we didn't store the offsets initially)
    neighbours = pipes[pos]
    return any((pos - n).imag != 0 for n in neighbours)

def infer_start_piece(pipes, pos):
    # Based on the (already-inferred) neighbour offsets, what's the start piece's character?
    # Get the offsets of S from each facing neighbour
    offsets = set(n - pos for n in pipes[pos])
    for (c, offs) in tiles.items():
        if offsets == set(offs):
            return c
    raise Exception(f"Got the offsets of start wrong, can't infer shape. Start {pos=}, neighbours {pipes[pos]=}, offsets {offsets=}")

def trace_loop(pipes, start_pos):
    # Find the full path of the loop (in the correct order) that includes the start
    path = [start_pos]
    # Arbitrarily pick a direction from the facing-neighbours of start
    for n in pipes[start_pos]:
        if facing(pipes, start_pos, n):
            path.append(n)
            break
    # Keep following the pipe in that direction until we find start_pos again!
    while True:
        pos1 = path[-1]
        neighbours = [pos2 for pos2 in pipes[pos1] if pos2 != path[-2] and facing(pipes, pos1, pos2)]
        # print(f"Going from {pos1=} to {neighbours=}")
        # There should only be 1 valid new neighbour here, since all pipes (except S) only connect to 2 tiles
        if len(neighbours) != 1:
            raise Exception(f"Unexpected number of neighbours for {pos1=}. {path=}")
        pos2 = neighbours[0]
        path.append(pos2)
        if pos2 == start_pos:
            # We reached the start pos again!
            break
    
    return path

def print_loop(lines, pipes):
    out = []
    for (y, l) in enumerate(lines):
        out_row = []
        for (x, c) in enumerate(l):
            pos = (x + y * 1j)
            if pos not in pipes:
                c = "."
            out_row.append(c)
        out.append("".join(out_row))
    
    out_s = "\n".join(out)
    print(out_s)
    # with open("input_simplified.txt", "w") as f:
    #     f.write(out_s)


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip()
    lines = data.split()

    pipes, start_pos, path = parse_input(lines)
    # Simplify path to only include useful pipes
    for k in set(pipes).difference(path):
        if k != start_pos:
            del pipes[k]
    # print(f"Simplified pipes: {pipes}")
    part1(pipes, start_pos, path)
    print("--------")
    part2(lines, pipes, start_pos, path)
    