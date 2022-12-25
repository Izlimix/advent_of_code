#!/usr/bin/env python3

# https://adventofcode.com/2022/day/25

def part1(ns):
    total = sum(snafu_to_dec(n) for n in ns)
    print("Part 1 result:")
    print(f"Total in decimal: {total}")
    snafu_total = dec_to_snafu(total)
    print(f"Total in SNAFU: {snafu_total}")

def snafu_to_dec(n):
    total = 0
    snafu_lookup = {
        "2": 2,
        "1": 1,
        "0": 0,
        "-": -1,
        "=": -2
    }
    for (i, c) in enumerate(str(n)[::-1]):
        total += snafu_lookup[c] * pow(5, i)
    return total

def dec_to_snafu(n):
    # From reddit. Apparently SNAFU is a balanced number system.
    # Doing divmod by 5 gives us n in base-5
    # From wiki, we can convert from ternary to balanced-ternary by adding 1 to every non-zero place with carry, 
    #   then subtract 1 from each place without borrow.
    # But SNAFU is balanced base-5, so we need to add and subtract 2 instead.
    # The n+2 adds 2 to the place, while the lookup subtracts 2 from every place without borrow.
    digits = []
    while n > 0:
        n, rem = divmod(n + 2, 5)
        digits.append("=-012"[rem])
    return "".join(digits[::-1])

def dec_to_base(n, b):
    digits = []
    while n >= b:
        n, rem = divmod(n, b)
        digits.append(str(rem))
    digits.append(str(n))
    return "".join(digits[::-1])


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    snafu_nums = data.strip().split("\n")
    
    part1(snafu_nums)
    print("--------")
    