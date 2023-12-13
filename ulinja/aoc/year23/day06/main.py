"""Solves Advent of Code 2023 - Day 06."""

from typing import List

from aoc.utils.file import get_lines_from_file, get_path_to_input_data
from aoc.year23.day06.race import Race


def main():
    path_to_data_file = get_path_to_input_data(23, 6)
    lines: List[str] = get_lines_from_file(path_to_data_file)
    races: List[Race] = Race.from_lines(lines)

    race_win_product = 1
    for race in races:
        race_win_product *= len(race.get_winning_instances())

    print(f"Product of all winning race configuration counts (Part I): {race_win_product}")
    #print(f"Total number of scratchcards after copying (Part II): {stacks_sum}")
