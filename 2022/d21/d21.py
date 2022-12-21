#!/usr/bin/env python3

# https://adventofcode.com/2022/day/21

import re
import operator

def part1(monkeys):
    root = monkeys["root"].yell(monkeys)
    print("Part 1 result:")
    print(f"Root yells {root}")

def part2(monkeys):
    # The root checks for equality (it needs to pass)
    monkeys["root"].op = lambda v1, v2: (v1, v2)
    monkeys["humn"].value = 1j # imaginary j stands in for some unknown x. This won't work if the monkeys multiply j*j=-1  

    # You are humn, what number do you need to yell so the equality passes?
    root = monkeys["root"].yell(monkeys)
    print("Part 2 result:")
    print(f"Root yells {root} should be equal")
    # Solve simultaneous equations
    diff = (root[0] - root[1])
    real, imag = diff.real, diff.imag
    print(f"You need to shout {int(real / (-imag))}")

class Monkey:
    def __init__(self, name, value=None, op=None, wait1=None, wait2=None):
        self.name = name
        self.value = value
        self.op = op
        self.wait1 = wait1
        self.wait2 = wait2
        
    def yell(self, monkeys):
        if self.value is None:
            self.value = self.op(monkeys[self.wait1].yell(monkeys), monkeys[self.wait2].yell(monkeys))
        return self.value

def parse_monkeys(lines):
    name_pattern = re.compile(r"^([a-z]{4}): (.+)$")
    op_pattern = re.compile(r"([a-z]{4}) ([+\-*/]) ([a-z]{4})")
    digit_pattern = re.compile(r"\d+")
    operations = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv
    }
    
    monkeys = dict()
    for l in lines:
        m_name = name_pattern.fullmatch(l)
        name, yells = m_name.groups()
        m_op = op_pattern.match(yells)
        if m_op:
            # Operation monkey
            (wait1, op, wait2) = m_op.groups()
            op = operations[op]
            monkeys[name] = Monkey(name, op=op, wait1=wait1, wait2=wait2)
        else:
            # Constant monkey
            v = int(digit_pattern.match(yells).group(0))
            monkeys[name] = Monkey(name, value=v)
    return monkeys


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    monkeys = parse_monkeys(data.strip().split("\n"))
    
    part1(monkeys)
    print("--------")
    part2(parse_monkeys(data.strip().split("\n"))) # Each monkey remembers what it yelled, so get a fresh copy
    