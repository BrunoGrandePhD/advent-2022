#!/usr/bin/env python3

from __future__ import annotations

from ast import literal_eval
from collections.abc import Sequence

import sys


class Packet:
    contents: Sequence[int | Sequence]

    def __init__(self, contents) -> None:
        self.contents = contents

    def __repr__(self):
        return repr(self.contents)

    def __lt__(self, other: Packet):
        return self.compare(self.contents, other.contents) == -1

    def __gt__(self, other: Packet):
        return self.compare(self.contents, other.contents) == 1

    def __le__(self, other: Packet):
        return self.compare(self.contents, other.contents) <= 0

    def __ge__(self, other: Packet):
        return self.compare(self.contents, other.contents) >= 0

    def __eq__(self, other: Packet):
        return self.compare(self.contents, other.contents) == 0

    @classmethod
    def compare(cls, left, right):
        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return -1
            elif left > right:
                return 1
            else:
                return 0
        if isinstance(left, int):
            left = [left]
        if isinstance(right, int):
            right = [right]
        for index in range(len(left)):
            if index >= len(right):
                return 1
            comparison = cls.compare(left[index], right[index])
            # print(left[index], " ? ", right[index], " = ", comparison)
            if comparison != 0:
                return comparison
        if len(left) < len(right):
            return -1
        return 0


class InputParser:

    path: str

    def __init__(self, path) -> None:
        self.path = path

    def parse(self):
        packets = []
        with open(self.path, "r") as infile:
            contents = infile.read()
        contents = contents.strip()
        pairs = contents.split("\n\n")
        for pair in pairs:
            raw_first, raw_second = pair.split("\n")
            first, second = literal_eval(raw_first), literal_eval(raw_second)
            packet_1, packet_2 = Packet(first), Packet(second)
            packets.append((packet_1, packet_2))
        return packets


if __name__ == "__main__":
    input_path = sys.argv[1]
    parser = InputParser(input_path)
    # Part 1
    packets = parser.parse()
    comparisons = [p1 <= p2 for p1, p2 in packets]
    indices = [index for index, comp in enumerate(comparisons, start=1) if comp]
    print("Part 1:", sum(indices))
    # Part 2
    # Source: https://stackoverflow.com/a/952952
    flat_packets = [item for sublist in packets for item in sublist]
    sentinel_1 = Packet([[2]])
    sentinel_2 = Packet([[6]])
    flat_packets.extend([sentinel_1, sentinel_2])
    ordered = list(sorted(flat_packets))
    sentinel_1_index = ordered.index(sentinel_1) + 1
    sentinel_2_index = ordered.index(sentinel_2) + 1
    print("Part 2:", sentinel_1_index * sentinel_2_index)
