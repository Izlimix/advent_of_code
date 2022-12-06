#!/usr/bin/env python3

# https://adventofcode.com/2022/day/6

def part1(signal):
    start_pos = detect_start_packet(signal)
    print("Part 1 result:")
    print(f"Start packet marker detected after {start_pos} characters.")

def part2(signal):
    start_pos = detect_start_message(signal)
    print("Part 2 result:")
    print(f"Start message marker detected after {start_pos} characters.")
    

def detect_start_packet(signal):
    # Detect a start-of-packet marker, indicated by a sequence of 4 characters that are all different.
    return detect_start_marker(signal, 4)

def detect_start_message(signal):
    # Detect a start-of-message marker, indicated by a sequence of 14 characters that are all different.
    return detect_start_marker(signal, 14)

def detect_start_marker(signal, n):
    # Detect a start-marker of n different characters.
    for i in range(n, len(signal) + 1):
        cs = set(signal[i-n:i])
        if len(cs) == n:
            return i

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    signal = data.strip()
    
    part1(signal)
    print("--------")
    part2(signal)
    