#!/usr/bin/env python3

from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
import re
import sys

class Stacks:

    stacks: Mapping[int, Sequence]

    def __init__(self, stacks):
        self.stacks = dict()
        for num, sequence in stacks.items():
            self.stacks[num] = list(sequence)

    def move_1(self, num, source, target):
        for _ in range(num):
            crate = self.stacks[source].pop()
            self.stacks[target].append(crate)

    def move_2(self, num, source, target):
        crates = self.stacks[source][-num:]
        self.stacks[source] = self.stacks[source][:-num]
        self.stacks[target].extend(crates)

    def get_top_crates(self):
        top_crates = []
        for stack in self.stacks.values():
            top_crate = stack[-1]
            top_crates.append(top_crate)
        return "".join(top_crates)


class InputParser:

    path: Path

    def __init__(self, path):
        self.path = path

    def parse_stacks(self, text):
        stacks_dict = defaultdict(list)
        lines = text.split("\n")
        # Remove stack numbers
        lines = lines[:-1]
        for line in reversed(lines):
            # Remove irrelevant spaces and special characters
            line = line[1::4]
            for stack_id, character in enumerate(line, start=1):
                if character.strip():
                    stacks_dict[stack_id].append(character)
        return Stacks(stacks_dict)

    def parse_moves(self, stacks, text, move_mode):
        text = text.strip()
        for line in text.split("\n"):
            num, source, target = re.findall(r"\d+", line)
            num, source, target = int(num), int(source), int(target)
            if move_mode == 1:
                stacks.move_1(num, source, target)
            elif move_mode == 2:
                stacks.move_2(num, source, target)
        return stacks

    def parse(self, move_mode):
        with open(self.path, "r") as infile:
            contents = infile.read()
        stacks_text, moves_text = contents.split("\n\n")
        stacks = self.parse_stacks(stacks_text)
        stacks = self.parse_moves(stacks, moves_text, move_mode)
        return stacks


if __name__ == "__main__":
    input_path = sys.argv[1]
    # Part 1
    parser_1 = InputParser(input_path)
    stacks_1 = parser_1.parse(move_mode=1)
    top_crates_1 = stacks_1.get_top_crates()
    print("Part 1:", top_crates_1)
    # Part 2
    parser_2 = InputParser(input_path)
    stacks_2 = parser_2.parse(move_mode=2)
    top_crates_2 = stacks_2.get_top_crates()
    print("Part 2:", top_crates_2)
