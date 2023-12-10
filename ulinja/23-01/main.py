#!/usr/bin/env python3
"""Solves Advent of Code 2023 - Day 01."""

from typing import List
from pathlib import Path
from string import digits as DIGITS


def get_lines() -> List[str]:
    """Retrieves the lines of the input file as a list of strings."""

    PATH_TO_INPUT_FILE = Path('input.txt').resolve()
    if not PATH_TO_INPUT_FILE.is_file():
        raise FileNotFoundError(f"Input file not found: '{PATH_TO_INPUT_FILE}'")

    lines = []
    with open(PATH_TO_INPUT_FILE) as input_file:
        lines = input_file.readlines()

    return lines


def parse_value_from_line(input_str: str) -> int:
    """Retrieves the calibration value from a line."""

    if not isinstance(input_str, str):
        raise TypeError(f"Expected input to be of type 'str' but got: '{type(input_str)}'")

    first_digit = last_digit = None
    for char in input_str:
        if char in DIGITS:
            first_digit = char
            break
    if first_digit is None:
        raise RuntimeError("Came across a line which contains no digits.")
    for char in reversed(input_str):
        if char in DIGITS:
            last_digit = char
            break

    return int(f"{first_digit}{last_digit}")


def main():
    """Parses the caliration values from the input files, sums them up and prints the result."""

    lines = get_lines()
    sum = 0
    for line in lines:
        sum += parse_value_from_line(line)

    print(sum)


if __name__ == '__main__':
    main()
