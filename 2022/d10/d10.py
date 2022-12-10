#!/usr/bin/env python3

# https://adventofcode.com/2022/day/10

def part1(instructions):
    cycle = 0
    x = 1
    pending_op = None
    signal_strength = 0
    n_ops = len(instructions)
    i = 0

    while i < n_ops:
        cycle += 1
        # Look at signal strength during cycles 20, 60, ... (+ every 40 cycles after 20)
        if cycle % 40 == 20:
            signal_strength += cycle * x
        # The instruction finishes execution after the cycle
        if pending_op is not None:
            (op, n) = pending_op
            x += n
            pending_op = None
            continue
        op = instructions[i]
        match op.split(" "):
            case ["noop"]:
                pass
            case ["addx", n]:
                n = int(n)
                pending_op = ("addx", n)
        i += 1
    print("Part 1 result:")
    print(f"Signal strength sum: {signal_strength}")
    
def part2(instructions, crt_width=40, crt_height=6):
    x = 1
    pending_op = None
    ops = iter(instructions)

    for h in range(crt_height):
        for w in range(crt_width):
            # Draw a pixel during each cycle
            print("#" if (x - 1 <= w) and (w <= x + 1) else ".", end="")

            # The instruction finishes execution after the cycle
            if pending_op is not None:
                (op, n) = pending_op
                x += n
                pending_op = None
                continue
            op = next(ops)
            match op.split(" "):
                case ["noop"]:
                    pass
                case ["addx", n]:
                    n = int(n)
                    pending_op = ("addx", n)
        print("") # Next line of the picture!

    print("Part 2 result: ^")


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    instructions = data.strip().split("\n")
    
    part1(instructions)
    print("--------")
    part2(instructions)
    