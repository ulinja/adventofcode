"""Solves Advent of Code 2023 - Day 01."""

from aoc.utils.file import get_path_to_input_data, get_lines_from_file
from aoc.year23.day01.calibrationdigit import parse_calibration_digits_from_line

def main():
    """Parses the calibration values from the input file, sums them up and prints the results."""

    lines = get_lines_from_file(get_path_to_input_data(23, 1))
    sum_numeric = sum_with_words = 0
    for line in lines:
        digits_numeric = parse_calibration_digits_from_line(line, parse_words=False)
        # Contstruct calibration value by concatenating the first and the last parsed digits
        calibration_value_numeric = int(f"{digits_numeric[0].value}{digits_numeric[-1].value}")
        sum_numeric += calibration_value_numeric

        digits_with_word = parse_calibration_digits_from_line(line, parse_words=True)
        calibration_value_with_words = int(f"{digits_with_word[0].value}{digits_with_word[-1].value}")
        sum_with_words += calibration_value_with_words

    print(f"Sum with numbers only (Part I): {sum_numeric}")
    print(f"Sum with words included (Part II): {sum_with_words}")
