#!/usr/bin/env python3

import re
import operator
import math
from collections import deque
from dataclasses import dataclass, field
from typing import Callable

# https://adventofcode.com/2023/day/19

"""
Could use a lot of cleanup, but we got an answer eventually
"""

ops = {
    ">": operator.gt,
    "<": operator.lt
}

def part1():
    # Using global parts and workflows
    accepted = []
    for p in parts:
        r = run_workflow(workflows["in"], p)
        if r:
            accepted.append(p)

    print(f"{len(accepted)=}")
    print(f"Part 1: {sum(sum(p.values()) for p in accepted)=}")

def part2():
    # Count distinct combinations of ratings that will be accepted
    # Every time we meet a workflow step, split into 2 branches of accept/reject?
    
    # We can do this top-down or bottom-up (which makes more sense)
    # from bottom: Find all the A steps, and figure out how to get there
    # -> To reach a step, all prev steps have to fail, and we need to have gotten to this workflow from a previous step
    # -> if we reach a contradiction/non-overlapping range, there's no chance

    # When we find a range of values for each rating, the distinct combinations = * (lengths of each of xmas)
    # -> assuming that none of the ranges overlap... (gah)
    # Top-down should ensure that our ranges don't overlap

    # Part ranges of {xmas: (1, 4000 incl)}, along with which workflow to split them on next

    parts = deque()
    parts.append(("in", dict(zip("xmas", [(1, 4000) for _ in range(4)]))))
    accepted_ranges = []
    while parts:
        wf, p = parts.pop()
        match wf:
            case "R":
                continue
            case "A":
                accepted_ranges.append(p)
            case _:
                wf = workflows[wf]
                # Split this range on the specified workflow, and add them to the todo list
                parts.extend(split_workflow(wf, p))
    # print(f"{accepted_ranges=}")
    out = sum(math.prod(hi - lo + 1 for (lo, hi) in p.values()) for p in accepted_ranges)
    print(f"Part 2: {out=}")


# Could use a dataclass or sth else, but this also lets us sum the ratings of the part
# A dict wouldn't be bad though -> would make getting the attr easier
# Part = namedtuple("Part", ["x", "m", "a", "s"])

@dataclass
class Rule:
    target: str
    rating: str=field(default=None)
    op_s: str=field(default=None)
    op: Callable=field(default=None)
    v: int=field(default=None)
    
    def run(self, part: dict):
        # Would be nice to raise an Exception on accept/reject instead
        if self.op is None or self.op(part[self.rating], self.v):
            # Default or passed test
            return self.target
        return None
    
    def split_range(self, part_range: dict):
        if self.op is None:
            # Default
            return [(self.target, part_range)]
        rating_lo, rating_hi = part_range[self.rating]
        ps = []
        if self.op_s == ">":
            # Failed test
            p_lo = part_range.copy()
            p_lo[self.rating] = (rating_lo, self.v)
            ps.append((None, p_lo))
            # Passed test
            p_hi = part_range.copy()
            p_hi[self.rating] = (self.v + 1, rating_hi)
            ps.append((self.target, p_hi))
        elif self.op_s == "<":
            # Passed test
            p_lo = part_range.copy()
            p_lo[self.rating] = (rating_lo, self.v - 1)
            ps.append((self.target, p_lo))
            # Failed test
            p_hi = part_range.copy()
            p_hi[self.rating] = (self.v, rating_hi)
            ps.append((None, p_hi))
        else:
            raise Exception(f"Unknown op {self.op_s} in {self} when splitting {part_range=}")
        # Cleanup: remove any impossible/empty ranges (lo > hi)
        ps = [(target, p) for (target, p) in ps if not is_empty_range(p)]
        return ps
    
def run_workflow(workflow: list[Rule], part: dict):
    for w in workflow:
        out = w.run(part)
        match out:
            case None:
                continue
            case "A":
                return True
            case "R":
                return False
            case _:
                return run_workflow(workflows[out], part)
    raise Exception(f"Ran out of workflow steps. {part=}, {workflow=}")

def split_workflow(workflow: list[Rule], part_range: dict):
    # For every rule in this workflow, get the result if part succeeds at it, or fails and continues to the next rule
    # On fail, update part_range before continuing
    # Return list of all (non-empty) part ranges
    out = []
    for w in workflow:
        ps = w.split_range(part_range)
        if not ps:
            # All splits empty, somehow. We're done splitting!
            print("ps empty, done splitting workflow")
            break
        for (target, p) in ps:
            if target is None:
                part_range = p
            else:
                out.append((target, p))
    return out

def is_empty_range(part_range):
    return any(lo > hi for (lo, hi) in part_range.values())

def parse_workflows(ws: str) -> dict:
    workflows = dict()
    workflow_pat = re.compile(r"^([a-z]+)\{(.+)\}$")
    rule_pat = re.compile(r"([xmas])([><])(\d+):([a-zA-Z]+)")

    for l in ws.split("\n"):
        wf_id, wf_steps = workflow_pat.match(l).groups()
        rules = []
        # Parse all steps
        for step in wf_steps.split(","):
            m = rule_pat.match(step)
            if m:
                # Conditional step
                rating, op, v, target = m.groups()
                
                rules.append(Rule(target, rating, op, ops[op], int(v)))
            else:
                # Default step
                target = step
                rules.append(Rule(target))
        # Make a workflow and add to the dict
        workflows[wf_id] = rules

    return workflows

def parse_parts(ps: str) -> list[dict]:
    part_pat = re.compile(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}")  # Could make this more flexible, but input's consistent
    parts = []
    for l in ps.split("\n"):
        m = part_pat.match(l)
        p = dict(zip("xmas", map(int, m.groups())))
        parts.append(p)
    return parts


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip() 
    
    workflow_data, part_data = data.split("\n\n")
    # Global workflows and parts (hope the values don't need to be modified)
    workflows = parse_workflows(workflow_data)
    parts = parse_parts(part_data)
    
    part1()
    print("--------")
    part2()
    