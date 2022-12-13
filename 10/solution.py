#!/usr/bin/env python3

from abc import ABC, abstractmethod
from collections.abc import Sequence
import sys


class Observer(ABC):
    @abstractmethod
    def update(self, cycle, x): ...


class Subject(ABC):
    @abstractmethod
    def register_observer(self, observer: Observer): ...

    @abstractmethod
    def remove_observer(self, observer: Observer): ...

    @abstractmethod
    def notify_observers(self): ...


class CPU(Subject):
    cycle: int
    x: int
    observers: Observer

    def __init__(self) -> None:
        self.cycle = 0
        self.x = 1
        self.observers = set()

    def execute_noop(self):
        # Cycle 1
        self.start_cycle()
        self.end_cycle()

    def execute_addx(self, x: int):
        x = int(x)
        # Cycle 1
        self.start_cycle()
        self.end_cycle()
        # Cycle 2
        self.start_cycle()
        self.x += x
        # print(f"Incrementing register X to {self.x}")
        self.end_cycle()

    def start_cycle(self):
        self.cycle += 1
        # print(f"Starting cycle {self.cycle}")
        self.notify_observers()

    def end_cycle(self):
        pass

    def register_observer(self, observer: Observer):
        return self.observers.add(observer)

    def remove_observer(self, observer: Observer):
        return self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.cycle, self.x)


class Tracker(Observer):
    history: Sequence

    def __init__(self) -> None:
        self.reset()

    def update(self, cycle, x):
        self.history.append((cycle, x))

    def calc_signal_strength(self):
        total_signal_strength = 0
        for position in range(20, len(self.history), 40):
            index = position - 1
            _, x = self.history[index]
            signal_strength = position * x
            total_signal_strength += signal_strength
            # print(position, x, signal_strength, sep=", ")
        return total_signal_strength

    def reset(self):
        self.history = []


class CRT(Observer):
    width: int
    height: int
    screen: Sequence[Sequence[str]]
    sprite_center: int
    cursor: Sequence[int]

    def __init__(self, width=40, height=6) -> None:
        self.width = width
        self.height = height
        self.reset()
        self.sprite_center = 1
        self.cursor = [0, 0]

    def update(self, cycle, x):
        # print(f"Cycle {cycle} / X = {x}")
        self.sprite_center = x
        self.draw()

    def draw(self):
        cursor_row, cursor_col = self.cursor
        sprite_left_edge = self.sprite_center - 1
        sprite_right_edge = self.sprite_center + 1
        # print(self.cursor)
        if cursor_col >= sprite_left_edge and cursor_col <= sprite_right_edge:
            self.screen[cursor_row][cursor_col] = "#"
        else:
            self.screen[cursor_row][cursor_col] = " "
        self.increment_cursor()
        # self.print()

    def increment_cursor(self):
        cursor_row, cursor_col = self.cursor
        max_row_index = self.height - 1
        max_col_index = self.width - 1
        if cursor_col < max_col_index:
            self.cursor = [cursor_row, cursor_col + 1]
        elif cursor_col >= max_col_index and cursor_row < max_row_index:
            self.cursor = [cursor_row + 1, 0]
        elif cursor_col >= max_col_index and cursor_row >= max_row_index:
            self.cursor = [0, 0]

    def reset(self):
        self.screen = [["_" for _ in range(self.width)] for _ in range(self.height)]

    def print(self):
        text_list = []
        for row in self.screen:
            row_str = "".join(row)
            text_list.append(row_str)
        text_list.append("\n")
        print("\n".join(text_list))


class InputParser:

    path: str

    def __init__(self, path) -> None:
        self.path = path

    def parse(self, cpu: CPU):
        with open(self.path, "r") as infile:
            for line in infile:
                line = line.strip()
                operation, _, argument = line.partition(" ")
                if operation == "addx":
                    cpu.execute_addx(argument)
                elif operation == "noop":
                    cpu.execute_noop()


if __name__ == "__main__":
    # Set up parser
    input_path = sys.argv[1]
    parser = InputParser(input_path)
    # Part 1
    cpu_1 = CPU()
    tracker = Tracker()
    cpu_1.register_observer(tracker)
    parser.parse(cpu_1)
    signal_strength = tracker.calc_signal_strength()
    print("Part 1:", signal_strength)
    # Part 2
    cpu_2 = CPU()
    crt = CRT()
    cpu_2.register_observer(crt)
    print("Part 2:")
    parser.parse(cpu_2)
    crt.print()
