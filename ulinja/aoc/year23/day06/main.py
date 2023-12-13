"""Solves Advent of Code 2023 - Day 06."""

from typing import List

from aoc.utils.file import get_lines_from_file, get_path_to_input_data
from aoc.year23.day06.race import Race


def main():
    path_to_data_file = get_path_to_input_data(23, 6)
    lines: List[str] = get_lines_from_file(path_to_data_file)
    races: List[Race] = Race.from_lines(lines)
    races_bad_kerning: List[Race] = Race.from_lines(lines, bad_kerning=True)

    race_win_product = 1
    for race in races:
        race_win_product *= len(race.get_winning_instances())

    race_win_product_bad_kerning = 1
    for race in races_bad_kerning:
        race_win_product_bad_kerning *= len(race.get_winning_instances())

    print(f"Product of all winning race configuration counts (Part I): {race_win_product}")
    print(f"Count of winning race conditions with bad kerning (Part II): {race_win_product_bad_kerning}")
