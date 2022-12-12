#!/usr/bin/env python3

from collections.abc import Collection, MutableSet
from functools import reduce
import sys

class Rucksack:

    section_1: MutableSet[str]

    section_2: MutableSet[str]

    def __init__(self, *sections: Collection[str]):
        self.sections = [set(s) for s in sections]

    def find_common_items(self) -> Collection[str]:
        intersect = reduce(set.intersection, self.sections)
        return list(intersect)

    def calc_priority(self, item: str):
        priority = None
        assert len(item) == 1
        if item.isupper():
            priority = ord(item) - ord("A") + 1 + 26
        elif item.islower():
            priority = ord(item) - ord("a") + 1
        return priority

    def calc_priority_of_common_items(self):
        common_items = self.find_common_items()
        return sum(self.calc_priority(x) for x in common_items)


class InputParser:

    path: str

    def __init__(self, path) -> None:
        self.path = path

    def parse_1(self):
        rucksacks = []
        with open(self.path, "r") as infile:
            for line in infile:
                line = line.strip()
                halfway_point = len(line) // 2
                half_1, half_2 = line[:halfway_point], line[halfway_point:]
                rucksack = Rucksack(half_1, half_2)
                rucksacks.append(rucksack)
        return rucksacks

    def parse_2(self):
        rucksacks = []
        with open(self.path, "r") as infile:
            triplet = []
            for line in infile:
                line = line.strip()
                triplet.append(line)
                if len(triplet) == 3:
                    rucksack = Rucksack(*triplet)
                    rucksacks.append(rucksack)
                    triplet = []
        return rucksacks


if __name__ == "__main__":
    input_path = sys.argv[1]
    parser = InputParser(input_path)
    # Part 1
    rucksacks = parser.parse_1()
    priorities = sum(r.calc_priority_of_common_items() for r in rucksacks)
    print("Part 1:", priorities)
    # Part 2
    rucksacks = parser.parse_2()
    priorities = sum(r.calc_priority_of_common_items() for r in rucksacks)
    print("Part 2:", priorities)
