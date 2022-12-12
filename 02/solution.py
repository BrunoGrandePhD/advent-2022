#!/usr/bin/env python3

from collections.abc import Mapping, Collection
from enum import Enum, auto
from pathlib import Path
import sys


class Shape(Enum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()


class Outcome(Enum):
    LOSS = auto()
    DRAW = auto()
    WIN = auto()


class RockPaperScissors:

    hand_1: Shape

    hand_2: Shape

    shape_scoring_map: Mapping = {
        Shape.ROCK: 1,
        Shape.PAPER: 2,
        Shape.SCISSORS: 3,
    }

    outcome_scoring_map: Mapping = {
        Outcome.LOSS: 0,
        Outcome.DRAW: 3,
        Outcome.WIN: 6,
    }

    def __init__(self, hand_1, hand_2) -> None:
        self.hand_1 = hand_1
        self.hand_2 = hand_2
        self.outcome = self.calc_outcome(hand_1, hand_2)
        self.score = self.calc_score()

    def shape_to_score(self, shape: Shape):
        return self.shape_scoring_map[shape]

    @classmethod
    def calc_outcome(cls, hand_1, hand_2):
        if hand_1 == hand_2:
            return Outcome.DRAW
        if hand_1 == Shape.PAPER:
            if hand_2 == Shape.ROCK:
                return Outcome.WIN
            if hand_2 == Shape.SCISSORS:
                return Outcome.LOSS
        if hand_1 == Shape.ROCK:
            if hand_2 == Shape.SCISSORS:
                return Outcome.WIN
            if hand_2 == Shape.PAPER:
                return Outcome.LOSS
        if hand_1 == Shape.SCISSORS:
            if hand_2 == Shape.PAPER:
                return Outcome.WIN
            if hand_2 == Shape.ROCK:
                return Outcome.LOSS

    @classmethod
    def hand_1_from_outcome(cls, hand_2, desired_outcome):
        for hand_1 in Shape:
            actual_outcome = cls.calc_outcome(hand_1, hand_2)
            if actual_outcome == desired_outcome:
                return hand_1


    def outcome_to_score(self):
        return self.outcome_scoring_map[self.outcome]

    def calc_score(self):
        shape_score = self.shape_to_score(self.hand_1)
        outcome_score = self.outcome_to_score()
        return shape_score + outcome_score


class Tournament:

    rounds: Collection[RockPaperScissors]

    def __init__(self, rounds=None) -> None:
        self.rounds = rounds or []

    def add_round(self, round: RockPaperScissors):
        self.rounds.append(round)

    def calc_total_score(self):
        return sum(r.calc_score() for r in self.rounds)


class GuideParser:

    path: Path

    code_hand_map: Mapping = {
        "A": Shape.ROCK,
        "B": Shape.PAPER,
        "C": Shape.SCISSORS,
        "X": Shape.ROCK,
        "Y": Shape.PAPER,
        "Z": Shape.SCISSORS,
    }

    code_outcome_map: Mapping = {
        "X": Outcome.LOSS,
        "Y": Outcome.DRAW,
        "Z": Outcome.WIN,
    }

    def __init__(self, path) -> None:
        self.path = path

    def parse_hand(self, code):
        return self.code_hand_map[code]

    def parse_outcome(self, code):
        return self.code_outcome_map[code]

    def parse_part_1(self):
        with open(self.path) as infile:
            tournament = Tournament()
            for line in infile:
                line = line.strip()
                code_1, code_2 = line.split(" ")
                hand_1, hand_2 = self.parse_hand(code_1), self.parse_hand(code_2)
                # Swapping hands 1 and 2 since the second column is us
                round = RockPaperScissors(hand_2, hand_1)
                tournament.add_round(round)
                # print(f"Round: {line} = {round.calc_score()}")
        return tournament

    def parse_part_2(self):
        with open(self.path) as infile:
            tournament = Tournament()
            for line in infile:
                line = line.strip()
                code_1, code_2 = line.split(" ")
                hand_2 = self.parse_hand(code_1)
                desired_outcome = self.parse_outcome(code_2)
                hand_1 = RockPaperScissors.hand_1_from_outcome(hand_2, desired_outcome)
                round = RockPaperScissors(hand_1, hand_2)
                tournament.add_round(round)
                # print(f"Round: {hand_1.name} {hand_2.name} = {round.calc_score()}")
        return tournament


if __name__ == "__main__":
    input_path = sys.argv[1]
    parser_1 = GuideParser(input_path)
    tournament_1 = parser_1.parse_part_1()
    print("Part 1:", tournament_1.calc_total_score())
    parser_2 = GuideParser(input_path)
    tournament_2 = parser_2.parse_part_2()
    print("Part 2:", tournament_2.calc_total_score())
