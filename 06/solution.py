#!/usr/bin/env python3

import sys


class InputParser:

    path: str

    def __init__(self, path) -> None:
        self.path = path

    def parse(self, marker_len):
        with open(self.path, "r") as infile:
            contents = infile.read()
        contents = contents.strip()
        str_len = len(contents)
        for i in range(str_len - marker_len - 1):
            excerpt = contents[i:i+marker_len]
            excerpt_set = set(excerpt)
            if len(excerpt_set) == marker_len:
                return i + marker_len
        return -1


if __name__ == "__main__":
    input_path = sys.argv[1]
    parser = InputParser(input_path,)
    # Part 1
    result = parser.parse(marker_len=4)
    print("Part 1:", result)
    # Part 2
    result = parser.parse(marker_len=14)
    print("Part 2:", result)
