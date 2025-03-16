"""Utilities for file operations."""

from typing import List
from pathlib import Path

import aoc


def get_path_to_input_data(year: int, day: int) -> Path:
    """Retrieves the absolute Path to the input data file for the specified challenge.

    Assumes that the input data files are in a named directory 'data' relative to the
    current working directory.
    Input data files must be named '<year>-<day>.txt', whereby <year> is the last two digits of
    the year, and <day> is the day padded with zeroes to length 2. For example:

    data
    ├── 23-01.txt
    ├── 23-02.txt
    ├── 23-03.txt
    └── 23-04.txt

    Returns
    -------
    pathlib.Path
        A Path object pointing to the input data file's absolute path.

    Raises
    ------
    FileNotFoundError
        If the input file could not be located.
    """

    if not isinstance(year, int):
        raise TypeError(f"Expected type 'int' for parameter 'year' but got: '{type(year)}'")
    if not aoc._AOC_MIN_YEAR <= year <= aoc._AOC_MAX_YEAR:
        raise ValueError(f"Value for 'year' must be in range [{aoc._AOC_MIN_YEAR}, {aoc._AOC_MAX_YEAR}].")

    if not isinstance(day, int):
        raise TypeError(f"Expected type 'int' for parameter 'day' but got: '{type(day)}'")
    if not 1 <= day <= 24:
        raise ValueError("Value for 'day' must be in range [1, 24].")


    path = Path(f"./data/{year}-{str(day).rjust(2, '0')}.txt").resolve().absolute()
    if not path.is_file():
        raise FileNotFoundError(f"Input file not found: '{path}'")

    return path


def get_lines_from_file(path: Path) -> List[str]:
    """Retrieves contents of the specified file as a list of strings, line by line.

    Returns
    -------
    List[str]
        List containing each line of the input file.

    Raises
    ------
    FileNotFoundError
        If the input file does not exist.
    """

    if not isinstance(path, Path):
        raise TypeError(f"Expetced file path to be of type 'pathlib.Path' but got: '{type(path)}'.")

    path = Path(path).resolve().absolute()
    if not path.is_file():
        raise FileNotFoundError(f"Input file does not exist: '{path}'")

    lines = []
    with open(path) as input_file:
        lines = input_file.readlines()

    return lines
