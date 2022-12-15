#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence
from math import inf
import sys


class Coordinates:
    row: int
    col: int

    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col

    def get_values(self):
        return (self.row, self.col)

    def connect(self, other: Coordinates):
        path = [self]
        if self.row == other.row:
            row = self.row
            min_col, max_col = sorted([self.col, other.col])
            for col in range(min_col + 1, max_col):
                coordinates = Coordinates(row, col)
                path.append(coordinates)
        elif self.col == other.col:
            min_row, max_row = sorted([self.row, other.row])
            col = self.col
            for row in range(min_row + 1, max_row):
                coordinates = Coordinates(row, col)
                path.append(coordinates)
        else:
            raise ValueError("Cannot be connected by a straight line")
        path.append(other)
        return path


class Cave:
    grid: defaultdict[defaultdict[str]]
    num_sands: int

    SOLID = {"#", "o"}

    def __init__(self) -> None:
        self.height = 0
        self.grid = defaultdict(lambda: defaultdict(lambda: "."))
        self.num_sands = 0

    def add_feature(self, coordinates: Coordinates, feature: str):
        row, col = coordinates.get_values()
        self.grid[row][col] = feature

    def add_rocks(self, start: Coordinates, end: Coordinates):
        path = start.connect(end)
        for coordinates in path:
            self.add_feature(coordinates, "#")
            row, _ = coordinates.get_values()
            self.height = max(row, self.height)

    def fall(self, row, col):
        if row >= self.height:
            return None, None
        elif self.grid[row + 1][col] not in self.SOLID:
            return row + 1, col
        elif self.grid[row + 1][col - 1] not in self.SOLID:
            return row + 1, col - 1
        elif self.grid[row + 1][col + 1] not in self.SOLID:
            return row + 1, col + 1
        else:
            return row, col

    def produce_sand(self, starting_point: Coordinates):
        source_row, source_col = starting_point.get_values()
        old_row, old_col = source_row, source_col
        is_moving = True
        while is_moving:
            # print(old_row, old_col)
            row, col = self.fall(old_row, old_col)
            if row is None and col is None:
                return False
            if row == source_row and col == source_col:
                self.num_sands += 1
                return False
            if row == old_row and col == old_col:
                is_moving = False
            old_row, old_col = row, col
        ending_point = Coordinates(row, col)
        self.add_feature(ending_point, "o")
        self.num_sands += 1
        return True

    def start_sand_flow(self, starting_point: Coordinates):
        self.add_feature(starting_point, "+")
        sand_on_rock = True
        while sand_on_rock:
            sand_on_rock = self.produce_sand(starting_point)

    def add_floor(self, distance: int):
        floor_height = self.height + distance
        self.grid[floor_height] = defaultdict(lambda: "#")
        self.height = floor_height

    def print(self):
        minimums = [min(row.keys(), default=inf) for row in self.grid.values()]
        maximums = [max(row.keys(), default=-inf) for row in self.grid.values()]
        start = min(minimums)
        end = max(maximums)
        for row_index in range(self.height + 1):
            row_list = []
            for col_index in range(start, end + 1):
                col = self.grid[row_index][col_index]
                row_list.append(col)
            row_str = "".join(row_list)
            print(f"{row_index}\t{row_str}")


class InputParser:
    path: str

    def __init__(self, path) -> None:
        self.path = path

    def parse(self, cave: Cave):
        with open(self.path, "r") as infile:
            for line in infile:
                line = line.strip()
                previous_coords = None
                for points in line.split(" -> "):
                    col, row = [int(x) for x in points.split(",")]
                    coordinates = Coordinates(row, col)
                    if previous_coords:
                        cave.add_rocks(previous_coords, coordinates)
                    previous_coords = coordinates


if __name__ == "__main__":
    input_path = sys.argv[1]
    parser = InputParser(input_path)
    # Part 1
    cave_1 = Cave()
    result = parser.parse(cave_1)
    cave_1.start_sand_flow(Coordinates(0, 500))
    print("Part 1:", cave_1.num_sands, end="\n\n")
    cave_1.print()
    print()
    # Part 2
    cave_2 = Cave()
    result = parser.parse(cave_2)
    cave_2.add_floor(2)
    cave_2.start_sand_flow(Coordinates(0, 500))
    print("Part 2:", cave_2.num_sands, end="\n\n")
    cave_2.print()
