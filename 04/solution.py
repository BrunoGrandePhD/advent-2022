#!/usr/bin/env python3

from __future__ import annotations

import sys


class Range:

    start: int
    end: int

    def __init__(self, start, end):
        self.start = int(start)
        self.end = int(end)

    def is_contained_by(self, other: 'Range'):
        if self.start >= other.start and self.end <= other.end:
            return True
        return False

    def overlaps(self, other: 'Range'):
        if self.end >= other.start and self.start <= other.end:
            return True
        if self.start >= other.start and self.end <= other.end:
            return True
        if self.start <= other.start and self.end >= other.end:
            return True
        return False


class InputParser:

    path: str

    def __init__(self, path) -> None:
        self.path = path

    def parse(self):
        range_pairs = []
        with open(self.path, "r") as infile:
            for line in infile:
                line = line.strip()
                first, second = line.split(",")
                range_1 = Range(*first.split("-"))
                range_2 = Range(*second.split("-"))
                range_pairs.append((range_1, range_2))
        return range_pairs


def is_redundant(range_1, range_2):
    return range_1.is_contained_by(range_2) or range_2.is_contained_by(range_1)

def is_overlapping(range_1, range_2):
    return range_1.overlaps(range_2)


if __name__ == "__main__":
    input_path = sys.argv[1]
    parser = InputParser(input_path)
    range_pairs = parser.parse()
    # Part 1
    num_redundant_pairs = sum(is_redundant(r1, r2) for r1, r2 in range_pairs)
    print("Part 1:", num_redundant_pairs)
    # Part 2
    num_overlapping_pairs = sum(is_overlapping(r1, r2) for r1, r2 in range_pairs)
    print("Part 2:", num_overlapping_pairs)
