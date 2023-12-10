"""Solves Advent of Code 2023 - Day 02."""

from typing import List

from aoc.utils.file import get_path_to_input_data
from aoc.year23.day03.schematic import Schematic


def main():
    schematic = Schematic(get_path_to_input_data(23, 3))
    part_number_sum = 0
    for part_number in schematic.part_numbers:
        part_number_sum += part_number.value

    print(f"Sum of all part numbers in schematic (Part I): {part_number_sum}")
