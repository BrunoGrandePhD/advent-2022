#!/usr/bin/env python3

from collections.abc import Collection, Mapping
import sys

import networkx


class Coordinate:
    row: int
    col: int

    def __init__(self, row, col, height) -> None:
        self.row = row
        self.col = col
        self.height = height

    def __repr__(self):
        return f"Coordinate[{self.row},{self.col},{self.height}]"


class Map:
    graph: networkx.DiGraph()

    def __init__(self) -> None:
        self.graph = networkx.DiGraph()

    def add_node(self, node: Coordinate, neighbors: Collection[Coordinate]):
        for neighbor in neighbors:
            self.graph.add_edge(node, neighbor)

    def print(self):
        print(self.graph)

    def find_shortest_path(self, start: Coordinate, end: Coordinate):
        try:
            shortest_path = networkx.shortest_path(self.graph, start, end)
        except networkx.exception.NetworkXNoPath:
            shortest_path = None
        return shortest_path

    def find_shortest_path_ever(self, end: Coordinate):
        shortest_paths = []
        for node in self.graph:
            if node.height == 0:
                shortest_path = self.find_shortest_path(node, end)
                shortest_paths.append(shortest_path)
        shortest_paths = filter(None, shortest_paths)
        shortest_paths = sorted(shortest_paths, key=lambda x: len(x))
        shortest_path_ever = shortest_paths[0]
        return shortest_path_ever


class InputParser:

    path: str
    cache: Mapping[tuple[int, int], Coordinate]

    def __init__(self, path) -> None:
        self.path = path
        self.cache = {}
        with open(self.path, "r") as infile:
            contents = infile.read()
            contents = contents.strip()
        self.grid = [list(row) for row in contents.split("\n")]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def get_coordinate(self, row_idx, col_idx):
        as_tuple = (row_idx, col_idx)
        if as_tuple in self.cache:
            return self.cache[as_tuple]
        raw_height = self.grid[row_idx][col_idx]
        if raw_height == "S":
            raw_height = "a"
        if raw_height == "E":
            raw_height = "z"
        height = ord(raw_height) - ord("a")
        coord = Coordinate(row_idx, col_idx, height)
        self.cache[as_tuple] = coord
        return coord

    def find_neighbors(self, row_idx, col_idx):
        neighbors = []
        adjustments = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for adjustment in adjustments:
            row_adj, col_adj = adjustment
            adj_row_idx, adj_col_idx = row_idx + row_adj, col_idx + col_adj
            if (
                adj_row_idx >= 0
                and adj_col_idx >= 0
                and adj_row_idx < self.height
                and adj_col_idx < self.width
            ):
                neighbors.append((adj_row_idx, adj_col_idx))
        return neighbors

    def parse(self, map: Map):
        start_node = None
        end_node = None
        for row_idx, row in enumerate(self.grid):
            for col_idx, col in enumerate(row):
                neighbors = []
                current = self.get_coordinate(row_idx, col_idx)
                for adj_row_idx, adj_col_idx in self.find_neighbors(row_idx, col_idx):
                    neighbor = self.get_coordinate(adj_row_idx, adj_col_idx)
                    if neighbor.height <= current.height + 1:
                        neighbors.append(neighbor)
                map.add_node(current, neighbors)
                if col == "S":
                    start_node = current
                if col == "E":
                    end_node = current
        return start_node, end_node


if __name__ == "__main__":
    input_path = sys.argv[1]
    parser = InputParser(input_path)
    # Part 1
    map = Map()
    start, end = parser.parse(map)
    path = map.find_shortest_path(start, end)
    num_steps = len(path) - 1
    print("Part 1:", num_steps)
    # Part 2
    path = map.find_shortest_path_ever(end)
    num_steps = len(path) - 1
    print("Part 2:", num_steps)
