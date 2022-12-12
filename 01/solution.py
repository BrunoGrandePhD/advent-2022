#!/usr/bin/env python3

from math import inf
from pathlib import Path
import sys
from collections.abc import Collection


class Elf:

    food_items: Collection[int]

    def __init__(self, food_items) -> None:
        self.food_items = food_items
        self.total_cals = self.calc_total_calories()

    def calc_total_calories(self):
        return sum(self.food_items)


class ElfCohort:

    elves: Collection[Elf]

    def __init__(self, elves=None) -> None:
        self.elves = elves or []

    def add_elf(self, elf: Elf):
        self.elves.append(elf)

    def find_elves_with_most_calories(self, n: int = 1):
        ranked = sorted(self.elves, key=lambda x: x.total_cals, reverse=True)
        return ranked[:n]


class CohortParser:

    path: Path

    def __init__(self, path):
        self.path = path

    def parse(self):
        with open(self.path, "r") as infile:
            contents = infile.read()
        blocks = contents.split("\n\n")
        cohort = ElfCohort()
        for block in blocks:
            block = block.strip()
            items = block.split("\n")
            items = [int(i) for i in items]
            elf = Elf(items)
            cohort.add_elf(elf)
        return cohort


if __name__ == "__main__":
    input_path = Path(sys.argv[1])
    parser = CohortParser(input_path)
    cohort = parser.parse()
    most_calories_elves = cohort.find_elves_with_most_calories(n=3)
    most_calories_nums = [e.total_cals for e in most_calories_elves]
    print("Part 1:", most_calories_nums[0])
    print("Part 2:", sum(most_calories_nums))
