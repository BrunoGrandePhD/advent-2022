#!/usr/bin/env python3

from __future__ import annotations

from collections import deque, OrderedDict
from collections.abc import Sequence, Callable, Mapping
from math import lcm
import re
import sys


class Item:
    worry: int

    def __init__(self, initial_worry) -> None:
        self.worry = initial_worry

    def __repr__(self):
        return f"Item<{self.worry}>"

    def change_worry(self, callable):
        new_worry = callable(self.worry)
        self.worry = new_worry


class Monkey:
    troop: Troop
    items: deque[Item]
    operation: Callable[[int], int]
    relieve: Callable[[int], int]
    test: Callable[[int], int]
    n_inspections = int

    def __init__(self, troop, starting_items: Sequence[Item]) -> None:
        self.troop = troop
        self.items = deque(starting_items)
        self.operation = lambda x: x
        self.relieve = lambda x: x
        self.test = lambda x: x
        self.n_inspections = 0

    def __repr__(self):
        items = list(self.items)
        items_str = ", ".join(str(item) for item in items)
        return f"Monkey[{items_str}]"

    def update_callables(self, operation, relieve, test):
        self.operation = operation
        self.relieve = relieve
        self.test = test

    def inspect_next_item(self):
        next_item = self.items[0]
        next_item.change_worry(self.operation)
        self.n_inspections += 1

    def pause_with_next_item(self):
        next_item = self.items[0]
        next_item.change_worry(self.relieve)

    def throw_next_item(self):
        next_item = self.items.popleft()
        new_monkey = self.test(next_item.worry)
        self.troop.throw_item(next_item, new_monkey)

    def catch_item(self, item: Item):
        self.items.append(item)

    def start_turn(self):
        while self.items:
            self.inspect_next_item()
            self.pause_with_next_item()
            self.throw_next_item()
            # self.troop.print()


class Troop:
    monkeys: Mapping[int, Monkey]

    def __init__(self) -> None:
        self.monkeys = OrderedDict()

    def add_monkey(self, monkey_id: int, items: Sequence[Item]) -> Monkey:
        monkey = Monkey(self, items)
        self.monkeys[monkey_id] = monkey
        return monkey

    def throw_item(self, item: Item, target: int):
        target_monkey = self.monkeys[target]
        target_monkey.catch_item(item)

    def print(self):
        print("Monkey Troop:")
        for monkey_id, monkey in self.monkeys.items():
            print(f"  {monkey_id}: {monkey}")

    def start_round(self):
        for monkey in self.monkeys.values():
            monkey.start_turn()

    def start_rounds(self, round_count):
        for _ in range(round_count):
            self.start_round()
            self.print_inspection_report

    def print_inspection_report(self):
        print("Monkey Troop - Inspection Report:")
        for monkey_id, monkey in self.monkeys.items():
            print(f"  {monkey_id}: {monkey.n_inspections}")

    def generate_inspection_report(self):
        report = {}
        for monkey_id, monkey in self.monkeys.items():
            report[monkey_id] = monkey.n_inspections
        return report

    def calc_monkey_business(self):
        report = self.generate_inspection_report()
        ordered_monkeys = sorted(report.values(), reverse=True)
        monkey_1st, monkey_2nd = ordered_monkeys[0:2]
        monkey_business = monkey_1st * monkey_2nd
        return monkey_business


class InputParser:

    path: str

    def __init__(self, path, relieve_fn) -> None:
        self.path = path
        self.relieve_fn = relieve_fn
        self.divisors = []

    @staticmethod
    def generate_test_callable(raw_test, raw_if_true, raw_if_false):
        raw_test = int(raw_test)
        raw_if_true = int(raw_if_true)
        raw_if_false = int(raw_if_false)

        def _test(x):
            divisor = int(raw_test)
            if (x - divisor * x) % divisor == 0:
                return int(raw_if_true)
            else:
                return int(raw_if_false)

        return _test

    def parse_monkey_line(self, line):
        line_monkey_id = line
        raw_monkey_id = re.findall(r"\d+", line_monkey_id)[0]
        monkey_id = int(raw_monkey_id)
        return monkey_id

    def parse_starting_items_line(self, line):
        line_items = line
        raw_items = re.findall(r"\d+", line_items)
        items = [Item(int(item)) for item in raw_items]
        return items

    def parse_operation_line(self, line):
        line_operation = line
        raw_operation = line_operation.split(" = ")[1]
        lambda_str = f"lambda old: {raw_operation}"
        operation = eval(lambda_str)
        return operation

    def parse_test_lines(self, lines):
        raw_test = re.findall(r"\d+", lines[0])[0]
        raw_if_true = re.findall(r"\d+", lines[1])[0]
        raw_if_false = re.findall(r"\d+", lines[2])[0]
        self.divisors.append(int(raw_test))
        test = self.generate_test_callable(raw_test, raw_if_true, raw_if_false)
        return test

    def parse_block(self, block: str, troop: Troop):
        lines = [s.strip() for s in block.split("\n")]
        monkey_id = self.parse_monkey_line(lines[0])
        items = self.parse_starting_items_line(lines[1])
        test = self.parse_operation_line(lines[2])
        operation = self.parse_test_lines(lines[3:])
        monkey = troop.add_monkey(monkey_id, items)
        monkey.update_callables(test, self.relieve_fn, operation)

    def parse(self, troop: Troop):
        with open(self.path, "r") as infile:
            contents = infile.read()
        contents = contents.strip()
        blocks = contents.split("\n\n")
        for block in blocks:
            self.parse_block(block, troop)
        least_common_multiple = lcm(*self.divisors)
        for monkey in troop.monkeys.values():
            monkey.relieve = lambda x: x % least_common_multiple


if __name__ == "__main__":
    input_path = sys.argv[1]
    # Part 1
    parser = InputParser(input_path, lambda x: x // 3)
    troop = Troop()
    parser.parse(troop)
    troop.start_rounds(20)
    monkey_business = troop.calc_monkey_business()
    print(f"Part 1: {monkey_business}")
    # Part 2
    parser = InputParser(input_path, lambda x: x)
    troop = Troop()
    parser.parse(troop)
    troop.start_rounds(10000)
    monkey_business = troop.calc_monkey_business()
    print(f"Part 2: {monkey_business}")
