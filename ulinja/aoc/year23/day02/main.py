"""Solves Advent of Code 2023 - Day 02."""

from typing import List

from aoc.utils.file import get_path_to_input_data, get_lines_from_file
from aoc.year23.day02.game import Game


def main():
    """Parses the calibration values from the input file, sums them up and prints the results."""

    lines: List[str] = get_lines_from_file(get_path_to_input_data(23, 2))
    games: List[Game] = []
    for line in lines:
        games.append(Game(line))

    id_sum = 0
    for game in games:
        if game.possible_with(red_max_count=12, green_max_count=13, blue_max_count=14):
            id_sum += game.id

    print(f"Sum of IDs of all possible games (Part I): {id_sum}")
