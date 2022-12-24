#!/usr/bin/env python3

# https://adventofcode.com/2022/day/20

from tqdm import tqdm

def part1(ns):
    l = len(ns)
    for i in tqdm(range(l)):
        for (ind, (pos, n)) in enumerate(ns):
            if pos == i:
                current_pos, original_pos, v = ind, pos, n
                break
        else:
            print(f"Looked for original index {i} that's missing from ns")
            print(ns)
            raise Exception
        ns.pop(current_pos)
        ns.insert(wrap_into(current_pos + v, l - 1), (original_pos, v)) # This doesn't start the list in the right place, but it's ok
    #print(f"List after moves: {ns}")
    ns = [n for (_, n) in ns]
    idx0 = ns.index(0)
    # Result = sum(1000th, 2000th and 3000th numbers after 0)
    r = sum(ns[(idx0 + i) % l] for i in (1000, 2000, 3000))

    print("Part 1 result:")
    print(f"Sum of 1000th, 2000th and 3000th numbers after 0: {r}")

def part2(ns):
    key = 811589153
    ns = [(i, n * key) for (i, n) in ns]
    l = len(ns)
    for _ in tqdm(range(10)):
        for i in tqdm(range(l)):
            for (ind, (pos, n)) in enumerate(ns):
                if pos == i:
                    current_pos, original_pos, v = ind, pos, n
                    break
            else:
                print(f"Looked for original index {i} that's missing from ns")
                print(ns)
                raise Exception
            ns.pop(current_pos)
            ns.insert(wrap_into(current_pos + v, l - 1), (original_pos, v))
    
    ns = [n for (_, n) in ns]
    idx0 = ns.index(0)
    # Result = sum(1000th, 2000th and 3000th numbers after 0)
    r = sum(ns[(idx0 + i) % l] for i in (1000, 2000, 3000))

    print("Part 2 result:")
    print(f"Sum of 1000th, 2000th and 3000th numbers after 0: {r}")

def wrap_into(v, hi):
    if v < 0:
        cycles = -(v // hi) + 1
        return wrap_into(v + hi * cycles, hi)
    return v % hi

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    ns = [(i, int(n)) for (i, n) in enumerate(data.strip().split())] # Original pos, value
    print(f"Received {len(ns)} ns")
    
    part1(ns[:])
    print("--------")
    part2(ns[:])
    