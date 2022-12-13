#!/usr/bin/env python3

from collections.abc import Sequence
import sys


class Coordinate:
    row: int
    col: int

    def __init__(self) -> None:
        self.row = 0
        self.col = 0

    def __repr__(self):
        return f"Coordinate({self.row}, {self.col})"

    def get_distance_from(self, other, absolute=False):
        vertical_dist = self.row - other.row
        horizontal_dist = self.col - other.col
        if absolute:
            vertical_dist = abs(vertical_dist)
            horitontal_dist = abs(horitontal_dist)
        return (vertical_dist, horizontal_dist)

    def move(self, direction):
        direction = direction.upper()
        if direction == "U":
            self.row += 1
        elif direction == "D":
            self.row -= 1
        elif direction == "L":
            self.col -= 1
        elif direction == "R":
            self.col += 1
        else:
            raise ValueError("Invalid direction.")

    def follow(self, other, max_distance=1):
        # Vertical and horizontal distance
        vdist, hdist = self.get_distance_from(other)
        abs_vdist, abs_hdist = abs(vdist), abs(hdist)
        # No need to move if the already within the allowable distance
        if max(abs_vdist, abs_hdist) <= max_distance:
            return
        # Only a vertical gap
        if abs_vdist > 0 and abs_hdist == 0:
            # `self` is above `other`
            if vdist > 0:
                self.row = other.row + 1
            # `self` is below `other`
            else:
                self.row = other.row - 1
        # Only a horizontal gap
        elif abs_vdist == 0 and abs_hdist > 0:
            # `self` is to the right of `other`
            if hdist > 0:
                self.col = other.col + 1
            # `self` is to the left of `other`
            else:
                self.col = other.col - 1
        # Both (bigger) vertical and (smaller) horizontal gaps
        elif abs_vdist > abs_hdist:
            self.col = other.col
            # `self` is above `other`
            if vdist > 0:
                self.row = other.row + 1
            # `self` is below `other`
            else:
                self.row = other.row - 1
        # Both (smaller) vertical and (bigger) horizontal gaps
        elif abs_vdist < abs_hdist:
            self.row = other.row
            # `self` is to the right of `other`
            if hdist > 0:
                self.col = other.col + 1
            # `self` is to the left of `other`
            else:
                self.col = other.col - 1
        # If `self` is 2 spots away diagonally
        elif abs_vdist == abs_hdist and abs_vdist == 2:
            # `self` is to the top-right of `other`
            if hdist > 0 and vdist > 0:
                self.row = other.row + 1
                self.col = other.col + 1
            # `self` is to the top-left of `other`
            elif hdist < 0 and vdist > 0:
                self.row = other.row + 1
                self.col = other.col - 1
            # `self` is to the bottom-right of `other`
            elif hdist > 0 and vdist < 0:
                self.row = other.row - 1
                self.col = other.col + 1
            # `self` is to the bottom-left of `other`
            elif hdist < 0 and vdist < 0:
                self.row = other.row - 1
                self.col = other.col - 1
        else:
            raise ValueError("Unexpected vertical and horizontal distance.")

    def get_coordinates(self):
        return (self.row, self.col)


class RopeGrid:
    knots: Sequence[Coordinate]
    max_distance: int
    tail_history: Sequence[Sequence]

    def __init__(self, rope_length, size) -> None:
        self.knots = [Coordinate() for x in range(rope_length)]
        self.size = size
        self.tail_history = []
        self.snapshot()
        # self.print("Initial State")

    def print(self, title=None):
        current_height, current_width = self.get_grid_size()
        width = max(self.size, current_width)
        height = max(self.size, current_height)
        grid = [["•" for _ in range(width)] for _ in range(height)]
        for index in range(len(self.knots)-1, -1, -1):
            if index == 0:
                name = "H"
            elif index == len(self.knots) - 1:
                name = "T"
            else:
                name = str(index)
            knot = self.knots[index]
            row, col = knot.get_coordinates()
            grid[row][col] = name
        text_list = []
        for row in reversed(grid):
            row_str = "".join(row)
            text_list.append(row_str)
        text_str = "\n".join(text_list) + "\n"
        if title:
            print(f"== {title} ==\n")
        print(text_str)

    def get_grid_size(self):
        min_row, max_row = 0, 0
        min_col, max_col = 0, 0
        for knot in self.knots:
            row, col = knot.get_coordinates()
            min_row = min(min_row, row)
            max_row = max(max_row, row)
            min_col = min(min_col, col)
            max_col = max(max_col, col)
        height = max_row - min_row + 1
        width  = max_col - min_col + 1
        return (height, width)

    def snapshot(self):
        tail_coords = self.knots[-1].get_coordinates()
        self.tail_history.append(tail_coords)

    def move(self, direction, distance):
        head = self.knots[0]
        for _ in range(distance):
            head.move(direction)
            for index, knot in enumerate(self.knots[1:], 1):
                previous_knot = self.knots[index-1]
                knot.follow(previous_knot)
            self.snapshot()
            # self.print(f"{direction} {distance}")


class InputParser:

    path: str

    def __init__(self, path) -> None:
        self.path = path

    def parse(self, rope_length, grid_size=5):
        grid = RopeGrid(rope_length, grid_size)
        with open(self.path, "r") as infile:
            for line in infile:
                line = line.strip()
                direction, distance = line.split(" ")
                distance = int(distance)
                grid.move(direction, distance)
        return grid


if __name__ == "__main__":
    input_path = sys.argv[1]
    parser = InputParser(input_path)
    # Part 1
    grid_1 = parser.parse(rope_length=2)
    tail_visits_1 = list(set(grid_1.tail_history))
    print("Part 1:", len(tail_visits_1))
    grid_1.print("Final State")
    # Part 2
    grid_2 = parser.parse(rope_length=10, grid_size=6)
    tail_visits_2 = list(set(grid_2.tail_history))
    print("Part 2:", len(tail_visits_2))
    grid_2.print("Final State")
