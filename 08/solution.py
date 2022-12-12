#!/usr/bin/env python3

from collections.abc import Sequence
from pathlib import Path
import sys

import numpy as np


class Forest:

    grid: np.array

    def __init__(self, rows: Sequence[Sequence[int]]):
        self.grid = np.array(rows)

    def find_visible_trees(self):
        visible_trees = []
        nrows, ncols = self.grid.shape
        for row in range(nrows):
            for col in range(ncols):
                if self.is_tree_visible(row, col):
                    visible_trees.append((row, col))
        return visible_trees

    def _generate_views(self, row, col, inward=True):
        views = [
            self.grid[ :row      , col:col+1 ],  # Top view
            self.grid[ row+1:    , col:col+1 ],  # Bottom view
            self.grid[ row:row+1 , :col ],       # Left view
            self.grid[ row:row+1 , col+1: ],     # Right view
        ]
        # Reverse bottom and right views for inward direction
        views[1] = np.flip(views[1])
        views[3] = np.flip(views[3])
        # print([list(v.flatten()) for v in views])
        return views

    def is_tree_visible(self, row, col):
        # Get tree height
        tree_height = self.grid[row, col]
        # Retrieve tree heights from each view
        views = self._generate_views(row, col)
        # Flatten to simple 1D arrays
        views = [v.flatten() for v in views]
        # Add a zero for edge (helps max() for empty views)
        views = [np.append(v, -1) for v in views]
        # Take the maximum of each view
        view_maxs = [np.max(v) for v in views]
        # Take the minimum of all view maxs
        min_view_max = np.min(view_maxs)
        # Compute whether the tree is visible
        return tree_height > min_view_max

    def calc_scenic_score(self, row, col):
        # Get tree height
        tree_height = self.grid[row, col]
        # Retrieve tree heights from each view
        views = self._generate_views(row, col)
        # Flatten to simple 1D arrays
        views = [v.flatten() for v in views]
        # Flip (reverse) the arrays for traversal
        views = [np.flip(v) for v in views]
        # Iterate over the views to find viewing distance
        scenic_score = 1
        for view in views:
            if len(view) == 0:
                scenic_score *= 0
            for dist, height in enumerate(view, 1):
                if height >= tree_height or dist == len(view):
                    scenic_score *= dist
                    break
        return scenic_score

    def calc_scenic_scores(self):
        scenic_scores = []
        nrows, ncols = self.grid.shape
        for row in range(nrows):
            for col in range(ncols):
                scenic_score = self.calc_scenic_score(row, col)
                scenic_scores.append(scenic_score)
        return scenic_scores


class InputParser:

    path: Path

    def __init__(self, path):
        self.path = path

    def parse(self):
        rows = []
        with open(self.path, "r") as infile:
            for line in infile:
                line = line.strip()
                row = [int(x) for x in line]
                rows.append(row)
        return Forest(rows)


if __name__ == "__main__":
    input_path = Path(sys.argv[1])
    # Part 1
    parser = InputParser(input_path)
    forest = parser.parse()
    visible_trees = forest.find_visible_trees()
    print("Part 1:", len(visible_trees))
    scenic_scores = forest.calc_scenic_scores()
    print("Part 2:", max(scenic_scores))
