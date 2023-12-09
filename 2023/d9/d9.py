#!/usr/bin/env python3
from tqdm import tqdm

# https://adventofcode.com/2023/day/9


def extrapolate(lines, backwards=False):
    total = 0
    for l in tqdm(lines):
        values = [int(v) for v in l.split()]
        if backwards:
            values = values[::-1]
        # Repeatedly get the deltas until the diffs are all 0
        diffs = [values, deltas(values)]
        d = diffs[-1]
        while any(v != 0 for v in d):
            d = deltas(d)
            diffs.append(d)

        # Infer the next final value by adding up the final value of each delta
        inferred_v = sum(d[-1] for d in diffs)
        total += inferred_v

    print(f"{backwards=} extrapolated value = {total}")
    
def deltas(ls):
    return [b - a for (a, b) in zip(ls, ls[1:])]


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip()

    lines = data.split("\n")
    print("Part 1:")
    extrapolate(lines)
    print("--------")
    print("Part 2:")
    extrapolate(lines, backwards=True)
    