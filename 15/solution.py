#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict, Counter
from collections.abc import Sequence, Mapping
from math import inf
import re
from string import ascii_uppercase
import sys


EMPTY: str = "."
SENSOR: str = "S"
BEACON: str = "B"
SIGNAL: str = "#"


class Coordinates:
    row: int
    col: int

    def __init__(self, row, col, data=None) -> None:
        self.row = row
        self.col = col
        self.data = data or {}

    def get_values(self):
        return (self.row, self.col)

    def calc_manhattan_distance(self, other):
        return abs(self.row - other.row) + abs(self.col - other.col)

    def add_data(self, **kwargs):
        self.data.update(kwargs)

    def get_data(self, key):
        return self.data.get(key)


class Cave:
    min_row: int
    max_row: int
    min_col: int
    max_col: int
    grid: Mapping[Mapping[str]]
    adj_cache: Mapping[Sequence[int]]
    sensors: Sequence[Coordinates]

    def __init__(self) -> None:
        self.min_row = 0
        self.max_row = 0
        self.min_col = 0
        self.max_col = 0
        self.adj_cache = dict()
        self.sensors = []
        self.grid = defaultdict(lambda: defaultdict(lambda: EMPTY))

    def add_feature(self, coordinates: Coordinates, feature: str, overwrite=False):
        row, col = coordinates.get_values()
        if self.grid[row][col] == EMPTY or overwrite:
            self.grid[row][col] = feature
            self.min_row = min(self.min_row, row)
            self.max_row = max(self.max_row, row)
            self.min_col = min(self.min_col, col)
            self.max_col = max(self.max_col, col)

    def generate_adjustments(self, distance: int):
        if distance in self.adj_cache:
            return self.adj_cache[distance]
        adjustments = set()
        sign_combos = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        if distance == 0:
            self.adj_cache[distance] = adjustments
            return adjustments
        for row_adj in range(distance + 1):
            delta = distance - row_adj
            for row_sign, col_sign in sign_combos:
                adjustment = (row_adj * row_sign, delta * col_sign)
                adjustments.add(adjustment)
        all_adjustments = adjustments | self.generate_adjustments(distance - 1)
        self.adj_cache[distance] = all_adjustments
        return all_adjustments

    def generate_coords_within_distance(self, coordinates: Coordinates, distance: int):
        all_coordinates = set()
        row, col = coordinates.get_values()
        # print(row, col, distance)
        adjustments = self.generate_adjustments(distance)
        for row_adj, col_adj in adjustments:
            # print(row + row_adj, col + col_adj)
            coords = Coordinates(row + row_adj, col + col_adj)
            all_coordinates.add(coords)
        return all_coordinates

    def generate_coords_for_row(
        self, coordinates: Coordinates, distance: int, query_row: int
    ):
        result = set()
        _, source_col = coordinates.get_values()
        target_row, target_col = query_row, source_col
        increment = 0
        direction = -1
        cursor = target_col
        num_strikes = 0
        while num_strikes <= 3:
            signal_coords = Coordinates(target_row, cursor)
            signal_dist = signal_coords.calc_manhattan_distance(coordinates)
            if signal_dist <= distance:
                result.add(signal_coords)
            else:
                num_strikes += 1
            if direction == 1:
                direction = -1
            elif direction == -1:
                increment += 1
                direction = 1
            cursor = target_col + increment * direction
        return result

    def generate_coords_for_row_v2(
        self, coordinates: Coordinates, max_distance: int, query_row: int
    ):
        result = set()
        _, source_col = coordinates.get_values()
        target_row, target_col = query_row, source_col
        closest_coords = Coordinates(target_row, target_col)
        current_distance = closest_coords.calc_manhattan_distance(coordinates)
        # Add closest coordinate if within max distance
        if current_distance <= max_distance:
            result.add(closest_coords)
        # Add flanking coordinates if within max distance
        increment = 1
        while (current_distance + increment) <= max_distance:
            left_coords = Coordinates(target_row, target_col - increment)
            right_coords = Coordinates(target_row, target_col + increment)
            result.add(left_coords)
            result.add(right_coords)
            increment += 1
        return result

    def add_sensor(self, coordinates: Coordinates):
        self.add_feature(coordinates, SENSOR)
        self.sensors.append(coordinates)

    def add_beacon(self, coordinates: Coordinates):
        self.add_feature(coordinates, BEACON)

    def add_sensor_beacon_pair(self, sensor: Coordinates, beacon: Coordinates):
        self.add_sensor(sensor)
        self.add_beacon(beacon)
        distance = sensor.calc_manhattan_distance(beacon)
        sensor.add_data(distance=distance)

    def start_nearby_signals(self, query_row=None):
        # print(f"Number of sensors: {len(self.sensors)}")
        for index, sensor in enumerate(self.sensors):
            distance = sensor.get_data("distance")
            # print(f"Sensor index = {index} / Distance = {distance}")
            sensor_row, _ = sensor.get_values()
            lower_row, upper_row = sensor_row - distance, sensor_row + distance
            if query_row is None:
                pass
            elif query_row < lower_row or query_row > upper_row:
                continue
            signal_coords = self.generate_coords_within_distance(sensor, distance)
            for signal_coord in signal_coords:
                self.add_feature(signal_coord, SIGNAL)

    def start_signals_in_row(self, query_row):
        # print(f"Number of sensors: {len(self.sensors)}")
        for index, sensor in enumerate(self.sensors):
            # print(f"Sensor {index}")
            distance = sensor.get_data("distance")
            signal_coords = self.generate_coords_for_row_v2(sensor, distance, query_row)
            for signal_coord in signal_coords:
                self.add_feature(signal_coord, SIGNAL)

    def scan_row_v1(self, row: int):
        num_ruled_out = 0
        self.start_nearby_signals(row)
        for col in self.grid[row].values():
            if col == SIGNAL:
                num_ruled_out += 1
        return num_ruled_out

    def scan_row_v2(self, row: int):
        self.start_nearby_signals(row)
        within_range = set()
        for col in sorted(self.grid[row].keys()):
            feature = self.grid[row][col]
            if feature in {BEACON, SENSOR}:
                continue
            coords = Coordinates(row, col)
            for sensor in self.sensors:
                row_distance = coords.calc_manhattan_distance(sensor)
                beacon_distance = sensor.get_data("distance")
                if row_distance <= beacon_distance:
                    within_range.add(coords)
        return len(within_range)

    def scan_row_v3(self, row: int):
        within_range = set()
        # Scan main section
        for col in range(self.min_col, self.max_col):
            coords = Coordinates(row, col)
            is_within_range = self.check_sensors(coords)
            if is_within_range:
                within_range.add(coords)
        return len(within_range)

    def scan_row_v4(self, row_index: int):
        self.start_signals_in_row(row_index)
        row = self.grid[row_index]
        feature_counts = Counter(row.values())
        return feature_counts[SIGNAL]

    def check_sensors(self, coordinates: Coordinates):
        row, col = coordinates.get_values()
        feature = self.grid[row][col]
        if feature in {BEACON, SENSOR}:
            return False
        for sensor in self.sensors:
            row_distance = coordinates.calc_manhattan_distance(sensor)
            beacon_distance = sensor.get_data("distance")
            if row_distance <= beacon_distance:
                return True
        return False

    def find_gap(self, max_row, max_col):
        for row_index in range(max_row + 1):
            for k in self.grid[row_index].keys():
                if k < 0 or k > max_col:
                    self.grid[row_index].pop(k)
            self.start_signals_in_row(row_index)
            for col_index in range(max_col + 1):
                feature = self.grid[row_index][col_index]
                if feature == EMPTY:
                    return (row_index, col_index)
        return None

    def print(self, row: int = None):
        min_row, max_row = self.min_row, self.max_row
        if row is not None:
            min_row, max_row = row - 1, row + 1
        for row_index in range(min_row, max_row + 1):
            row_list = []
            for col_index in range(self.min_col, self.max_col + 1):
                col = self.grid[row_index][col_index]
                row_list.append(col)
            row_str = "".join(row_list)
            print(f"{row_index}\t{row_str}")


class InputParser:
    path: str

    PATTERN = re.compile(
        r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    )

    def __init__(self, path) -> None:
        self.path = path

    def parse(self, cave: Cave):
        with open(self.path, "r") as infile:
            for line in infile:
                line = line.strip()
                match = self.PATTERN.fullmatch(line)
                if match is None:
                    raise ValueError("Unexpected line format")
                match_ints = [int(group) for group in match.groups()]
                sensor_x, sensor_y, beacon_x, beacon_y = match_ints
                sensor = Coordinates(sensor_y, sensor_x)
                beacon = Coordinates(beacon_y, beacon_x)
                cave.add_sensor_beacon_pair(sensor, beacon)


if __name__ == "__main__":
    input_path = sys.argv[1]
    row_of_interest = int(sys.argv[2])
    parser = InputParser(input_path)
    # Part 1
    cave_1 = Cave()
    result_1 = parser.parse(cave_1)
    # cave_1.start_nearby_signals()
    num_ruled_out_1 = cave_1.scan_row_v4(row_of_interest)
    print(f"Part 1: {num_ruled_out_1}")
    # cave_1.print(row_of_interest)
    # cave_1.print()
    # Part 1
    cave_2 = Cave()
    result_2 = parser.parse(cave_2)
    distress_y, distress_x = cave_2.find_gap(20, 20)
    tuning_frequency = distress_x * 4000000 + distress_y
    print(f"Part 2: {tuning_frequency}")
