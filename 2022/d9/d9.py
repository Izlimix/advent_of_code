#!/usr/bin/env python3

# https://adventofcode.com/2022/day/9

def part1(moves):
    hx, hy = 0, 0
    tx, ty = 0, 0
    t_visited = set()
    t_visited.add((tx, ty))
    for m in moves:
        ((offset_x, offset_y), n) = parse_move(m)
        for _ in range(n):
            hx_prev, hy_prev = hx, hy
            # Head moves
            hx += offset_x
            hy += offset_y
            # Tail follows if chebyshev-distance > 1
            if max(abs(hx - tx), abs(hy - ty)) > 1:
                # Since head can only move in cardinal directions, tail just follows to the prev position of h
                tx, ty = hx_prev, hy_prev
                t_visited.add((tx, ty))

    print("Part 1 result:")
    print(f"The tail visited {len(t_visited)} unique positions")
    
def part2(moves, n_knots=10):
    # Now with 10 knots!
    # Note: Intermediate knots can move diagonally! So the next knot can't just follow to the previous position
    knots = [(0, 0) for _ in range(n_knots)]
    tail_visited = set()
    tail_visited.add(knots[-1])
    for m in moves:
        ((offset_x, offset_y), n) = parse_move(m)
        for _ in range(n):
            # Head moves
            hx, hy = knots[0]
            knots[0] = (hx + offset_x, hy + offset_y)
            # Each tail follows
            for i in range(1, n_knots):
                knots[i] = follow(*knots[i-1], *knots[i])
            # Remember the position of the final knot
            tail_visited.add(knots[-1])

    print("Part 2 result:")
    print(f"The tail visited {len(tail_visited)} unique positions")
    
directions = {
    "U": (0, 1), # going up increases our y but not x
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0)
}

def parse_move(move):
    (d, n) = move.split(" ")
    n = int(n)
    offset = directions[d]
    return (offset, n)

def follow(hx, hy, tx, ty):
    # Given the new position of the head (hx, hy) and the current pos of the tail (tx, ty), get the new position of the tail
    
    # tail only follows if the head's more than 1 chebyshev-unit away     
    if max(abs(hx - tx), abs(hy - ty)) <= 1: return (tx, ty)
    # If the head is vertical or diagonal with the tail, the tail follows in the same direction
    if hx == tx or hy == ty:
        # We take the average of the two values since steps are only 1-large, to avoid direction maths >.>
        tx += (hx - tx) // 2
        ty += (hy - ty) // 2
    else:
        # The head is diagonal from the tail. The tail takes 1 step in each of x and y to catch up
        if hx > tx:
            tx += 1
        else:
            tx -= 1
        if hy > ty:
            ty += 1
        else:
            ty -= 1
    return (tx, ty)

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    moves = data.strip().split("\n")
    
    part1(moves)
    print("--------")
    #print("Sanity checking: part 2 with 2 knots should be the same as part 1.")
    #part2(moves, 2)
    print("--------")
    part2(moves)
    