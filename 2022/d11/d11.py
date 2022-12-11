#!/usr/bin/env python3

# https://adventofcode.com/2022/day/11

import re
import operator
import math

def part1(monkeys):
    #pprint_monkeys(monkeys)
    for i in range(1, 21):
        for m in monkeys:
            m.inspect_items(monkeys)
        #print(f"---- After round {i} ----")
        #pprint_monkeys(monkeys)
    
    print("Part 1 result:")
    inspections = sorted((m.n_inspected for m in monkeys), reverse=True)
    monkey_business = inspections[0] * inspections[1]
    print(f"Monkey business after 20 rounds: {monkey_business}")
    
def part2(monkeys, rounds=10000):
    tests = [m.test_value for m in monkeys]
    print("Tests:")
    print(tests)
    manual_relief = math.lcm(*tests)
    product = math.prod(tests)

    print(f"LCM: {manual_relief}")
    print(f"product: {product}")
    # Hahaha they're prime! >.> This is a big number

    for i in range(1, rounds + 1):
        for m in monkeys:
            m.inspect_items(monkeys, manual_relief)
        if i % 1000 == 0 or i == 20:
            print(f"---- After round {i} ----")
            #pprint_monkeys(monkeys)
    print("Part 2 result: ")
    inspections = sorted((m.n_inspected for m in monkeys), reverse=True)
    print("Inspections:")
    print(inspections)
    monkey_business = inspections[0] * inspections[1]
    print(f"Monkey business after {rounds} rounds: {monkey_business}")


def pprint_monkeys(monkeys):
    for i in range(len(monkeys)):
        m = monkeys[i]
        print(f"Monkey {str(i)} ({m.n_inspected}): {', '.join(str(item) for item in m.items)}")

class Monkey:
    def __init__(self, items, op, test_value, target_true, target_false):
        self.items = items
        self.op = op
        self.test_value = test_value
        self.target_true = target_true
        self.target_false = target_false
        self.n_inspected = 0
        
    def inspect_items(self, monkeys, manual_relief=None):
        for worry in self.items:
            self.n_inspected += 1
            worry = self.op(worry)
            if manual_relief is None:
                worry = worry // 3 # Relief that it didn't break
            else:
                worry = worry % manual_relief
            
            if worry % self.test_value == 0:
                target = self.target_true
            else:
                target = self.target_false
            monkeys[target].items.append(worry) # Throw it to another monkey
        
        self.items = [] # This monkey's done looking at items

def parse_monkey(data):
    lines = data.split("\n")
    # The monkeys are passed in order
    op_pattern = re.compile(r"Operation: new = old ([+\-*/]) ([a-zA-Z0-9]+)")
    digit_pattern = re.compile(r"\d+")
    operations = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv
    }

    items = [int(n) for n in digit_pattern.findall(lines[1])]
    m_op = op_pattern.search(lines[2])
    op = operations[m_op.group(1)]
    op_arg2 = m_op.group(2)
    monkey_op = lambda old: op(old, old if op_arg2 == "old" else int(op_arg2))

    test_val, target_true, target_false = [int(digit_pattern.search(lines[n]).group()) for n in (3, 4, 5)]

    return Monkey(items, monkey_op, test_val, target_true, target_false)


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    monkey_data = data.strip().split("\n\n")
    # This isn't great, but eh.
    def monkeys(m_data):
        return [parse_monkey(m) for m in m_data]
    
    # Note: Once again, my original answer ended up mutating the list in part 1 before passing it to part 2.
    # Please stop doing that.
    part1(monkeys(monkey_data))
    print("--------")
    part2(monkeys(monkey_data), 10000)
    