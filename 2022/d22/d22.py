#!/usr/bin/env python3

# https://adventofcode.com/2022/day/22

import re
from enum import Enum

def part1(tilemap, borders, moves):
    row_borders, col_borders = borders
    pos = (row_borders[0][0], 0) # Note: this might be a wall.
    orientations = [(1, 0), (0, 1), (-1, 0), (0, -1)] # ESWN
    facing = 0 # Start facing East

    for m in moves:
        match m:
            case "R":
                # Clockwise turn
                facing = wrap(facing + 1, 0, 3)
            case "L":
                # Anti-clockwise turn
                facing = wrap(facing - 1, 0, 3)
            case n:
                # Move forwards n steps
                n = int(n)
                for i in range(n):
                    next_pos = add_pair(pos, orientations[facing])
                    tile = tilemap.get(next_pos, None)
                    match tile:
                        case Tile.OPEN:
                            pos = next_pos
                        case Tile.WALL:
                            # Blocked, skip to the next move~
                            break
                        case None:
                            #void, try to wrap around
                            row_lo, row_hi = row_borders[pos[1]]
                            col_lo, col_hi = col_borders[pos[0]]
                            wrapped_x, wrapped_y = wrap(next_pos[0], row_lo, row_hi), wrap(next_pos[1], col_lo, col_hi) # wraps based on the x, y of the ...?
                            match tilemap.get((wrapped_x, wrapped_y), None):
                                case Tile.OPEN:
                                    pos = (wrapped_x, wrapped_y)
                                case Tile.WALL:
                                    break
                                case None:
                                    print(f"Borders: row {row_borders[pos[1]]}, col {col_borders[pos[0]]}")
                                    print(f"Tried to move {n - i} facing {facing} from {pos}, wrapped from {next_pos} to {(wrapped_x, wrapped_y)}, but it's still void?")
                                    raise Exception
    print("---- Done moving ---- ")
    print(f"Final pos: {pos}, facing {facing}")
    # Note: the answer is 1-indexed, not 0
    pw = 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing # 1000 * row, 4 * col, facing
    print("Part 1 result:")
    print(f"Final password: {pw}")
    

def part2(tilemap, borders, moves):
    # Fold the map into a cube, wrap differently. Hm.
    # Each cube has 4 edges, connected to 1 edge of another cube
    # If we fall off of one face (50x50 map), we know which other map we'll be on.
    # Could try preprocessing to fold the cube.
    # Let's hard-code it first.

    # To split a map into faces, we can take the outermost corner and cut a 50x50 (or 4x4 for sample) square out, then repeat until we have 6
    # If you can go from one spot to another without void or wrap, then they're adjacent in the cube too.
    # ...

    # Attempt? 2:
    # Split into 50x50 faces
    # Connect each adjacent NESW edge (if manhattan distance between face //50 == 1)
    # Then, considering from each face in turn,
    # - Try and find two adjacent faces to zip up (NE, NW, SE, SW), call the directions d1 and d2
    # -- If both edges are known, and they don't already have a neighbour in that direction,
    # --- face1's neighbour in d2 is face2, face2's neighbour in d1 is face1
    # --- now that we have a new edge-pair, maybe we can fold their neighbours together.
    # After, whenever we fall off a face in a direction d1,
    # - We land on that face's neighbour in direction d1, on that face's d2 edge.
    # -- Our x and y coord are changed based on the clockwise-anticlockwise pair? (so prob 50 - x, 50 - y for the offset direction)

    # Attempt? 3: Let's just hardcode the wrapping manually.
    row_borders, _ = borders
    pos = (row_borders[0][0], 0) # Note: this might be a wall.
    orientations = [(1, 0), (0, 1), (-1, 0), (0, -1)] # ESWN
    facing = 0 # Start facing East

    for m in moves:
        match m:
            case "R":
                # Clockwise turn
                facing = wrap(facing + 1, 0, 3)
            case "L":
                # Anti-clockwise turn
                facing = wrap(facing - 1, 0, 3)
            case n:
                # Move forwards n steps
                n = int(n)
                for i in range(n):
                    next_pos = add_pair(pos, orientations[facing])
                    tile = tilemap.get(next_pos, None)
                    match tile:
                        case Tile.OPEN:
                            pos = next_pos
                        case Tile.WALL:
                            # Blocked, skip to the next move~
                            break
                        case None:
                            #void, wrap around the cube~
                            # Let's do the faces manually...
                            wrapped_facing, wrapped_x, wrapped_y = cube_wrap(facing, *pos)
                            match tilemap.get((wrapped_x, wrapped_y), None):
                                case Tile.OPEN:
                                    pos = (wrapped_x, wrapped_y)
                                    facing = wrapped_facing
                                case Tile.WALL:
                                    break
                                case None:
                                    print(f"Tried to move {n - i} facing {facing} from {pos}, wrapped from {next_pos} to {(wrapped_x, wrapped_y)} facing {wrapped_facing}, but it's still void?")
                                    raise Exception
    print("---- Done moving ---- ")
    print(f"Final pos: {pos}, facing {facing}")
    # Note: the answer is 1-indexed, not 0
    pw = 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing # 1000 * row, 4 * col, facing

    print("Part 2 result:")
    print(f"Final password: {pw}")

# Wrap a value around between lo and hi (inclusive)
def wrap(v, lo, hi):
    m = (hi + 1) - lo
    v1 = v - lo
    r = lo + (v1 % m)
    return r

def add_pair(p1, p2):
    return tuple(sum(vs) for vs in zip(p1, p2))

def cube_wrap(facing, x, y):
    # We fell into void. Wrap old pos to the next face, then add the offset!
    # Manual wrapping, only works on this specific cube.
    # facing: ESWN
    match facing, x // 50, y // 50:
        case 0, 2, 0:
            # Fell eastwards off face (2, 0), reappear on the east edge of face (1, 2)
            return (2, 99, 149 - y)
        case 0, 1, 1:
            # fell east off (1, 1), reappear south of (2, 0)
            return (3, y + 50, 49)
        case 0, 1, 2:
            # fell east off (1, 2), reappear east of (2, 0)
            return (2, 149, 149 - y)
        case 0, 0, 3:
            # fell east off (0, 3), reappear south of (1, 2)
            return (3, 50 + (y - 150), 149)
        case 1, 0, 3:
            # S (0,3) -> N (2,0)
            return (1, x + 100, 0)
        case 1, 1, 2:
            # S (1,2) -> E (0,3)
            return (2, 49, (x - 50) + 150)
        case 1, 2, 0:
            # S (2,0) -> E (1,1)
            return (2, 99, x - 50)
        case 2, 1, 0:
            # W (1,0) -> W (0,2)
            return (0, 0, 149 - y)
        case 2, 1, 1:
            # W (1,1) -> N (0,2)
            return (1, y - 50, 100)
        case 2, 0, 2:
            # W (0,2) -> W (1,0)
            return (0, 50, 149 - y)
        case 2, 0, 3:
            # W (0,3) -> N (1,0)
            return (1, y - 100, 0)
        case 3, 0, 2:
            # N (0,2) -> W (1,1)
            return (0, 50, x + 50)
        case 3, 1, 0:
            # N (1,0) -> W (0,3)
            return (0, 0, x + 100)
        case 3, 2, 0:
            # N (2,0) -> S (0,3)
            return (3, x - 100, 199)
    print(f"Tried to cube-wrap {(x, y)} facing {facing}, cube-face {(x // 50, y // 50)}, but it didn't match the faces?")
    raise Exception

class Tile(Enum):
    OPEN = 0
    WALL = 1

def pprint_map(tilemap):
    xs, ys = sorted(x for (x, _) in tilemap.keys()), sorted(y for (_, y) in tilemap.keys())
    print(f"{xs[0]}-{xs[-1]}")
    for y in range(ys[0], ys[-1] + 1):
        for x in range(xs[0], xs[-1] + 1):
            match tilemap.get((x, y), None):
                case None:
                    c = " "
                case Tile.OPEN:
                    c = "."
                case Tile.WALL:
                    c = "#"
            print(c, end="")
        print(y)
    

def parse_map(data):
    # For every (x, y), if it's the first or last . or # in the line, remember it as the edge
    # Also remember the edges of the top and bottom...
    # We can just do this as a post-processing step?
    lines = data.split("\n")
    tilemap = dict()
    
    for y in range(len(lines)):
        l = lines[y]
        for x in range(len(l)):
            c = l[x]
            match c:
                case "#":
                    tilemap[x, y] = Tile.WALL
                case ".":
                    tilemap[x, y] = Tile.OPEN

    # Post-processing: Get the first and last tiles of every row and column for part1 wrapping.
    row_borders = dict()
    col_borders = dict()
    xs, ys = sorted(x for (x, _) in tilemap.keys()), sorted(y for (_, y) in tilemap.keys())
    for x in range(xs[0], xs[-1] + 1):
        col = sorted(y1 for (x1, y1) in tilemap.keys() if x1 == x)
        col_borders[x] = (col[0], col[-1]) # lo, hi index of that col (inclusive)
    for y in range(ys[0], ys[-1] + 1):
        row = sorted(x1 for (x1, y1) in tilemap.keys() if y1 == y)
        row_borders[y] = (row[0], row[-1]) # lo, hi of that row

    return tilemap, row_borders, col_borders

def parse_moves(data):
    pattern = re.compile(r"(\d+|[LR])")
    return pattern.findall(data)

def _check_cubewraps(x_lo, x_hi, y_lo, y_hi, facing):
    face_coords = {(1,0), (2,0), (1,1), (0,2), (1,2), (0,3)}
    directions = "ESWN"
    for x in range(x_lo, x_hi):
        for y in range(y_lo, y_hi):
            face = (x // 50, y // 50)
            if face not in face_coords:
                print(f"Checking {(x, y)} on face {face}, but it's not one we know how to wrap!")
                raise Exception
            # ESWN
            f1, x1, y1 = cube_wrap(facing, x, y)
            dual = (f1 + 2) % 4
            f2, x2, y2 = cube_wrap(dual, x1, y1)
            dual2 = (f2 + 2) % 4
            if (facing, x, y) != (dual2, x2, y2):
                print("---- non-reversible wrap: ----")
                print(f"{directions[facing]} {(x, y)} -> {directions[f1]} {(x1, y1)}")
                print(f"{directions[dual]} {(x1, y1)} -> {directions[f2]} {(x2, y2)}")
    print(f"Done checking wraps {(x_lo, x_hi, y_lo, y_hi)} facing {facing}")

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    map_data, move_data = data.split("\n\n")

    tilemap, *borders = parse_map(map_data)
    moves = parse_moves(move_data)

    #print("Check cube-wraps are reversible")
    #_check_cubewraps(100, 150, 49, 50, 1)


    part1(tilemap, borders, moves)
    print("--------")
    part2(tilemap, borders, moves)    