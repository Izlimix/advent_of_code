#!/usr/bin/env python3

# https://adventofcode.com/2022/day/15

import re

def part1(sensors, line_y=10):
    # Circle-line intersection, except the circles are diamonds bc Manhattan distance instead of Euclidean
    # The input coords are so large that it doesn't look feasible to store every point
    
    # Given a row number, how many positions can't contain a beacon?
    # Given a circle (pt, manhattan radius), we can find whether a horizontal line intersects with it
    # If pt_y - radius <= line_y <= pt_y + radius, then they intersect
    # Find the two points on the line where they intersect. Every point between is blocked (within the circle).
    segments = []
    for (sx, sy, bx, by) in sensors:
        radius = manhattan_distance((sx, sy), (bx, by))
        intersects = intersection_points((sx, sy), radius, line_y)
        if intersects is not None:
            segments.append(intersects)

    # Now we have a bunch of line segments of blocked points. Find the total non-overlapping length.
    # Sort by x values, sweep left-to-right. Whenever we see a new point, the space from the previous point is blocked iff the "active lines" set is empty
    # (If one line segment starts where another ends, that point should be included.)
    # (Include both start and end points. Does that already cover ^? Yes.)
    blocked = 0
    if not segments:
        print(f"No circles intersect with y={line_y}")
        return
    segments.sort()
    blocked_start, blocked_end = None, None
    for i in range(len(segments)):
        (start_x, end_x) = segments[i]
        # Only store current blocking line's min start and max end x! If the stored x < the new start x, then flush and add to blocked length.
        if blocked_end is None:
            (blocked_start, blocked_end) = start_x, end_x
            continue
        if blocked_end < start_x:
            # The last segment and this one don't intersect. Flush~
            blocked += (blocked_end + 1) - blocked_start # end +1 to include both ends
            blocked_start, blocked_end = start_x, end_x
        else:
            # The last segment intersects with this one
            blocked_end = max(blocked_end, end_x)

    # Flush the last line
    if blocked_end is not None:
        blocked += (blocked_end + 1) - blocked_start # end +1 to include both ends
    
    # If any beacons lie directly on the line, subtract 1 from our total for each.
    # (set, as the same beacon can be the closest to more than one sensor.)
    known_beacons = set((bx, by) for (_, _, bx, by) in sensors)
    #print(f"Number of beacons on the line: {sum(1 for (_, by) in known_beacons if by == line_y)}")
    blocked -= sum(1 for (_, by) in known_beacons if by == line_y)

    print("Part 1 result:")
    print(f"Positions in row {line_y:,} that can't contain a beacon: {blocked:,}")

def part2(sensors, bound_lo=0, bound_hi=4_000_000):
    for line_y in range(bound_lo, bound_hi):
        if line_y % 10000 == 0:
            print(f"Processing line {line_y}...")
        segments = []
        for (sx, sy, bx, by) in sensors:
            radius = manhattan_distance((sx, sy), (bx, by))
            intersects = intersection_points((sx, sy), radius, line_y)
            if intersects is not None:
                segments.append(intersects)

        if not segments:
            #print(f"No circles intersect with y={line_y}")
            continue
        segments = [(max(bound_lo, x1), min(bound_hi, x2)) for (x1, x2) in segments if x1 >= bound_lo or x2 <= bound_hi]
        segments.sort()
        blocked_start, blocked_end = None, None
        for i in range(len(segments)):
            (start_x, end_x) = segments[i]
            # Only store current blocking line's min start and max end x! If the stored x < the new start x, then flush and add to blocked length.
            if blocked_end is None:
                (blocked_start, blocked_end) = start_x, end_x
                continue
            if blocked_end < start_x:
                # The last segment and this one don't intersect. Our answer! (unless we're unlucky and it's on an edge)
                print(f"Non-intersecting on line {line_y}! Prev: {(blocked_start, blocked_end)}. New: {(start_x, end_x)}")
                print(f"Part 2 distress beacon position: {(start_x - 1, line_y)}")
                print(f"Tuning frequency: {(start_x - 1) * 4_000_000 + line_y:,}")
                return
            else:
                # The last segment intersects with this one
                blocked_end = max(blocked_end, end_x)
    
def manhattan_distance(p1, p2):
    return sum(abs(x1 - x2) for (x1, x2) in zip(p1, p2))

def intersection_points(sensor, radius, line_y):
    # Find the (x-coord of the) points where line_y intersects with the diamond made by the sensor
    (s_x, s_y) = sensor
    y_dist = abs(s_y - line_y)
    #dist = manhattan_distance(sensor, (s_x, line_y))
    if y_dist > radius:
        # The circle and line don't intersect
        return None
    # The 2 points are at x', y where x' is the x of the sensor +- (manhattan_dist - y dist) 
    x_off = radius - y_dist
    # Since radius >= y_dist and y_dist >= 0 (+ve or 0), x_off >= 0. So this should give them in ascending order.
    return (s_x - x_off, s_x + x_off)

def find_sensors(data):
    pattern = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    return [list(map(int, m)) for m in pattern.findall(data)]

# Debug
def _inspect(sensors, interesting_y=3442119):
    for sensor in sensors:
        print(sensor)
        (sx, sy, bx, by) = sensor
        dist = manhattan_distance((sx, sy), (bx, by))
        print(f"Manhattan dist: {dist}")
        intersections = intersection_points((sx, sy), dist, interesting_y)
        if intersections:
            (x1, x2) = intersections
            print(f"Intersects y={interesting_y} at {(x1, interesting_y)} and {(x2, interesting_y)}")
        print("----")
    known_beacons = set((bx, by) for (_, _, bx, by) in sensors)
    print(f"Beacons on line: {sum(1 for (bx, by) in known_beacons if by == interesting_y)}")
    for (bx, by) in known_beacons:
        if by == interesting_y:
            print((bx, by))

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    sensors = find_sensors(data)

    part1(sensors, 2000000)
    print("--------")
    part2(sensors, 0, 4_000_000)
    