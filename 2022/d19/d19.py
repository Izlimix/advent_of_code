#!/usr/bin/env python3

# https://adventofcode.com/2022/day/19

import re
from collections import Counter
from functools import cache
import math
from tqdm import tqdm

# When exploring routes through a blueprint, we can trim any that don't reach material milestones in time.
# To obtain at least 1 geode we need a geode bot by the end of round 23
# e.g. In the first sample, geode bots cost 7 obsidian, so we need an obsidian bot by round 16? (wait no, we could halve this time by having 2 bots later...)
# Assuming we can build one bot of that type every turn, the minimum number of turns to get enough resources is: ...
# Let's build a bot of this type every turn. So every turn we have +1 bot (=> +1 of that resource per turn)
# Turn | Resources | Bots at end of turn
# 1  |  0 | 1
# 2  |  1 | 2
# 3  |  3 | 3
# 4  |  6 | 4
# 5  | 10 | 5
# 6  | 15 | 6
# 7  | 21 | 7
# 8  | 28 | 8
# 9  | 36 | 9
# 10 | 45 | 10
# 11 | 55 | 11
# ^ could maybe use this table to trim, since with an obsidian cost of 7, that's still looking ~5 turns ahead
# (triangle numbers)

# Easier optimisation (from reddit): Cap the max number of bots of each type as the highest cost that uses that material.
# Also, don't consider every step. Consider the next type of bot to build, and jump to the step that you build it (like with valves on day 16)

def part1(blueprints):
    # 24 minutes, 1 ore-collecting robot, 1 factory. Max number of geodes collected per blueprint?
    # We start with 1 ore-collecting bot
    total_quality = 0
    for r in tqdm(range(len(blueprints))):
        blueprint = blueprints[r]

        bots = Counter(["ore"])
        resources = Counter() # If we use a Counter here, we can just do resources + bots

        caps = dict((mat, max(robot[mat] for robot in blueprint.values())) for mat in blueprint) # We don't need to build more robots of any type than the max we can consume per minute building a new bot. 
        #milestones = get_milestones(blueprint, 1) # We need a geode bot by the time we only have 1 round remaining

        gs = geodes2(blueprint, caps, bots, resources)
        total_quality += (r + 1) * gs
    print("Part 1 result:")
    print(f"Total quality levels: {total_quality}")
    
def part2(blueprints):
    # 32 minutes, only first 3 blueprints. Multiply their geode numbers together.
    result = 1
    for r in tqdm(range(min(3, len(blueprints)))):
        blueprint = blueprints[r]
        bots = Counter(["ore"])
        resources = Counter()
        caps = dict((mat, max(robot[mat] for robot in blueprint.values())) for mat in blueprint) # We don't need to build more robots of any type than the max we can consume per minute building a new bot. 

        gs = geodes2(blueprint, caps, bots, resources, 32)
        result *= gs
    
    print("Part 2 result:")
    print(f"Product of geode values for first 3 blueprints: {result}")

def geodes2(blueprint, caps, bots, resources, rounds=24, best_gs=0):
    if rounds <= 0:
        return resources["geode"]
    
    # If there's no way we could beat the current best geodes, prune this branch.
    estimate = resources["geode"] + optimistic_resources(bots["geode"], rounds) 
    if estimate <= best_gs:
        return 0
    
    # How many geodes would we get if we just wait from now on?
    gs = resources["geode"] + bots["geode"] * rounds
    best_gs = max(best_gs, gs)

    # What's the next bot we want to make?
    for (bot_type, costs) in blueprint.items():
        # If we've met the cap for this bot, there's no point in making it.
        if bot_type != "geode" and bots[bot_type] >= caps[bot_type]:
            continue
        # If we don't have bots to harvest its materials, then we can't make it.
        if any(c not in bots for c in costs.keys()):
            continue
        # How many rounds to finish this bot?
        r = turns_to_bot(costs, resources, bots)
        if r > rounds:
            # It would take too long
            continue
        # Skip ahead to that round
        future_resources = +resources
        for _ in range(r):
            future_resources += bots
        future_resources -= costs
        gs = geodes2(blueprint, caps, bots + Counter([bot_type]), future_resources, rounds - r, best_gs)
        best_gs = max(best_gs, gs)
    
    return best_gs
    
def turns_to_bot(costs, resources, bots):
    if costs <= resources:
        return 1
    remaining = +(costs - resources)
    return 1 + max(math.ceil(remaining[m] / bots[m]) for m in remaining)

# Needs optimisation, not fast enough.
def geodes_achievable(blueprint, caps, bots, resources, rounds=24, best_so_far=0, *, milestones=None):
    if rounds <= 0:
        #print(f"Ran out of time. Returning {resources['geode']} geodes")
        #print(f"attempt {attempts}, round {rounds}, geodes {resources['geode']}. (Best: {best_so_far})")
        return resources["geode"]
    
    # If there's no way we could beat the current best geodes, prune this branch.
    estimate = resources["geode"] + optimistic_resources(bots["geode"], rounds) 
    if estimate <= best_so_far:
        print(f"Pruning branch at depth {rounds}. Best: {best_so_far}")
        #print(f"Milestones: {milestones}")
        #print(f"Bots: {bots}")
        return 0
    
    if milestones is not None:
        # If we've missed the latest turn milestones (so we can't reach geode bots in time to beat our best), then prune.
        for (material, turn) in milestones.items():
            if turn > rounds and bots[material] < 1:
                #print(f"Missed milestone {material} bot by {turn} rounds left. Pruning at depth {rounds}.")
                #print(resources)
                #print(bots)
                return 0

    # Order: 
    # 1. Decide on action and consume resources
    # 2. Existing bots mine ore
    # 3. Factory done making the bot from 1, +1 of that bot type.

    # We have 5 choices of actions
    # -> For each of the 4 bot types, if we have the resources, we can make 1 of that bot.
    # -> Or, we can wait one round and gather more resource.
    # We can encode our entire path as a 24-length string of W (wait), R (ore), C (clay), B (obsidian), G (geode)
    #  and check whether it's valid by following it~
    valid_actions = []
    for material in ["geode", "obsidian", "clay", "ore"]:
        if (material == "geode" or bots[material] < caps[material]) and resources >= blueprint[material]:
            valid_actions.append(material)
    valid_actions.append("wait")
    #print(valid_actions)

    # 2. Mine ore
    resources.update(bots) # Counter.update adds counts instead of replacing!

    current_max = resources["geode"]
    # 3. Make the bot
    for action in valid_actions:
        #print(action)
        match action:
            case "wait":
                #print("Waiting")
                gs = geodes_achievable(blueprint, caps, +bots, +resources, rounds - 1, best_so_far, milestones=milestones)
            case material:
                #print(f"Making a {material} bot")
                #resources -= blueprint[material]
                #bots[material] += 1
                gs = geodes_achievable(blueprint, caps, bots + Counter([material]), resources - Counter(blueprint[material]), rounds - 1, best_so_far, milestones=milestones)
        current_max = max(current_max, gs)
        if gs > best_so_far:
            best_so_far = gs
            if milestones is not None:
                # Update milestones if the geode milestone changed
                geode_milestone = milestone_round(best_so_far)
                if geode_milestone is not None and milestones["geode"] < geode_milestone:
                    milestones.update(get_milestones(blueprint, geode_milestone))
    
    return current_max

# Untested~
def robots_from_instructions(blueprint, instructions):
    # A 23-long instruction
    assert len(instructions) == 23
    bots = Counter(["ore"])
    resources = Counter()
    mat_lookup = {
        "R": "ore",
        "C": "clay",
        "B": "obsidian",
        "G": "geode"
    }
    for action in instructions:
        turn_start_resources = resources.copy()
        resources += bots
        match action:
            case "W":
                # Wait
                pass
            case material:
                mat = mat_lookup[material]
                cost = Counter(blueprint([mat]))
                assert turn_start_resources >= cost
                resources -= cost
    print(f"Ran {instructions}")
    print(f"Final geodes: {resources['geode']}")

def get_milestones(blueprint, geode_round_target):
    print(f"Finding milestones for {blueprint}")
    milestones = {"geode": geode_round_target}
    materials = ["geode", "obsidian", "clay"] #, "ore"]
    for (bot_type, mat) in zip(materials, materials[1:]):
        mat_required = blueprint[bot_type][mat]
        turns_advance = milestone_round(mat_required)
        if turns_advance is None:
            turns_advance = 0
        milestones[mat] = milestones[bot_type] + turns_advance
    print(f"New milestones: {milestones}")
    return milestones

@cache
def milestone_round(n):
    # The first triangle number that's >= n
    for i in range(1, n):
        if summation(i) >= n:
            return i

@cache
def optimistic_resources(bots, rounds):
    return bots * rounds + summation(rounds - 1)

@cache
def summation(n):
    # Sum from 1 to N. Triangular numbers~
    return n * (n + 1) / 2
    
def parse_blueprints(lines):
    # e.g. Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 7 clay. Each geode robot costs 2 ore and 19 obsidian.
    robot_pattern = re.compile(r"Each ([a-zA-Z]+) robot costs (.+?)\.")
    cost_pattern = re.compile(r"(\d+) ([a-zA-Z]+)")
    blueprints = []
    for l in lines:
        blueprint = dict()
        for (robot_type, cost_data) in robot_pattern.findall(l):
            cost = Counter()
            for (n, material) in cost_pattern.findall(cost_data):
                cost[material] = int(n)
            blueprint[robot_type] = cost
        blueprints.append(blueprint)
    return blueprints

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    lines = data.strip().split("\n")
    blueprints = parse_blueprints(lines)
    print("Done parsing!")

    part1(blueprints)
    print("--------")
    part2(blueprints)
    