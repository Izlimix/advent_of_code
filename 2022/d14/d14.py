#!/usr/bin/env python3

# https://adventofcode.com/2022/day/14

# Default pretty-printing symbols
WALL_CHAR = "#"
SAND_CHAR = "o"
VOID_CHAR = " "


def part1(walls, *, pretty_print=False):
    (sand_map, settled_grains) = sand(walls, floor=False)
    if pretty_print:
        pprint_map(sand_map)
    print("Part 1 result:")
    print(f"Units of sand that come to rest before falling into the abyss: {settled_grains}")
    
def part2(walls, *, pretty_print=False):
    (sand_map, settled_grains) = sand(walls, floor=True)
    if pretty_print:
        pprint_map(sand_map)
    print("Part 2 result:")
    print(f"Units of sand that come to rest before the origin is blocked: {settled_grains}")

def sand(walls, floor=False, wall_char=WALL_CHAR, sand_char=SAND_CHAR):
    sand_origin = (500, 0)
    sand_map = dict.fromkeys(walls, wall_char)

    lowest_wall_y = max(y for (_, y) in sand_map)
    ground_level = lowest_wall_y + 2
    fall_offsets = [(0, 1), (-1, 1), (1, 1)] # down, down-left, down-right
    settled_grains = 0
    
    # Drop each grain of sand one-by-one
    falling_sand = sand_origin
    while falling_sand is not None:
        (x, y) = falling_sand
        # Part 1: Are we falling into the void? Then we're done!
        if not floor and y >= lowest_wall_y:
            falling_sand = None
            break
        # Try to fall down, down-left, down-right
        for (x_off, y_off) in fall_offsets:
            (next_x, next_y) = (x + x_off, y + y_off)
            if floor and next_y >= ground_level:
                # Part 2: Reached the floor
                continue 
            if (next_x, next_y) not in sand_map:
                falling_sand = (next_x, next_y)
                break
        else:
            # Couldn't fall, settle here.
            sand_map[falling_sand] = sand_char
            settled_grains += 1
            # Part 2: If we just settled on the origin, we're done!
            if floor and falling_sand == sand_origin:
                falling_sand = None
                break
            else:
                # Next piece of sand...
                falling_sand = sand_origin
    
    return (sand_map, settled_grains)


def pprint_map(points, void_char=VOID_CHAR):
    xs = sorted(x for (x, _) in points)
    x_lo, x_hi = xs[0], xs[-1]
    ys = sorted(y for (_, y) in points)
    y_lo, y_hi = ys[0], ys[-1]
    print(f"x lo {x_lo} hi {x_hi}")
    print(f"y lo {y_lo} hi {y_hi}")
    print(f"x {x_lo} - {x_hi}")
    for y in range(y_lo, y_hi + 1):
        for x in range(x_lo, x_hi + 1):
            print(points.get((x, y), void_char), end="")
        print()

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    inp_lines = data.strip().split("\n")

    """
    # Data exploration. Based on this, the map isn't too big to brute-force by storing every point.
    xs, ys = [], []
    for l in inp_lines:
        for coord in l.split(" -> "):
            (x, y) = coord.split(",")
            xs.append(int(x))
            ys.append(int(y))
    xs.sort()
    ys.sort()
    print(f"Lengths: {len(xs)} {len(ys)}")
    print(f"X ranges from {xs[0]} to {xs[-1]}")
    print(f"y ranges from {ys[0]} to {ys[-1]}")
    """

    line_segments = []
    for l in inp_lines:
        points = [tuple(map(int, coord.split(","))) for coord in l.split(" -> ") ]
        for (p1, p2) in zip(points, points[1:]):
            line_segments.append((p1, p2))

    # Wall-parsing, pass it in and copy? (since the sand mutates walls)
    # Brute-force this, make a set (dict for pretty-printing characters) of every occupied cell
    # (could try storing lines and a set of sand-occupied cells instead)
    walls = set()
    for ((x1, y1), (x2, y2)) in line_segments:
        # Note: This line below only works because the walls are horizontal or vertical, not diagonal.
        x_lo, x_hi = min(x1, x2), max(x1, x2)
        y_lo, y_hi = min(y1, y2), max(y1, y2)
        walls.update((x, y) for x in range(x_lo, x_hi + 1) for y in range(y_lo, y_hi + 1))
    

    part1(walls, pretty_print=True)
    print("--------")
    part2(walls, pretty_print=False)
    