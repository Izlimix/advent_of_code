#!/usr/bin/env python3

# https://adventofcode.com/2022/day/18

from collections import deque

# Detect exposed surface area of voxels
# Options:
# Sort list of voxels by coordinates before adding them (not really useful)
# Might need to detect inner-cavities? (prob part 2... yep.)
# Can do 6 scans (forwards and backwards through each of x, y, z) to see if, for every cell, whether its face is blocked by an adjacent cell in that dir
# Flood-fill from outside to see which cells are reachable, then only count the... hm.
# -> E.g. cell (20, 12, 11) has an outer-exposed face and an inner-face that's exposed to an air pocket but not outside.
# -> Some air pockets might have contact with outside through a vert-tunnel.
# Just simulate this in MC, with a ball of water and a ball of lava :p

# Flood-fill from outside. The faces you find are the ones exposed to air.
# Whenever you touch a cell face, remember which direction you touched. That's 1 to our exposed count.
# (This doesn't use our part1 solution though...)

# We can invert the voxels. Then flood-fill travelling through the air from the outside. Any cells we don't travel through become filled!
# Then we just invert again, and count using part 1. (having filled all the internal bubbles)
# To make sure we touch every outer cell, pad the outermost layer with air, and start our flood from each of those voxels.
# Our coords range from 0-21 on each axis (x, y, z). After padding with air to (-1, 22), that's 24 ^ 3 = 13824 voxels to search through max.

def part1(voxels):
    print(f"Received {len(voxels)} cubes")
    vs = set(voxels)
    print(f"{len(vs)} are unique")
    exposed = exposed_faces(vs)

    print("Part 1 result:")
    print(f"Total surface area: {exposed}")

def part2(voxels):
    # Yup, need to detect air pockets.
    # Invert. Pad the outermost layer with air, then travel inwards detecting all air-cells.
    # Then invert again, which fills all air cells not reachable from the outside. Then just run part 1 again on our now-solid mass!
    vs = set(voxels)
    v_xs = sorted(map(get_axis("x"), vs))
    v_ys = sorted(map(get_axis("y"), vs))
    v_zs = sorted(map(get_axis("z"), vs))
    
    # Pad the outside with a layer of air. (An air bounding box!)
    bounding_air = set()
    x_lo, x_hi = v_xs[0] - 1, v_xs[-1] + 1
    y_lo, y_hi = v_ys[0] - 1, v_ys[-1] + 1
    z_lo, z_hi = v_zs[0] - 1, v_zs[-1] + 1
    for x in range(x_lo, x_hi + 1):
        for y in range(y_lo, y_hi + 1):
            for z in range(z_lo, z_hi + 1):
                if x in (x_lo, x_hi) or y in (y_lo, y_hi) or z in (z_lo, z_hi):
                    bounding_air.add((x, y, z))
    
    seen = set()
    explore = deque(bounding_air) # It's all connected so we really only need the first cell
    offsets = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    def in_bounds(x, y, z):
        return (x_lo < x < x_hi) and (y_lo < y < y_hi) and (z_lo < z < z_hi)

    try:
        while True:
            current = explore.pop()
            if current in seen:
                continue
            seen.add(current)
            (x, y, z) = current
            # Explore neighbours
            for (x_off, y_off, z_off) in offsets:
                neighbour = (x + x_off, y + y_off, z + z_off)
                # Add neighbours if they're in bounds and also air 
                if in_bounds(*neighbour) and neighbour not in vs:
                    explore.append(neighbour)
    except IndexError:
        # Done exploring!
        pass
    
    print(f"Done exploring. {len(seen)} air cells touched, of which {len(seen) - len(bounding_air)} were in the original.")

    vs_filled = set(vs)
    # Now re-invert, keeping only air cells that we just touched from the outside
    for x in range(x_lo, x_hi):
        for y in range(y_lo, y_hi):
            for z in range(z_lo, z_hi):
                if (x, y, z) not in seen:
                    vs_filled.add((x, y, z))
    #print("Droplet before filling:")
    #pprint_droplet(vs)
    #print("Droplet after filling:")
    #pprint_droplet(vs_filled)
    
    # Get the result using part 1!
    exposed = exposed_faces(vs_filled)

    print("Part 2 result:")
    print(f"Total surface area exposed to outside air: {exposed}")


def exposed_faces(vs):
    offsets = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}
    backwards_offs = {"x": (-1, 0, 0), "y": (0, -1, 0), "z": (0, 0, -1)}
    def is_covered(p1, off):
        p2 = tuple(x1 + o1 for (x1, o1) in zip(p1, off))
        return p2 in vs
    
    exposed = 0

    for (axis, off) in offsets.items():
        # Sweep forwards, get exposed faces
        exposed += sum(1 for v in vs if not is_covered(v, off))
        # Sweep backwards, get exposed faces
        exposed += sum(1 for v in vs if not is_covered(v, backwards_offs[axis]))
    return exposed
    
def get_axis(axis):
    match axis:
        case "x":
            ind = 0
        case "y":
            ind = 1
        case "z":
            ind = 2
    return lambda c: c[ind]

def parse_voxel(line):
    return tuple(coord for coord in map(int, line.split(",")))

def pprint_droplet(droplet):
    v_xs = sorted(map(get_axis("x"), droplet))
    v_ys = sorted(map(get_axis("y"), droplet))
    v_zs = sorted(map(get_axis("z"), droplet))
    for z in range(v_zs[0], v_zs[-1] + 1):
        print(f"z={z}")
        for y in range(v_ys[0], v_ys[-1] + 1):
            for x in range(v_xs[0], v_xs[-1] + 1):
                print("#" if (x, y, z) in droplet else ".", end="")
            print(y)
        print(f"{v_xs[0]} - {v_xs[-1]}")

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    lines = data.strip().split("\n")
    voxels = [parse_voxel(l) for l in lines]
    
    #pprint_droplet(voxels)
    part1(voxels)
    print("--------")
    part2(voxels)
    