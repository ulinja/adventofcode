"""Solves Advent of Code 2023 - Day 03."""

from aoc.utils.file import get_path_to_input_data
from aoc.year23.day03.schematic import Schematic


def main():
    schematic = Schematic(get_path_to_input_data(23, 3))

    part_number_sum = 0
    for part_number in schematic.part_numbers:
        part_number_sum += part_number.value

    gear_ratio_sum = 0
    for gear in schematic.gears:
        gear_ratio_sum += gear.gear_ratio

    print(f"Sum of all part numbers in schematic (Part I): {part_number_sum}")
    print(f"Sum of all gear ratios in schematic (Part II): {gear_ratio_sum}")
