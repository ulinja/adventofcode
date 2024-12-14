"""Solves Advent of Code 2023 - Day 05."""

from aoc.utils.file import get_lines_from_file, get_path_to_input_data
from aoc.year23.day05.mapping import MapSequence


def main():
    path_to_data_file = get_path_to_input_data(23, 5)
    map_sequence = MapSequence(get_lines_from_file(path_to_data_file))
    map_sequence_with_range = MapSequence(get_lines_from_file(path_to_data_file), treat_seeds_as_ranges=True)

    print(f"Lowest location number (Part I): {map_sequence.get_smallest_location()}")
    #print(f"Lowest location number (Part II): {map_sequence_with_range.get_smallest_location()}")

    map_sequence_with_range.approximate_composite_mapping_function(10_000_000)
